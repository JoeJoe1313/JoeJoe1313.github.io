import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
from scipy.optimize import minimize


class DualContouring:
    def __init__(self, grid_size=20, bounds=(-1, 1)):
        """Initialize the dual contouring system with a grid size and bounds."""
        self.grid_size = grid_size
        self.bounds = bounds
        # Create grid points
        x = np.linspace(bounds[0], bounds[1], grid_size)
        y = np.linspace(bounds[0], bounds[1], grid_size)
        z = np.linspace(bounds[0], bounds[1], grid_size)
        self.X, self.Y, self.Z = np.meshgrid(x, y, z, indexing="ij")

    def sphere_sdf(self, x, y, z, radius=0.7):
        """Signed distance function for a sphere."""
        return np.sqrt(x**2 + y**2 + z**2) - radius

    def sphere_normal(self, x, y, z):
        """Calculate normal vector for sphere at given point."""
        norm = np.sqrt(x**2 + y**2 + z**2)
        return np.array([x / norm, y / norm, z / norm])

    def find_edge_intersections(self):
        """Find intersections of the surface with grid edges."""
        intersections = []
        normals = []

        # Sample the SDF at grid points
        sdf = self.sphere_sdf(self.X, self.Y, self.Z)

        # Check edges along each axis
        for axis in range(3):
            # Create slices for the current axis
            shape = [slice(None)] * 3
            shape[axis] = slice(None, -1)

            # Get signs at start and end of edges
            signs1 = sdf[tuple(shape)]
            shape[axis] = slice(1, None)
            signs2 = sdf[tuple(shape)]

            # Find edges that cross zero
            crossings = (signs1 * signs2) < 0

            if np.any(crossings):
                # Get indices of crossing edges
                idx = np.nonzero(crossings)

                # For each crossing edge
                for i in range(len(idx[0])):
                    # Get coordinates
                    coords = [idx[0][i], idx[1][i], idx[2][i]]

                    # Get start and end points of edge
                    p1 = np.array(
                        [
                            self.X[tuple(coords)],
                            self.Y[tuple(coords)],
                            self.Z[tuple(coords)],
                        ]
                    )

                    coords[axis] += 1
                    p2 = np.array(
                        [
                            self.X[tuple(coords)],
                            self.Y[tuple(coords)],
                            self.Z[tuple(coords)],
                        ]
                    )

                    # Linear interpolation to find intersection
                    t = signs1[idx[0][i], idx[1][i], idx[2][i]] / (
                        signs1[idx[0][i], idx[1][i], idx[2][i]]
                        - signs2[idx[0][i], idx[1][i], idx[2][i]]
                    )
                    intersection = p1 + t * (p2 - p1)

                    # Calculate normal at intersection
                    normal = self.sphere_normal(*intersection)

                    intersections.append(intersection)
                    normals.append(normal)

        return np.array(intersections), np.array(normals)

    def minimize_qef(self, points, normals):
        """Minimize the quadratic error function for a set of points and normals."""

        def error_func(x):
            error = 0
            for p, n in zip(points, normals):
                error += (np.dot(n, (x - p))) ** 2
            return error

        # Use mean point as initial guess
        x0 = np.mean(points, axis=0)
        result = minimize(error_func, x0, method="L-BFGS-B")
        return result.x

    def generate_mesh(self):
        """Generate the mesh using dual contouring."""
        # Find intersections and normals
        intersections, normals = self.find_edge_intersections()

        # Create vertices and faces
        vertices = []
        faces = []

        # Group intersections by cells they belong to
        cell_dict = {}
        for i, point in enumerate(intersections):
            # Find which cell this intersection belongs to
            cell_coords = tuple(
                np.floor(
                    (point - self.bounds[0])
                    / (self.bounds[1] - self.bounds[0])
                    * (self.grid_size - 1)
                ).astype(int)
            )

            if cell_coords not in cell_dict:
                cell_dict[cell_coords] = []
            cell_dict[cell_coords].append((point, normals[i]))

        # Generate vertex for each cell by solving QEF
        vertex_dict = {}
        for cell_coords, points_normals in cell_dict.items():
            points = np.array([p[0] for p in points_normals])
            norms = np.array([p[1] for p in points_normals])

            vertex = self.minimize_qef(points, norms)
            vertex_dict[cell_coords] = len(vertices)
            vertices.append(vertex)

        vertices = np.array(vertices)
        return vertices


def visualize_comparison(dc):
    """Create a visualization comparing input sphere with dual contouring output."""
    # Create PyVista plotter with two subplots
    pl = pv.Plotter(shape=(1, 2))

    # Plot input sphere
    sphere = pv.Sphere(radius=0.7, center=(0, 0, 0))
    pl.subplot(0, 0)
    pl.add_mesh(sphere, color="blue", opacity=0.7)
    pl.add_text("Input Sphere", position="upper_left")

    # Plot dual contouring result
    vertices = dc.generate_mesh()
    point_cloud = pv.PolyData(vertices)

    pl.subplot(0, 1)
    pl.add_mesh(point_cloud, color="red", point_size=10)
    pl.add_text("Dual Contouring Output", position="upper_left")

    # Set same camera position for both plots
    pl.link_views()
    pl.view_isometric()

    # Show the plot
    pl.show()


# Create and run the visualization
dc = DualContouring(grid_size=10)
visualize_comparison(dc)
