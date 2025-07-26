import numpy as np
import plotly.graph_objects as go

# Sphere equation: x² + y² + z² = 2.5²
RADIUS = 2.5

# Grid parameters
GRID_MIN = -3
GRID_MAX = 3
CELL_SIZE = 1


# --------------------------------------------------
# Step 1: Compute exact edge intersections and normals
# --------------------------------------------------
def compute_exact_intersections_3d():
    cells = {}
    x_edges = np.arange(GRID_MIN, GRID_MAX + CELL_SIZE, CELL_SIZE)
    y_edges = np.arange(GRID_MIN, GRID_MAX + CELL_SIZE, CELL_SIZE)
    z_edges = np.arange(GRID_MIN, GRID_MAX + CELL_SIZE, CELL_SIZE)

    for i in range(len(x_edges) - 1):
        for j in range(len(y_edges) - 1):
            for k in range(len(z_edges) - 1):
                cell_x_min, cell_x_max = x_edges[i], x_edges[i + 1]
                cell_y_min, cell_y_max = y_edges[j], y_edges[j + 1]
                cell_z_min, cell_z_max = z_edges[k], z_edges[k + 1]
                intersections = []
                normals = []

                # Check all 12 edges of the cell
                # Edge along x-axis (fixed y, z)
                for y in [cell_y_min, cell_y_max]:
                    for z in [cell_z_min, cell_z_max]:
                        x_vals = np.sqrt(
                            RADIUS**2 - y**2 - z**2 + 1e-8
                        )  # Avoid sqrt(negative)
                        x_vals = np.real(x_vals)  # Ignore complex results
                        for x in [x_vals, -x_vals]:
                            if cell_x_min <= x <= cell_x_max:
                                intersections.append((x, y, z))
                                normals.append((x, y, z))

                # Edge along y-axis (fixed x, z)
                for x in [cell_x_min, cell_x_max]:
                    for z in [cell_z_min, cell_z_max]:
                        y_vals = np.sqrt(RADIUS**2 - x**2 - z**2 + 1e-8)
                        y_vals = np.real(y_vals)
                        for y in [y_vals, -y_vals]:
                            if cell_y_min <= y <= cell_y_max:
                                intersections.append((x, y, z))
                                normals.append((x, y, z))

                # Edge along z-axis (fixed x, y)
                for x in [cell_x_min, cell_x_max]:
                    for y in [cell_y_min, cell_y_max]:
                        z_vals = np.sqrt(RADIUS**2 - x**2 - y**2 + 1e-8)
                        z_vals = np.real(z_vals)
                        for z in [z_vals, -z_vals]:
                            if cell_z_min <= z <= cell_z_max:
                                intersections.append((x, y, z))
                                normals.append((x, y, z))

                # Normalize normals
                normals = [np.array(n) / np.linalg.norm(n) for n in normals]
                cells[(i, j, k)] = {"intersections": intersections, "normals": normals}

    return cells


# --------------------------------------------------
# Step 2: Solve least squares for vertex positions
# --------------------------------------------------
def compute_vertices_3d(cells):
    vertices = {}
    for (i, j, k), data in cells.items():
        if len(data["intersections"]) == 0:
            continue

        # Build A and b for least squares
        A = np.zeros((3, 3))
        b = np.zeros(3)

        for (x, y, z), n in zip(data["intersections"], data["normals"]):
            nx, ny, nz = n
            A += np.outer([nx, ny, nz], [nx, ny, nz])
            scalar = nx * x + ny * y + nz * z
            b += scalar * np.array([nx, ny, nz])

        # Regularize if singular
        epsilon = 1e-8
        A += epsilon * np.eye(3)

        try:
            v = np.linalg.solve(A, b)
            vertices[(i, j, k)] = v
        except np.linalg.LinAlgError:
            pass

    return vertices


# --------------------------------------------------
# Step 3: Resolve connectivity (edges between adjacent cells)
# --------------------------------------------------
def compute_edges_3d(vertices):
    edges = []
    for i, j, k in vertices:
        # Check neighbors in x, y, z directions
        for di, dj, dk in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
            neighbor_key = (i + di, j + dj, k + dk)
            if neighbor_key in vertices:
                edges.append([vertices[(i, j, k)], vertices[neighbor_key]])
    return edges


# --------------------------------------------------
# Execute pipeline
# --------------------------------------------------
cells = compute_exact_intersections_3d()
vertices = compute_vertices_3d(cells)
edges = compute_edges_3d(vertices)

# --------------------------------------------------
# Plotting with Plotly
# --------------------------------------------------
fig = go.Figure()

# Plot vertices
if vertices:
    vx, vy, vz = zip(*vertices.values())
    fig.add_trace(
        go.Scatter3d(
            x=vx,
            y=vy,
            z=vz,
            mode="markers",
            marker=dict(size=3, color="red"),
            name="Vertices",
        )
    )

# Plot edges
if edges:
    for edge in edges:
        x, y, z = zip(*edge)
        fig.add_trace(
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="lines",
                line=dict(color="blue", width=2),
                showlegend=False,
            )
        )

# Plot exact sphere for comparison
theta = np.linspace(0, 2 * np.pi, 50)
phi = np.linspace(0, np.pi, 50)
x_sphere = RADIUS * np.outer(np.cos(theta), np.sin(phi)).flatten()
y_sphere = RADIUS * np.outer(np.sin(theta), np.sin(phi)).flatten()
z_sphere = RADIUS * np.outer(np.ones(50), np.cos(phi)).flatten()

fig.add_trace(
    go.Scatter3d(
        x=x_sphere,
        y=y_sphere,
        z=z_sphere,
        mode="markers",
        marker=dict(size=1, color="rgba(0, 0, 255, 0.1)"),
        name="Exact Sphere",
    )
)

fig.update_layout(
    scene=dict(
        xaxis=dict(range=[GRID_MIN, GRID_MAX]),
        yaxis=dict(range=[GRID_MIN, GRID_MAX]),
        zaxis=dict(range=[GRID_MIN, GRID_MAX]),
        aspectmode="cube",
    ),
    margin=dict(l=80, r=0, b=0, t=40),
    # title='Dual Contouring for Sphere (Radius = 2.5)'
)

config = {
    "displayModeBar": True,
    "displaylogo": False,
}

fig.write_html(
    file="content/code/2025-01-20-dual-contouring/dc_3d.html",
    include_plotlyjs=True,
    full_html=True,
    auto_play=False,
    config=config,
)

fig.show()
