"""
Minimal PINN for the 1D Wave Equation: Fixed String.

The simplest possible approach inspired by okada39/pinn_wave:
  - Small hourglass MLP (1,473 params)
  - L-BFGS only (no Adam)
  - Hard Dirichlet BCs
  - No Fourier features, no causal weighting, no time decomposition
  - Single network over the full [0, 30] domain
"""

import numpy as np
import torch
import torch.nn as nn
import pandas as pd
import plotly.express as px
import wandb

torch.manual_seed(42)
np.random.seed(42)

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# ── problem constants ────────────────────────────────────────────────
L = np.pi * np.sqrt(5)
a = 2.0 / 3.0
T_MAX = 4.0

N_INTERIOR = 10_000
N_IC = 500
LBFGS_ITERS = 2_000
IC_WEIGHT = 20.0


def phi(x: np.ndarray) -> np.ndarray:
    y = np.zeros_like(x)
    mask = (x > 1) & (x < 3)
    y[mask] = np.sin(np.pi * x[mask]) ** 3
    return y


# ── network: 2 → 64 → 32 → 32 → 64 → 1 (~5,505 params) ────────────
class PINN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 64),  nn.Tanh(),
            nn.Linear(64, 32), nn.Tanh(),
            nn.Linear(32, 32), nn.Tanh(),
            nn.Linear(32, 64), nn.Tanh(),
            nn.Linear(64, 1),
        )
        self.register_buffer("x_mean", torch.tensor(L / 2.0, dtype=torch.float32))
        self.register_buffer("x_std", torch.tensor(L / 2.0, dtype=torch.float32))
        self.register_buffer("t_mean", torch.tensor(T_MAX / 2.0, dtype=torch.float32))
        self.register_buffer("t_std", torch.tensor(T_MAX / 2.0, dtype=torch.float32))

    def forward(self, x, t):
        x_n = (x - self.x_mean) / self.x_std
        t_n = (t - self.t_mean) / self.t_std
        raw = self.net(torch.cat([x_n, t_n], dim=1))
        return x * (L - x) * raw


def pde_residual(model, x, t):
    x = x.requires_grad_(True)
    t = t.requires_grad_(True)
    u = model(x, t)
    u_x = torch.autograd.grad(u, x, torch.ones_like(u), create_graph=True)[0]
    u_t = torch.autograd.grad(u, t, torch.ones_like(u), create_graph=True)[0]
    u_xx = torch.autograd.grad(u_x, x, torch.ones_like(u_x), create_graph=True)[0]
    u_tt = torch.autograd.grad(u_t, t, torch.ones_like(u_t), create_graph=True)[0]
    return u_tt - a ** 2 * u_xx


def fourier_u(x_np, t_val, n_terms=100):
    y = np.zeros_like(x_np)
    phi_x = phi(x_np)
    for k in range(1, n_terms + 1):
        Xk = np.sin(k * np.pi * x_np / L)
        Ak = (2 / L) * np.trapezoid(phi_x * Xk, x_np)
        y += Ak * np.cos(a * k * np.pi * t_val / L) * Xk
    return y


# ── L-BFGS training ─────────────────────────────────────────────────
def train(model):
    # L-BFGS needs CPU (no MPS support)
    was_mps = next(model.parameters()).device.type == "mps"
    if was_mps:
        model = model.to("cpu")
    dev = next(model.parameters()).device

    # fixed collocation points
    torch.manual_seed(0)
    x_int = torch.rand(N_INTERIOR, 1, device=dev) * L
    t_int = torch.rand(N_INTERIOR, 1, device=dev) * T_MAX
    x_ic = torch.linspace(0, L, N_IC, device=dev).unsqueeze(1)
    t_ic = torch.zeros(N_IC, 1, device=dev)
    phi_vals = torch.tensor(phi(x_ic.cpu().numpy()), dtype=torch.float32, device=dev)

    optimizer = torch.optim.LBFGS(
        model.parameters(), lr=1.0, max_iter=20, history_size=50,
        line_search_fn="strong_wolfe",
    )

    step = [0]
    def closure():
        optimizer.zero_grad()

        r = pde_residual(model, x_int.clone(), t_int.clone())
        loss_pde = torch.mean(r ** 2)

        u_pred = model(x_ic, t_ic)
        loss_ic_u = torch.mean((u_pred - phi_vals) ** 2)

        x_v = x_ic.detach().clone().requires_grad_(True)
        t_v = torch.zeros_like(x_v, requires_grad=True)
        u_v = model(x_v, t_v)
        u_t_v = torch.autograd.grad(u_v, t_v, torch.ones_like(u_v), create_graph=True)[0]
        loss_ic_v = torch.mean(u_t_v ** 2)

        loss = loss_pde + IC_WEIGHT * loss_ic_u + IC_WEIGHT * loss_ic_v
        loss.backward()

        step[0] += 1
        if step[0] % 500 == 0 or step[0] == 1:
            print(
                f"step {step[0]:>6d} | loss {loss.item():.3e} | "
                f"pde {loss_pde.item():.3e} | "
                f"ic_u {loss_ic_u.item():.3e} | "
                f"ic_v {loss_ic_v.item():.3e}"
            )
            wandb.log({
                "loss": loss.item(), "pde": loss_pde.item(),
                "ic_u": loss_ic_u.item(), "ic_v": loss_ic_v.item(),
                "step": step[0],
            })
        return loss

    for _ in range(LBFGS_ITERS):
        optimizer.step(closure)

    if was_mps:
        model = model.to("mps")
    return model


