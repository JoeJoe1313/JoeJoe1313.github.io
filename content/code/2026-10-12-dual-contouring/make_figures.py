"""Generate the article's SVG figures and self-contained interactive sphere.

Requires numpy, matplotlib, plotly. Run from any working directory.
Optional: --preview-dir /tmp/dual-contouring-preview writes PNG previews.
"""

import argparse
from itertools import product
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from dual_contouring import contour, qef_vertex, sphere_field, sphere_gradient


HERE = Path(__file__).resolve().parent
IMAGE_DIR = HERE.parents[1] / "images" / HERE.name
BLUE, ORANGE, GREEN = "#2476aa", "#d17735", "#25836c"
INK, GRID = "#253b50", "#dce2e8"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "text.color": INK, "axes.labelcolor": INK,
                     "axes.titleweight": "semibold", "axes.titlesize": 13,
                     "svg.hashsalt": "dual-contouring-article"})


def axes2d(ax, title, limits):
    ax.set_aspect("equal")
    ax.set_title(title, pad=16)
    ax.set_xlim(*limits)
    ax.set_ylim(*limits)
    ax.spines[["top", "right"]].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(color=GRID, labelcolor=INK)


def corner_figure():
    points = np.array([[0.25, 0.0], [1.0, 0.7]])
    normals = np.array([[-1, 0], [0, 1]])
    vertex = qef_vertex(points, normals)
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.9), layout="constrained")
    for ax, title in zip(axes, ("Marching Squares: connect crossings", "Dual Contouring: fit the tangent lines")):
        axes2d(ax, title, (-0.12, 1.16))
        ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, ec=GRID, lw=1.4))
        ax.plot([0.25, 0.25, 1], [0, 0.7, 0.7], color=INK, ls="--", lw=1.5,
                label="Exact boundary")
        ax.scatter(*points.T, s=55, c=BLUE, zorder=5, label="Hermite positions")
        ax.set_xticks([0, 0.25, 1])
        ax.set_yticks([0, 0.7, 1])
    axes[0].plot(*points.T, color=ORANGE, lw=2.6, label="Local contour segment")
    axes[1].axvline(0.25, color=GREEN, alpha=0.45, lw=1.2)
    axes[1].axhline(0.7, color=GREEN, alpha=0.45, lw=1.2)
    for point, normal in zip(points, normals):
        axes[1].annotate("", point + 0.2 * normal, point,
                         arrowprops={"arrowstyle": "->", "color": BLUE, "lw": 1.8})
    axes[1].scatter(*vertex, marker="D", s=65, c=ORANGE, zorder=6, label="QEF vertex")
    axes[1].annotate(r"$(0.25,\ 0.7)$", vertex, xytext=(12, 16), textcoords="offset points")
    for ax in axes:
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False, fontsize=10)
    return fig


def circle_figure(mesh):
    fig, axes = plt.subplots(1, 2, figsize=(10, 5.4), layout="constrained")
    theta = np.linspace(0, 2 * np.pi, 400)
    for ax, title in zip(axes, ("1. Sample edge crossings and normals", "2. Fit cell vertices and connect across crossings")):
        axes2d(ax, title, (-3.15, 3.15))
        for value in mesh.grid:
            ax.axhline(value, color=GRID, lw=0.7, zorder=0)
            ax.axvline(value, color=GRID, lw=0.7, zorder=0)
        ax.plot(2.5 * np.cos(theta), 2.5 * np.sin(theta), "--", color=INK,
                lw=1.2, alpha=0.7, label="Exact circle")
        ax.set_xticks([-3, 0, 3])
        ax.set_yticks([-3, 0, 3])
    for cell in mesh.cell_vertices:
        lower = mesh.grid[list(cell)]
        axes[0].add_patch(Rectangle(lower, 1, 1, color=BLUE, alpha=0.06, zorder=0))
    positions = np.array([sample[0] for sample in mesh.samples.values()])
    axes[0].scatter(*positions.T, color=BLUE, s=24, label="Edge crossings", zorder=4)
    for point, normal in mesh.samples.values():
        axes[0].annotate("", point + 0.30 * normal, point,
                         arrowprops={"arrowstyle": "->", "color": BLUE, "lw": 1.2})
    segments = [mesh.vertices[list(edge)] for edge in mesh.faces]
    axes[1].add_collection(LineCollection(segments, colors=ORANGE, linewidths=2))
    axes[1].scatter(*mesh.vertices.T, color=ORANGE, s=28, label="Dual vertices", zorder=5)
    for ax in axes:
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.06), frameon=False)
    return fig


def edge_figure():
    fig = plt.figure(figsize=(7.4, 5.5), layout="constrained")
    ax = fig.add_subplot(projection="3d")
    edges = set()
    for cx, cy in product((-1, 0), repeat=2):
        corners = list(product((cx, cx + 1), (cy, cy + 1), (0, 1)))
        for a in corners:
            for b in corners:
                if sum(x != y for x, y in zip(a, b)) == 1:
                    edges.add(tuple(sorted((a, b))))
    for edge in edges:
        ax.plot(*np.array(edge).T, color="#b6c2cd", lw=0.9, alpha=0.65)
    quad = np.array([[-.5, -.5], [.5, -.5], [.5, .5], [-.5, .5]])
    quad = np.column_stack([quad, .5 + .1 * quad[:, 0] - .05 * quad[:, 1]])
    ax.add_collection3d(Poly3DCollection([quad], facecolors=ORANGE, edgecolors=ORANGE,
                                        alpha=0.55, linewidths=2))
    ax.scatter(*quad.T, c=ORANGE, s=45, depthshade=False)
    ax.plot([0, 0], [0, 0], [0, 1], color=BLUE, lw=3)
    ax.scatter([0, 0], [0, 0], [0, 1], c=[INK, "white"], edgecolors=INK,
               s=55, depthshade=False)
    ax.text(0.04, 0.02, 1.06, "+", color=INK, fontsize=15)
    ax.text(0.03, 0.02, -.12, "−", color=INK, fontsize=15)
    ax.set_title("One crossed grid edge → one face joining four cell vertices", pad=12)
    ax.set_box_aspect((2, 2, 1.15))
    ax.view_init(elev=24, azim=-60)
    ax.set_axis_off()
    return fig


