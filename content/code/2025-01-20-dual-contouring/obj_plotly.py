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
        opacity=0.8,
        # color="blue",
        colorscale="Viridis",
        intensity=vertices[:, 2],  # Color based on z-coordinate
        showscale=False,
    )

    # Create and customize the figure
    fig = go.Figure(data=[mesh_trace])
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
        title="3D Model Visualization",
    )

    return fig


if __name__ == "__main__":

    obj_file_path = "/Users/ljoana/repos/JoeJoe1313.github.io/content/images/2025-01-20-dual-contouring/output_mc.obj"
    fig = load_obj_plotly(obj_file_path)
    fig.show()

    config = {
        "displayModeBar": True,  # Show the toolbar
        # "modeBarButtonsToRemove": ["lasso2d", "select2d"],  # Remove unused buttons
        "displaylogo": False,
        # "toImageButtonOptions": {"height": 500, "width": 800},  # Image export size
    }
    fig.write_html(
        file="content/code/2025-01-20-dual-contouring/sphere.html",
        include_plotlyjs=True,
        full_html=True,
        auto_play=False,
        config=config,
    )
