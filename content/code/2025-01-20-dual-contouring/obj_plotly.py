import plotly.graph_objects as go
import trimesh


def load_obj_plotly(obj_path):
    """Load an OBJ file and convert it to a Plotly figure.

    Parameters:
    -----------
    obj_path (str): Path to the .obj file

    Returns:
    --------
    plotly.graph_objects.Figure: Interactive 3D visualization of the mesh
    """
    # Load the mesh using trimesh
    mesh = trimesh.load_mesh(obj_path)

    # Extract vertices and faces
    vertices = mesh.vertices
    faces = mesh.faces

    # Create the mesh3d trace
    mesh_trace = go.Mesh3d(
        # Vertices coordinates
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        # Face indices
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2],
        # Visual properties
        # opacity=0.75,  # More transparent to see edges better
        # colorscale="Viridis",
        # intensity=vertices[:, 2],
        showscale=False,
        # Enhanced edge visibility settings
        flatshading=True,
        lighting=dict(
            ambient=0.6,  # Reduced ambient light
            diffuse=0.9,  # Increased diffuse
            specular=0.1,  # Minimal specular reflection
            roughness=0.9,  # High roughness for matte look
        ),
        contour=dict(
            show=True, width=1.0, color="black"  # Thinner lines  # Black edges
        ),
    )

    # Create edges for wireframe
    edges_x = []
    edges_y = []
    edges_z = []

    for face in faces:
        # Connect vertices to form triangle edges
        for i in range(3):
            # Get current and next vertex indices
            current = face[i]
            next = face[(i + 1) % 3]

            # Add line segment
            edges_x.extend([vertices[current][0], vertices[next][0], None])
            edges_y.extend([vertices[current][1], vertices[next][1], None])
            edges_z.extend([vertices[current][2], vertices[next][2], None])

    # Create wireframe trace
    wireframe_trace = go.Scatter3d(
        x=edges_x,
        y=edges_y,
        z=edges_z,
        mode="lines",
        line=dict(color="black", width=2),
        showlegend=False,
    )

    # Create figure with both traces
    fig = go.Figure(data=[mesh_trace, wireframe_trace])
    fig.update_layout(
        scene=dict(
            aspectmode="data",  # Preserve original proportions
            camera=dict(
                up=dict(x=0, y=1, z=0),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=1.5),
            ),
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
        ),
        title="Dual Contouring",
    )

    return fig


if __name__ == "__main__":

    obj_file_path = "./content/images/2025-01-20-dual-contouring/output_dc.obj"
    fig = load_obj_plotly(obj_file_path)
    fig.show()

    config = {
        "displayModeBar": True,  # Show the toolbar
        # "modeBarButtonsToRemove": ["lasso2d", "select2d"],  # Remove unused buttons
        "displaylogo": False,
        # "toImageButtonOptions": {"height": 500, "width": 500},  # Image export size
    }
    fig.write_html(
        file="content/code/2025-01-20-dual-contouring/sphere_dc.html",
        include_plotlyjs=True,
        full_html=True,
        auto_play=False,
        config=config,
    )