# ── evaluation & animation ──────────────────────────────────────────
@torch.no_grad()
def evaluate(model, x_np, t_vals):
    dev = next(model.parameters()).device
    results = []
    for t_val in t_vals:
        x_t = torch.tensor(x_np, dtype=torch.float32, device=dev).unsqueeze(1)
        t_t = torch.full_like(x_t, t_val)
        u_pred = model(x_t, t_t).cpu().numpy().flatten()
        u_ref = fourier_u(x_np, t_val)
        for xi, ui, ur in zip(x_np, u_pred, u_ref):
            results.append({"x": xi, "u_pinn": ui, "u_fourier": ur, "t": f"t = {t_val:.2f}"})
    return pd.DataFrame(results)


def create_animation(df, out_path):
    fig = px.line(
        df, x="x", y="u_pinn", animation_frame="t",
        labels={"x": "x", "u_pinn": "u(x, t)"},
        range_x=[-0.06, L + 0.06], range_y=[-1.1, 1.1],
        color_discrete_sequence=["#2563eb"],
    )
    fig.data[0].name = "PINN"
    fig.data[0].showlegend = True

    t0_label = df["t"].unique()[0]
    df_t0 = df[df["t"] == t0_label]
    fig.add_scatter(
        x=df_t0["x"], y=df_t0["u_fourier"],
        mode="lines", line=dict(color="red", dash="dash"),
        name="Fourier (100 terms)", showlegend=True,
    )
    for frame in fig.frames:
        t_label = frame.name
        df_t = df[df["t"] == t_label]
        fourier_trace = dict(
            type="scatter", x=df_t["x"].tolist(), y=df_t["u_fourier"].tolist(),
            mode="lines", line=dict(color="red", dash="dash"),
            name="Fourier (100 terms)", showlegend=True,
        )
        frame.data = (*frame.data, fourier_trace)

    fig.add_scatter(
        x=[0, L], y=[0, 0], mode="markers",
        marker=dict(color="black", size=10), showlegend=False,
    )
    t_vals = df["t"].unique()
    fig.update_layout(
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.7)"),
        height=350, margin=dict(l=10, r=30, t=30, b=10),
        updatemenus=[{
            "buttons": [
                {"args": [None, {"frame": {"duration": 200, "redraw": True},
                                  "fromcurrent": True, "mode": "immediate",
                                  "transition": {"duration": 0}}],
                 "label": "Play", "method": "animate"},
                {"args": [[None], {"frame": {"duration": 0, "redraw": True},
                                    "mode": "immediate", "transition": {"duration": 0}}],
                 "label": "Pause", "method": "animate"},
            ],
            "type": "buttons", "direction": "left", "showactive": True,
            "x": 0.2, "y": 0.3, "xanchor": "right", "yanchor": "top",
        }],
        sliders=[{
            "active": 0, "yanchor": "top", "xanchor": "left",
            "currentvalue": {"font": {"size": 16}, "visible": True, "xanchor": "right"},
            "transition": {"duration": 500, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50}, "len": 1, "x": 0, "y": 0,
            "steps": [
                {"args": [[tl], {"frame": {"duration": 500, "redraw": True},
                                  "mode": "immediate", "transition": {"duration": 0}}],
                 "label": tl.split("= ")[1], "method": "animate"}
                for tl in t_vals
            ],
        }],
    )
    fig.write_html(out_path, include_plotlyjs=True, full_html=True,
                   auto_play=False, config={"displayModeBar": True, "displaylogo": False})
    print(f"Animation saved to {out_path}")


if __name__ == "__main__":
    wandb.init(project="pinn-wave-equation", name="minimal-lbfgs", config={
        "method": "minimal (okada39-style)",
        "architecture": "2→32→16→16→32→1",
        "n_params": 1473,
        "lbfgs_iters": LBFGS_ITERS,
        "n_interior": N_INTERIOR, "n_ic": N_IC, "ic_weight": IC_WEIGHT,
        "L": L, "a": a, "T_max": T_MAX,
    })

    print(f"Device: {device}")
    print(f"L = {L:.4f}, a = {a:.4f}, T_max = {T_MAX}")
    print(f"1,473 params, {LBFGS_ITERS} L-BFGS iters, no decomposition")
    print()

    model = PINN().to(device)
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")

    model = train(model)

    x_eval = np.linspace(0, L, 101)
    t_eval = np.linspace(0, T_MAX, 31)
    df = evaluate(model, x_eval, t_eval)

    mae = np.mean(np.abs(df["u_pinn"] - df["u_fourier"]))
    max_err = np.max(np.abs(df["u_pinn"] - df["u_fourier"]))
    print(f"\nComparison with Fourier (100-term) reference:")
    print(f"  Mean Absolute Error : {mae:.6f}")
    print(f"  Max  Absolute Error : {max_err:.6f}")
    wandb.log({"eval/mae": mae, "eval/max_error": max_err})

    anim_path = "content/code/2025-01-04-fourier-method-fixed-string/fixed_string_pinn_minimal_animation.html"
    create_animation(df, anim_path)
    artifact = wandb.Artifact("pinn-minimal-animation", type="result")
    artifact.add_file(anim_path)
    wandb.log_artifact(artifact)
    wandb.finish()
