"""Draw the original figures for the Visual Calculus article.

Requires numpy and matplotlib. Run from any directory:
    python content/code/2026-10-09-visual-calculus/visual_calculus_figures.py

Use --preview-dir /tmp/visual-calculus-preview to also save PNG previews.
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle


BLUE = "#2376ad"
GREEN = "#25856b"
ORANGE = "#d38b32"
INK = "#233548"
MUTED = "#697b8a"
PALE = "#edf1f6"
SLUG = "2026-10-09-visual-calculus"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "text.color": INK,
    "axes.labelcolor": INK,
    "axes.titleweight": "semibold",
    "axes.titlesize": 14,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "svg.hashsalt": "visual-calculus",
    "savefig.facecolor": "white",
})


def axes_style(ax, title):
    ax.set_title(title, pad=18)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("bottom", "left"):
        ax.spines[side].set_color("#bbc6cf")
    ax.tick_params(length=3, pad=7)
    ax.set_axisbelow(True)


def caption(ax, text):
    ax.text(0.5, -0.22, text, transform=ax.transAxes, ha="center", va="top")


def subtangent():
    fig, ax = plt.subplots(figsize=(7.2, 4.6), layout="constrained")
    x = np.linspace(0, 1.94, 400)
    p = 1.7
    q = p / 2
    y = p**2
    ax.add_patch(Polygon([(q, 0), (p, 0), (p, y)], color=BLUE, alpha=0.10))
    ax.plot(x, x**2, color=BLUE, lw=2.7)
    t = np.linspace(q, 1.93, 100)
    ax.plot(t, 2 * p * (t - q), color=ORANGE, lw=2.2)
    ax.plot([p, p], [0, y], "--", color=MUTED, lw=1.2)
    ax.scatter([q, p], [0, y], color=INK, zorder=5, s=30)
    ax.annotate(r"$P=(x,f(x))$", (p, y), xytext=(-15, 20),
                textcoords="offset points", ha="right")
    ax.annotate(r"$Q$", (q, 0), xytext=(-13, 12), textcoords="offset points")
    ax.text(p + 0.045, y * 0.43, r"$f(x)$")
    ax.text(0.33, 1.45, r"$y=f(x)$", color=BLUE)
    ax.annotate("", (q, -0.43), (p, -0.43),
                arrowprops={"arrowstyle": "<->", "color": INK})
    ax.text((q + p) / 2, -0.57, r"$s(x)$", ha="center", va="top")
    ax.set_xticks([0, q, p], ["0", r"$x-s(x)$", r"$x$"])
    ax.set_yticks([])
    ax.spines["bottom"].set_position(("data", 0))
    ax.set(xlim=(0, 2.05), ylim=(-0.8, 4))
    axes_style(ax, "The subtangent is a horizontal projection")
    return fig


def exponential():
    fig, (left, right) = plt.subplots(
        1, 2, figsize=(11.4, 5.4), layout="constrained",
        gridspec_kw={"width_ratios": [4, 1]},
    )
    a, b = 1.0, 1.0
    height = np.exp(a / b)
    x = np.linspace(-4, a, 700)
    y = np.exp(x / b)
    terminal = np.maximum(0, height * (x - a + b) / b)
    left.fill_between(x, terminal, y, color=BLUE, alpha=0.23)
    left.fill_between(x, 0, terminal, color=ORANGE, alpha=0.28)
    left.plot(x, y, color=BLUE, lw=2.5)
    for t in np.linspace(-3, a, 13):
        left.plot([t - b, t], [0, np.exp(t / b)], color=BLUE, alpha=0.45, lw=1)
        right.plot([0, b], [0, np.exp(t / b)], color=GREEN, alpha=0.5, lw=1)
    left.plot([a - b, a], [0, height], color=ORANGE, lw=2)
    left.plot([a, a], [0, height], color=MUTED, lw=1)
    left.text(-2.5, 1.05, r"$y=e^{x/b}$", color=BLUE)
    right.add_patch(Polygon([(0, 0), (b, 0), (b, height)],
                            facecolor=GREEN, edgecolor=GREEN, alpha=0.20))
    right.plot([0, b, b], [0, height, 0], color=GREEN, lw=2)
    left.set(xlim=(-4.2, 1.35), ylim=(0, height * 1.14))
    right.set(xlim=(-0.12, 1.27), ylim=(0, height * 1.14))
    left.set_xticks([a - b, a], [r"$a-b$", r"$a$"])
    right.set_xticks([0, b], ["0", r"$b$"])
    for ax in (left, right):
        ax.set_yticks([0, height], ["0", r"$Y$"])
        ax.set_aspect("equal")
    axes_style(left, "Tangent sweep")
    axes_style(right, "Cluster")
    caption(left, r"Blue: $A-\frac{1}{2}bY$     Orange: $\frac{1}{2}bY$")
    caption(right, r"Green: $\frac{1}{2}bY$")
    return fig


def parabola():
    fig, (left, right) = plt.subplots(
        1, 2, figsize=(9.4, 5.5), layout="constrained",
        gridspec_kw={"width_ratios": [2, 1]},
    )
    a = 1.0
    height = a**2
    x = np.linspace(0, a, 500)
    terminal = np.maximum(0, 2 * a * (x - a / 2))
    left.fill_between(x, terminal, x**2, color=BLUE, alpha=0.23)
    left.fill_between(x, 0, terminal, color=ORANGE, alpha=0.28)
    left.plot(x, x**2, color=BLUE, lw=2.5)
    left.plot([a / 2, a], [0, height], color=ORANGE, lw=2)
    left.plot([a, a], [0, height], color=MUTED, lw=1)
    q = np.linspace(0, a / 2, 500)
    compressed = (2 * q)**2
    top = height * q / (a / 2)
    right.fill_between(q, 0, compressed, color=PALE)
    right.fill_between(q, compressed, top, color=GREEN, alpha=0.23)
    right.plot(q, compressed, color=BLUE, lw=2.5)
    right.plot(q, top, color=GREEN, lw=2)
    right.plot([a / 2, a / 2], [0, height], color=MUTED, lw=1)
    for t in np.linspace(0.2, a, 12):
        left.plot([t / 2, t], [0, t**2], color=BLUE, alpha=0.45, lw=1)
        right.plot([0, t / 2], [0, t**2], color=GREEN, alpha=0.5, lw=1)
    left.text(0.08, 0.8, r"$y=x^2$", color=BLUE)
    right.text(0.03, 0.84, r"$y=(2q)^2$", color=BLUE)
    right.text(0.39, 0.19, r"$A/2$", color=MUTED, ha="center")
    left.set(xlim=(0, a * 1.1), ylim=(0, height * 1.15))
    right.set(xlim=(0, a * 0.55), ylim=(0, height * 1.15))
    left.set_xticks([0, a / 2, a], ["0", r"$a/2$", r"$a$"])
    right.set_xticks([0, a / 2], ["0", r"$a/2$"])
    for ax in (left, right):
        ax.set_yticks([0, height], ["0", r"$Y$"])
        ax.set_aspect("equal")
    axes_style(left, "Tangent sweep")
    axes_style(right, "Translated cluster")
    caption(left, r"Blue: $A-\frac{aY}{4}$     Orange: $\frac{aY}{4}$")
    caption(right, r"Green: $\frac{aY}{4}-\frac{A}{2}$")
    return fig


def cycloid():
    fig, (left, right) = plt.subplots(
        1, 2, figsize=(11.6, 4.4), layout="constrained",
        gridspec_kw={"width_ratios": [2.65, 1]},
    )
    theta = np.linspace(0, 2 * np.pi, 801)
    x, y = theta - np.sin(theta), 1 - np.cos(theta)
    left.add_patch(Rectangle((0, 0), 2 * np.pi, 2, fill=False, ec=MUTED, lw=1))
    left.fill_between(x, y, 2, color=BLUE, alpha=0.22)
    left.plot(x, y, color=BLUE, lw=2.5)
    right.add_patch(Circle((0, -1), 1, facecolor=GREEN, edgecolor=GREEN, alpha=0.20))
    right.plot(np.cos(theta), -1 + np.sin(theta), color=GREEN, lw=2)
    for t in np.linspace(0, 2 * np.pi, 29):
        px, py = t - np.sin(t), 1 - np.cos(t)
        left.plot([px, t], [py, 2], color=BLUE, alpha=0.45, lw=1)
        right.plot([0, -np.sin(t)], [0, -1 - np.cos(t)], color=GREEN, alpha=0.5, lw=1)
    t = 2.0
    px, py = t - np.sin(t), 1 - np.cos(t)
    left.add_patch(Circle((t, 1), 1, fill=False, ec=ORANGE, lw=1.5, ls="--"))
    left.plot([t, px, t, t], [0, py, 2, 0], color=ORANGE, lw=1.5)
    left.scatter([t, px, t], [0, py, 2], s=18, color=INK, zorder=5)
    for name, xy, offset in [("B", (t, 0), (5, 9)), ("P", (px, py), (-18, -2)),
                             ("Q", (t, 2), (0, 11))]:
        left.annotate(name, xy, xytext=offset, textcoords="offset points", ha="center")
    right.scatter([0], [0], color=INK, s=24, zorder=5)
    right.annotate("O", (0, 0), xytext=(0, 11), textcoords="offset points", ha="center")
    left.text(4.4, 0.6, r"$3\pi r^2$", ha="center", fontsize=16)
    left.set(xlim=(-0.15, 2 * np.pi + 0.15), ylim=(-0.08, 2.42))
    right.set(xlim=(-1.18, 1.18), ylim=(-2.08, 0.42))
    for ax in (left, right):
        ax.set_aspect("equal")
    left.set_xticks([0, 2 * np.pi], ["0", r"$2\pi r$"])
    left.set_yticks([0, 2], ["0", r"$2r$"])
    right.set_xticks([])
    right.set_yticks([])
    axes_style(left, "Tangent chords above the arch")
    axes_style(right, "The cluster is one disk")
    for spine in right.spines.values():
        spine.set_visible(False)
    caption(left, r"Rectangle: $4\pi r^2$     Blue sweep: $\pi r^2$")
    caption(right, r"Green cluster: $\pi r^2$")
    return fig


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[2] / "images" / SLUG)
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.preview_dir:
        args.preview_dir.mkdir(parents=True, exist_ok=True)
    for name, draw in [("subtangent", subtangent), ("exponential", exponential),
                       ("parabola", parabola), ("cycloid", cycloid)]:
        fig = draw()
        destination = args.output_dir / f"{name}.svg"
        fig.savefig(destination, bbox_inches="tight", metadata={"Date": None})
        if args.preview_dir:
            fig.savefig(args.preview_dir / f"{name}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(destination)


if __name__ == "__main__":
    main()
