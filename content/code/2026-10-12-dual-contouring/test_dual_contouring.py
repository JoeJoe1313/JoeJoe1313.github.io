"""Geometry checks for the educational examples (Python unittest + NumPy)."""

import unittest
from collections import Counter

import numpy as np

from dual_contouring import contour, qef_vertex, sphere_field, sphere_gradient


class GeometryChecks(unittest.TestCase):
    def test_corner_fit(self):
        vertex = qef_vertex([[0.25, 0], [1, 0.7]], [[-1, 0], [0, 1]])
        np.testing.assert_allclose(vertex, [0.25, 0.7], atol=1e-12)

    def test_flat_patch_stays_near_samples_after_translation(self):
        points = np.array([[10, 20, 5], [12, 20, 5], [10, 22, 5.]])
        normals = np.tile([0, 0, 1.], (3, 1))
        np.testing.assert_allclose(qef_vertex(points, normals), points.mean(axis=0))
        shift = np.array([1000., -2000., 3000.])
        np.testing.assert_allclose(qef_vertex(points + shift, normals),
                                   points.mean(axis=0) + shift)

    def test_box_solve_is_better_than_coordinate_clamping(self):
        # These two tangent lines meet outside [0,1]^2 at (2, 0).
        points = np.array([[1, 1], [1, 0.5]])
        normals = np.array([[1, 1], [1, 2.]])
        vertex = qef_vertex(points, normals, [0, 0], [1, 1])
        np.testing.assert_allclose(vertex, [1, 9 / 13], atol=1e-12)
        clipped = np.clip(qef_vertex(points, normals), 0, 1)
        np.testing.assert_allclose(clipped, [1, 0], atol=1e-12)
        unit = normals / np.linalg.norm(normals, axis=1)[:, None]
        def error(x):
            return np.sum(np.einsum('ij,ij->i', unit, x - points)**2)
        self.assertLess(error(vertex), error(clipped))

    def test_circle_is_one_closed_loop(self):
        mesh = contour(sphere_field, sphere_gradient, np.arange(-3., 4.), 2)
        degree = Counter(v for edge in mesh.faces for v in edge)
        self.assertEqual(set(degree.values()), {2})
        self.assertEqual(len(mesh.vertices), len(mesh.faces))
        adjacency = {v: set() for v in degree}
        for a, b in mesh.faces:
            adjacency[a].add(b)
            adjacency[b].add(a)
        visited, stack = set(), [0]
        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                stack.extend(adjacency[v] - visited)
        self.assertEqual(len(visited), len(mesh.vertices))

    def test_sphere_is_closed_and_oriented(self):
        for grid in (np.arange(-3., 4.), np.linspace(-3.1, 3.1, 13)):
            mesh = contour(sphere_field, sphere_gradient, grid, 3)
            edges, directed = Counter(), Counter()
            for face in mesh.faces:
                self.assertEqual(len(set(face)), 4)
                for a, b in zip(face, face[1:] + face[:1]):
                    edges[tuple(sorted((a, b)))] += 1
                    directed[(a, b)] += 1
                points = mesh.vertices[list(face)]
                for triangle in ((0, 1, 2), (0, 2, 3)):
                    a, b, c = points[list(triangle)]
                    self.assertGreater(np.dot(np.cross(b - a, c - a), (a + b + c) / 3), 0)
            self.assertEqual(set(edges.values()), {2})
            self.assertTrue(all(directed[(b, a)] == count for (a, b), count in directed.items()))
            self.assertEqual(len(mesh.vertices) - len(edges) + len(mesh.faces), 2)
            for cell, vertex in mesh.cell_vertices.items():
                lower, upper = grid[list(cell)], grid[np.asarray(cell) + 1]
                self.assertTrue(np.all(mesh.vertices[vertex] >= lower - 1e-12))
                self.assertTrue(np.all(mesh.vertices[vertex] <= upper + 1e-12))
            for point, _ in mesh.samples.values():
                self.assertAlmostEqual(sphere_field(point), 0, places=9)

    def test_grid_corner_zero_is_explicit(self):
        with self.assertRaisesRegex(ValueError, 'grid corner'):
            contour(lambda p: np.dot(p, p) - 1, sphere_gradient, np.arange(-2., 3.), 2)


if __name__ == '__main__':
    unittest.main()