def sphere_figure(mesh):
    fig = plt.figure(figsize=(7, 6.2), layout="constrained")
    ax = fig.add_subplot(projection="3d")
    polygons = [mesh.vertices[list(face)] for face in mesh.faces]
    ax.add_collection3d(Poly3DCollection(polygons, facecolors="#91c4d9", edgecolors=INK,
                                        linewidths=0.65, alpha=0.95))
    ax.set(xlim=(-3, 3), ylim=(-3, 3), zlim=(-3, 3), xlabel="x", ylabel="y", zlabel="z")
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=22, azim=35)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_ticks([-3, 0, 3])
    ax.set_title(f"{len(mesh.vertices)} cell vertices · {len(mesh.faces)} quads", pad=12)
    return fig


def write_interactive(mesh):
    triangles = np.array([(f[0], f[1], f[2]) for f in mesh.faces]
                         + [(f[0], f[2], f[3]) for f in mesh.faces])
    fig = go.Figure(go.Mesh3d(x=mesh.vertices[:, 0], y=mesh.vertices[:, 1],
                            z=mesh.vertices[:, 2], i=triangles[:, 0], j=triangles[:, 1],
                            k=triangles[:, 2], color="#76b7cf", flatshading=True,
                            name="Surface", showlegend=True, hoverinfo="skip"))
    edges = {tuple(sorted((a, b))) for face in mesh.faces
             for a, b in zip(face, face[1:] + face[:1])}
    lines = []
    for a, b in sorted(edges):
        lines.extend([mesh.vertices[a].tolist(), mesh.vertices[b].tolist(), [None] * 3])
    x, y, z = zip(*lines)
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode="lines", name="Quad edges",
                              line={"color": INK, "width": 3}, hoverinfo="skip"))
    fig.add_trace(go.Scatter3d(x=mesh.vertices[:, 0], y=mesh.vertices[:, 1],
                              z=mesh.vertices[:, 2], mode="markers", name="Cell vertices",
                              marker={"color": ORANGE, "size": 3}, visible="legendonly"))
    theta, phi = np.meshgrid(np.linspace(0, 2 * np.pi, 60), np.linspace(0, np.pi, 30))
    fig.add_trace(go.Surface(x=2.5 * np.cos(theta) * np.sin(phi),
                            y=2.5 * np.sin(theta) * np.sin(phi), z=2.5 * np.cos(phi),
                            opacity=0.3, colorscale=[[0, GREEN], [1, GREEN]], showscale=False,
                            name="Exact sphere", visible="legendonly", showlegend=True,
                            hoverinfo="skip"))
    axis = {"range": [-3, 3], "nticks": 5}
    fig.update_layout(scene={"xaxis": axis, "yaxis": axis, "zaxis": axis,
                             "aspectmode": "cube", "camera": {"eye": {"x": 1.5, "y": 1.5, "z": 1.1}}},
                      margin={"l": 0, "r": 0, "t": 15, "b": 0},
                      legend={"orientation": "h", "y": 1.03, "x": 0},
                      font={"family": "Arial, sans-serif", "color": INK}, height=540)
    plot = fig.to_html(full_html=False, include_plotlyjs=True,
                       div_id="dual-contouring-sphere", config={"responsive": True, "displaylogo": False})
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dual Contouring: Sphere Mesh</title>
<style>body{{margin:0;padding:16px;font:15px/1.5 Arial,sans-serif;color:{INK};background:#fff}}
h1{{font-size:21px;margin:0 0 6px}}p{{margin:0 0 8px}}*{{box-sizing:border-box}}</style></head>
<body><h1>A sphere, one vertex per active cell</h1>
<p>{len(mesh.vertices)} vertices · {len(mesh.faces)} quads · {len(triangles)} display triangles.
Drag to rotate; scroll to zoom. Click legend labels to show the vertices or exact sphere.</p>
{plot}</body></html>'''
    (HERE / "sphere_mesh.html").write_text(html)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    if args.preview_dir:
        args.preview_dir.mkdir(parents=True, exist_ok=True)
    grid = np.arange(-3., 4.)
    circle = contour(sphere_field, sphere_gradient, grid, 2)
    sphere = contour(sphere_field, sphere_gradient, grid, 3)
    figures = [("corner_fit", corner_figure()), ("circle_pipeline", circle_figure(circle)),
               ("edge_to_quad", edge_figure()), ("sphere_mesh", sphere_figure(sphere))]
    for name, fig in figures:
        fig.savefig(IMAGE_DIR / f"{name}.svg", bbox_inches="tight", metadata={"Date": None})
        if args.preview_dir:
            fig.savefig(args.preview_dir / f"{name}.png", bbox_inches="tight", dpi=150)
        plt.close(fig)
        print(IMAGE_DIR / f"{name}.svg")
    write_interactive(sphere)
    print(HERE / "sphere_mesh.html")


if __name__ == "__main__":
    main()
