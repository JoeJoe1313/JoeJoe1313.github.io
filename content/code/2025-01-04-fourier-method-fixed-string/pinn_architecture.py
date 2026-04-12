"""Generate a clean architecture diagram for the PINN network."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(14, 5))
ax.set_xlim(-0.5, 14)
ax.set_ylim(-1.5, 4)
ax.axis("off")

# ── colour palette ───────────────────────────────────────────────────
C = {
    "input": ("#e8f4fd", "#4a9eda"),
    "norm": ("#fef9e7", "#d4ac0d"),
    "fourier": ("#f5eef8", "#8e44ad"),
    "hidden": ("#eaf7ea", "#27ae60"),
    "bc": ("#fdecea", "#e74c3c"),
    "output": ("#e8f4fd", "#2563eb"),
    "loss": ("#fff3e0", "#e67e22"),
}


def box(x, y, w, h, label_lines, colors, fontsize=10, title=None):
    """Draw a rounded box with centered multi-line text."""
    face, edge = colors
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.1",
        facecolor=face, edgecolor=edge, linewidth=1.5,
    )
    ax.add_patch(rect)
    n = len(label_lines)
    if title:
        ax.text(
            x + w / 2, y + h - 0.2, title,
            ha="center", va="top", fontsize=7,
            color=edge, fontweight="bold", family="monospace",
            fontstyle="italic",
        )
        offset = 0.35
    else:
        offset = 0.1
    for i, line in enumerate(label_lines):
        ty = y + h - offset - (i + 1) * (h - offset - 0.1) / (n + 0.5)
        ax.text(x + w / 2, ty, line, ha="center", va="center", fontsize=fontsize)
    return x + w  # right edge


def arrow(x1, y, x2, color="#444"):
    ax.annotate(
        "", xy=(x2, y), xytext=(x1, y),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4),
    )


# ── y positions ──────────────────────────────────────────────────────
mid = 1.8  # vertical center of the main pipeline

# ── INPUT ────────────────────────────────────────────────────────────
x = 0
r = box(x, mid - 0.6, 1.0, 1.2, ["Input", r"$(x,\, t)$", "2D"], C["input"], fontsize=11)
arrow(r, mid, r + 0.25)

# ── NORMALISE ────────────────────────────────────────────────────────
x = r + 0.3
r = box(x, mid - 0.5, 1.3, 1.0,
        ["Normalise", r"$x \to [-1,1]$", r"$t \to [-1,1]$"],
        C["norm"], fontsize=9)
arrow(r, mid, r + 0.25)

# ── FOURIER FEATURES ─────────────────────────────────────────────────
x = r + 0.3
r = box(x, mid - 0.65, 1.8, 1.3,
        [r"$\sin(\mathbf{B}\mathbf{z}),\;\cos(\mathbf{B}\mathbf{z})$",
         r"$\mathbf{B} \in \mathbb{R}^{2\times32}$ (learnable)",
         r"$\longrightarrow$ 64D"],
        C["fourier"], fontsize=9, title="FOURIER FEATURES")
arrow(r, mid, r + 0.25)

# ── HIDDEN LAYERS ────────────────────────────────────────────────────
x = r + 0.3
layer_w = 0.5
gap = 0.12
for i in range(4):
    r = box(x, mid - 0.75, layer_w, 1.5, ["128", "Tanh"], C["hidden"], fontsize=9)
    x = r + gap
    if i < 3:
        arrow(r, mid, r + gap, color="#27ae60")

# final layer (128 → 1)
r = box(x, mid - 0.45, layer_w, 0.9, ["128→1"], C["hidden"], fontsize=9)

# brace label
ax.text(
    (r + 0.3 + 4 * (layer_w + gap)) / 2 + 2.1, mid + 1.15,
    "MLP · 5 hidden layers · 74,561 parameters",
    ha="center", va="center", fontsize=8.5,
    color=C["hidden"][1], family="monospace", fontstyle="italic",
)
arrow(r, mid, r + 0.25)

# ── HARD BC (multiply) ───────────────────────────────────────────────
x = r + 0.3
r = box(x, mid - 0.75, 1.1, 1.5,
        [r"$x(L - x)$", r"$\times$", r"$u(0,t)=0$", r"$u(L,t)=0$"],
        C["bc"], fontsize=9, title="HARD BC")
arrow(r, mid, r + 0.25)

# ── OUTPUT ───────────────────────────────────────────────────────────
x = r + 0.3
r = box(x, mid - 0.4, 0.8, 0.8,
        [r"$u_\theta$", r"$(x,t)$"],
        C["output"], fontsize=12)

# ── LOSS / AUTOGRAD (below) ──────────────────────────────────────────
# vertical arrow from output down
out_cx = x + 0.4
ax.annotate(
    "", xy=(out_cx, mid - 1.0), xytext=(out_cx, mid - 0.45),
    arrowprops=dict(arrowstyle="-|>", color=C["output"][1], lw=1.3),
)

# loss box
loss_x = 5.5
loss_w = 7.5
box(loss_x, -1.4, loss_w, 1.0,
    [r"$\mathcal{L} = \|u_{tt} - a^2 u_{xx}\|^2 \;+\; \lambda_{\mathrm{IC}}\,\mathcal{L}_{\mathrm{IC}}$",
     "PDE residual + initial conditions → backprop"],
    C["loss"], fontsize=10, title="AUTOMATIC DIFFERENTIATION")

# dashed feedback arrow
ax.annotate(
    "", xy=(5.5, mid - 0.75), xytext=(5.5, -0.45),
    arrowprops=dict(
        arrowstyle="-|>", color=C["loss"][1], lw=1.2,
        linestyle="dashed",
    ),
)
ax.text(5.3, 0.5, r"$\nabla_\theta$", fontsize=11, color=C["loss"][1],
        ha="right", va="center")

plt.tight_layout()
plt.savefig(
    "content/images/2025-04-12-pinn-wave-equation-fixed-string/pinn_architecture.svg",
    format="svg", bbox_inches="tight", transparent=True,
)
plt.savefig(
    "content/images/2025-04-12-pinn-wave-equation-fixed-string/pinn_architecture.png",
    format="png", dpi=200, bbox_inches="tight", facecolor="white",
)
print("Saved pinn_architecture.svg and .png")
