import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


class Cube:
    def __init__(self, center=[0, 0, 0], size=2, subdivide=True):
        self.center = np.array(center)
        self.size = size
        self.vertices = self._generate_vertices()
        self.edges = self._generate_edges()
        self.subcubes = self._generate_subcubes() if subdivide else []

    def _generate_vertices(self):
        s = self.size / 2
        vertices = []
        for x in [-s, s]:
            for y in [-s, s]:
                for z in [-s, s]:
                    vertices.append(self.center + np.array([x, y, z]))
        return np.array(vertices)

    def _generate_edges(self):
        return [
            (0, 1),
            (0, 2),
            (0, 4),
            (1, 3),
            (1, 5),
            (2, 3),
            (2, 6),
            (3, 7),
            (4, 5),
            (4, 6),
            (5, 7),
            (6, 7),
        ]

    def _generate_subcubes(self):
        s = self.size / 4
        centers = []
        for x in [-s, s]:
            for y in [-s, s]:
                for z in [-s, s]:
                    centers.append(self.center + np.array([x, y, z]))
        return [Cube(center=c, size=self.size / 2, subdivide=False) for c in centers]

    def plot(self, ax):
        ax.scatter(
            self.vertices[:, 0],
            self.vertices[:, 1],
            self.vertices[:, 2],
            color="red",
            s=50,
        )

        for edge in self.edges:
            v1, v2 = self.vertices[edge[0]], self.vertices[edge[1]]
            ax.plot3D(
                [v1[0], v2[0]],
                [v1[1], v2[1]],
                [v1[2], v2[2]],
                "gray",
                linestyle="--",
                alpha=0.1,
            )


# Create figure
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")

# Create and plot main cube
cube = Cube()
cube.plot(ax)

# Plot subcubes
for subcube in cube.subcubes:
    subcube.plot(ax)

# Set display parameters
ax.set_box_aspect([1, 1, 1])
plt.axis("off")
plt.show()
