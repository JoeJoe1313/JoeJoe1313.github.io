"""Small uniform-grid dual contourer used by the blog post.

Requires NumPy. Supports 2D segments and 3D quads, with one vertex per
active cell. This teaching implementation assumes a closed surface inside
the sampling box, at most one crossing per edge, and no grid-corner zeros.
It does not resolve ambiguous topology or implement adaptive octrees.
"""

from dataclasses import dataclass
from itertools import product

import numpy as np


def qef_vertex(points, normals, lower=None, upper=None):
    """Minimize squared distances to tangent planes, optionally in a box.

    Work relative to the sample centroid so a rank-deficient least-squares
    solve chooses the closest minimizer to that centroid. Box constraints
    are handled by solving on every face/edge/corner, not by clamping an
    unconstrained minimizer. There are at most 3**3 subproblems.
    """
    points = np.asarray(points, dtype=float)
    normals = np.asarray(normals, dtype=float)
    if points.ndim != 2 or points.shape != normals.shape or not len(points):
        raise ValueError("Expected matching, nonempty (samples, dimension) arrays")
    if not np.isfinite(points).all() or not np.isfinite(normals).all():
        raise ValueError("Hermite data must be finite")
    lengths = np.linalg.norm(normals, axis=1)
    if np.any(lengths == 0):
        raise ValueError("Normals must be nonzero")
    A = normals / lengths[:, None]
    center = points.mean(axis=0)
    rhs = np.einsum("ij,ij->i", A, points - center)
    offset = np.linalg.lstsq(A, rhs, rcond=None)[0]
    if lower is None and upper is None:
        return center + offset
    if lower is None or upper is None:
        raise ValueError("Provide both lower and upper bounds")
    lo = np.asarray(lower, dtype=float) - center
    hi = np.asarray(upper, dtype=float) - center
    if lo.shape != center.shape or hi.shape != center.shape or np.any(lo > hi):
        raise ValueError("Bounds must match the dimension and satisfy lower <= upper")
    if np.all(offset >= lo) and np.all(offset <= hi):
        return center + offset

    candidates = []
    for state in product((-1, 0, 1), repeat=points.shape[1]):
        # -1: fixed at lower bound; 0: free; +1: fixed at upper bound.
        state = np.asarray(state)
        free = state == 0
        fixed = ~free
        y = np.zeros_like(center)
        y[state == -1] = lo[state == -1]
        y[state == 1] = hi[state == 1]
        if free.any():
            remaining = rhs - A[:, fixed] @ y[fixed]
            y[free] = np.linalg.lstsq(A[:, free], remaining, rcond=None)[0]
        if np.all(y >= lo) and np.all(y <= hi):
            residual = A @ y - rhs
            candidates.append((float(residual @ residual), float(y @ y), y.copy()))
    _, _, offset = min(candidates, key=lambda item: item[:2])
    return center + offset


@dataclass
class Contour:
    vertices: np.ndarray
    faces: list
    cell_vertices: dict
    samples: dict
    grid: np.ndarray


def incident_cells(axis, index, dimension):
    """Cells around an edge, in cyclic order for a 3D quad."""
    if dimension == 2:
        perpendicular = (axis + 1) % 2
        cells = []
        for offset in (-1, 0):
            cell = list(index)
            cell[perpendicular] += offset
            cells.append(tuple(cell))
        return cells
    u, v = (axis + 1) % 3, (axis + 2) % 3
    cells = []
    for du, dv in ((-1, -1), (0, -1), (0, 0), (-1, 0)):
        cell = list(index)
        cell[u] += du
        cell[v] += dv
        cells.append(tuple(cell))
    return cells


def contour(field, gradient, grid, dimension=3):
    """Extract a closed contour using f < 0 for the inside convention."""
    grid = np.asarray(grid, dtype=float)
    if dimension not in (2, 3) or grid.ndim != 1 or len(grid) < 2:
        raise ValueError("Use dimension 2 or 3 and a one-dimensional grid")
    spacing = np.diff(grid)
    if np.any(spacing <= 0) or not np.allclose(spacing, spacing[0]):
        raise ValueError("Grid coordinates must be increasing and uniformly spaced")
    size = len(grid)
    values = np.empty((size,) * dimension)
    for index in np.ndindex(values.shape):
        values[index] = field(grid[list(index)])
    if not np.isfinite(values).all():
        raise ValueError("Field samples must be finite")
    if np.any(values == 0):
        raise ValueError("Surface hits a grid corner; shift or refine this demo grid")

    samples, cell_samples, neighbors = {}, {}, {}
    for axis in range(dimension):
        edge_shape = [size] * dimension
        edge_shape[axis] -= 1
        for index in np.ndindex(tuple(edge_shape)):
            end = list(index)
            end[axis] += 1
            start_inside = values[index] < 0
            if start_inside == (values[tuple(end)] < 0):
                continue
            cells = incident_cells(axis, index, dimension)
            if any(any(c < 0 or c >= size - 1 for c in cell) for cell in cells):
                raise ValueError("Surface reaches the sampling box; enlarge the grid")
            left, right = grid[list(index)].copy(), grid[end].copy()
            # Refine the actual analytic field, not its linear interpolant.
            for _ in range(40):
                middle = (left + right) / 2
                value = field(middle)
                if value == 0:
                    left = right = middle
                    break
                if (value < 0) == start_inside:
                    left = middle
                else:
                    right = middle
            point = (left + right) / 2
            normal = np.asarray(gradient(point), dtype=float)
            length = np.linalg.norm(normal)
            if not np.isfinite(length) or length == 0:
                raise ValueError("Intersection has an undefined or zero normal")
            normal = normal / length
            key = (axis, *index)
            samples[key] = (point, normal)
            neighbors[key] = (cells, start_inside)
            for cell in cells:
                cell_samples.setdefault(cell, []).append(key)

    vertices, cell_vertices = [], {}
    for cell, keys in sorted(cell_samples.items()):
        points, normals = zip(*(samples[key] for key in keys))
        lower = grid[list(cell)]
        upper = grid[np.asarray(cell) + 1]
        cell_vertices[cell] = len(vertices)
        vertices.append(qef_vertex(points, normals, lower, upper))

    faces = []
    for cells, start_inside in neighbors.values():
        face = tuple(cell_vertices[cell] for cell in cells)
        if dimension == 3 and not start_inside:
            face = face[::-1]
        faces.append(face)
    return Contour(np.asarray(vertices).reshape(-1, dimension), faces,
                   cell_vertices, samples, grid)


def sphere_field(point):
    return np.dot(point, point) - 2.5**2


def sphere_gradient(point):
    return 2 * np.asarray(point)


if __name__ == "__main__":
    grid = np.arange(-3.0, 4.0)
    for dimension in (2, 3):
        mesh = contour(sphere_field, sphere_gradient, grid, dimension)
        element = "segments" if dimension == 2 else "quads"
        print(f"{dimension}D: {len(mesh.vertices)} vertices, {len(mesh.faces)} {element}")
