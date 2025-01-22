import plotly.graph_objects as go
import trimesh
from plotly.subplots import make_subplots


def get_mesh_traces(obj_path):
    """Create mesh and wireframe traces for a single OBJ file"""
    mesh = trimesh.load_mesh(obj_path)
    vertices = mesh.vertices
    faces = mesh.faces

    mesh_trace = go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2],
        showscale=False,
        flatshading=True,
        lighting=dict(ambient=0.6, diffuse=0.9, specular=0.1, roughness=0.9),
        contour=dict(show=True, width=1.0, color="black"),
    )

    edges_x, edges_y, edges_z = [], [], []
    for face in faces:
        for i in range(3):
            current = face[i]
            next = face[(i + 1) % 3]
            edges_x.extend([vertices[current][0], vertices[next][0], None])
            edges_y.extend([vertices[current][1], vertices[next][1], None])
            edges_z.extend([vertices[current][2], vertices[next][2], None])

    wireframe_trace = go.Scatter3d(
        x=edges_x,
        y=edges_y,
        z=edges_z,
        mode="lines",
        line=dict(color="black", width=2),
        showlegend=False,
    )

    return mesh_trace, wireframe_trace


def plot_two_obj(obj_path1, obj_path2, title1="Mesh 1", title2="Mesh 2"):
    """Plot two OBJ files side by side"""
    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "scene"}, {"type": "scene"}]],
        subplot_titles=(title1, title2),
    )

    # Load and add first mesh
    mesh1, wire1 = get_mesh_traces(obj_path1)
    fig.add_trace(mesh1, row=1, col=1)
    fig.add_trace(wire1, row=1, col=1)

    # Load and add second mesh
    mesh2, wire2 = get_mesh_traces(obj_path2)
    fig.add_trace(mesh2, row=1, col=2)
    fig.add_trace(wire2, row=1, col=2)

    # Update layout
    camera = dict(
        up=dict(x=0, y=1, z=0),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=1.5, y=1.5, z=1.5),
    )

    fig.update_layout(
        # title="Mesh Comparison",
        scene=dict(
            aspectmode="data",
            camera=camera,
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
        ),
        scene2=dict(
            aspectmode="data",
            camera=camera,
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
        ),
    )

    return fig


if __name__ == "__main__":
    obj_file1 = "./content/images/2025-01-20-dual-contouring/output_mc.obj"
    obj_file2 = "./content/images/2025-01-20-dual-contouring/output_dc.obj"

    fig = plot_two_obj(obj_file1, obj_file2, "Marching Cubes", "Dual Contouring")

    config = {
        "displayModeBar": True,
        "displaylogo": False,
    }

    fig.write_html(
        file="content/code/2025-01-20-dual-contouring/comparison.html",
        include_plotlyjs=True,
        full_html=True,
        auto_play=False,
        config=config,
    )

    fig.show()
