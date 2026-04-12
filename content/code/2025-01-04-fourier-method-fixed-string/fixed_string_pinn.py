"""
Physics-Informed Neural Network (PINN) for the 1D Wave Equation: Fixed String.

Solves the same problem as the Fourier method:
    u_tt = (2/3)^2 * u_xx,      x in [0, pi*sqrt(5)], t in [0, 30]
    u(x, 0) = sin^3(pi*x)       for x in [1, 3], 0 otherwise
    u_t(x, 0) = 0
    u(0, t) = u(pi*sqrt(5), t) = 0

Key design choices:
    - Hard-encoded Dirichlet BCs via u = x*(L-x) * net(x, t)
    - Input normalisation to [-1, 1] for stable training
    - Fourier feature embedding to capture high-frequency wave modes
    - Causal training: exponential time-weighting so the network
      learns the near-initial dynamics first before propagating forward
    - Two-phase optimisation: Adam warm-up then L-BFGS refinement
"""

import numpy as np
import torch
import torch.nn as nn
import pandas as pd
import plotly.express as px
import wandb

# ── reproducibility ──────────────────────────────────────────────────
torch.manual_seed(42)
np.random.seed(42)

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# ── problem constants ────────────────────────────────────────────────
L = np.pi * np.sqrt(5)  # string length  ≈ 7.025
a = 2.0 / 3.0           # wave speed
T_MAX = 30.0             # maximum time


def phi(x: np.ndarray) -> np.ndarray:
    """Initial displacement: sin^3(pi*x) on [1, 3], 0 elsewhere."""
    y = np.zeros_like(x)
    mask = (x > 1) & (x < 3)
    y[mask] = np.sin(np.pi * x[mask]) ** 3
    return y


# ── network architecture ────────────────────────────────────────────
class FourierFeatures(nn.Module):
    """Learnable Fourier feature embedding for the 2D input (x, t).

    Maps each input component through sin/cos at multiple frequencies,
    giving the network a head-start on representing oscillatory solutions.
    """

    def __init__(self, n_freq: int = 32, input_dim: int = 2):
        super().__init__()
        # frequencies are learnable so the network can adapt them
        self.B = nn.Parameter(torch.randn(input_dim, n_freq) * 2.0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        proj = x @ self.B                     # (N, n_freq)
        return torch.cat([torch.sin(proj), torch.cos(proj)], dim=1)  # (N, 2*n_freq)


class PINN(nn.Module):
    """Fully connected network with Fourier features and hard BCs.

    Architecture:
        (x, t) ──normalise──► Fourier embedding ──► MLP ──► raw
        output  =  x * (L - x) * raw     (hard Dirichlet BCs)
    """

    def __init__(self, hidden_dim: int = 128, n_hidden: int = 5, n_freq: int = 32):
        super().__init__()
        self.fourier = FourierFeatures(n_freq=n_freq, input_dim=2)
        embed_dim = 2 * n_freq

        layers = [nn.Linear(embed_dim, hidden_dim), nn.Tanh()]
        for _ in range(n_hidden - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), nn.Tanh()]
        layers.append(nn.Linear(hidden_dim, 1))
        self.net = nn.Sequential(*layers)

        # normalisation constants (registered as buffers, not parameters)
        self.register_buffer("x_mean", torch.tensor(L / 2.0, dtype=torch.float32))
        self.register_buffer("x_std", torch.tensor(L / 2.0, dtype=torch.float32))
        self.register_buffer("t_mean", torch.tensor(T_MAX / 2.0, dtype=torch.float32))
        self.register_buffer("t_std", torch.tensor(T_MAX / 2.0, dtype=torch.float32))

    def forward(self, x: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        # normalise inputs to roughly [-1, 1]
        x_n = (x - self.x_mean) / self.x_std
        t_n = (t - self.t_mean) / self.t_std
        inp = torch.cat([x_n, t_n], dim=1)
        raw = self.net(self.fourier(inp))
        # hard Dirichlet BCs: vanishes at x=0 and x=L
        return x * (L - x) * raw


# ── PDE residual via automatic differentiation ──────────────────────
def pde_residual(model: PINN, x: torch.Tensor, t: torch.Tensor):
    """Compute r = u_tt - a^2 * u_xx (should be ≈ 0)."""
    x = x.requires_grad_(True)
    t = t.requires_grad_(True)
    u = model(x, t)

    # first-order
    u_x = torch.autograd.grad(u, x, torch.ones_like(u), create_graph=True)[0]
    u_t = torch.autograd.grad(u, t, torch.ones_like(u), create_graph=True)[0]

    # second-order
    u_xx = torch.autograd.grad(u_x, x, torch.ones_like(u_x), create_graph=True)[0]
    u_tt = torch.autograd.grad(u_t, t, torch.ones_like(u_t), create_graph=True)[0]

    return u_tt - a ** 2 * u_xx


# ── collocation points ──────────────────────────────────────────────
N_INTERIOR = 20_000
N_IC = 1_000


def sample_points():
    """Random collocation points for each loss term."""
    x_int = torch.rand(N_INTERIOR, 1, device=device) * L
    t_int = torch.rand(N_INTERIOR, 1, device=device) * T_MAX

    x_ic = torch.rand(N_IC, 1, device=device) * L
    t_ic = torch.zeros(N_IC, 1, device=device)

    return x_int, t_int, x_ic, t_ic


# ── Fourier reference (for comparison only) ─────────────────────────
def fourier_u(x_np: np.ndarray, t_val: float, n_terms: int = 100) -> np.ndarray:
    """100-term Fourier partial sum (same as the original code)."""
    y = np.zeros_like(x_np)
    phi_x = phi(x_np)
    for k in range(1, n_terms + 1):
        Xk = np.sin(k * np.pi * x_np / L)
        Ak = (2 / L) * np.trapezoid(phi_x * Xk, x_np)
        Tk = Ak * np.cos(a * k * np.pi * t_val / L)
        y += Tk * Xk
    return y


# ── causal weighting helper ─────────────────────────────────────────
def causal_weights(t: torch.Tensor, epsilon: float = 1.0) -> torch.Tensor:
    """Exponential weight w(t) = exp(-t / epsilon).

    Points near t = 0 are weighted much more heavily, encouraging the
    network to learn the initial dynamics first.  As epsilon grows
    (scheduled during training), later times receive more weight.
    """
    return torch.exp(-t / epsilon)


# ── training ────────────────────────────────────────────────────────
def train(
    model: PINN,
    epochs: int = 30_000,
    lr: float = 1e-3,
    log_every: int = 2_000,
):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    # causal epsilon: start tight, relax over training
    eps_start, eps_end = 1.0, 50.0

    for epoch in range(1, epochs + 1):
        x_int, t_int, x_ic, t_ic = sample_points()

        # linearly increase causal epsilon
        frac = min(epoch / epochs, 1.0)
        epsilon = eps_start + frac * (eps_end - eps_start)

        # ── PDE loss (causally weighted) ─────────────────────────
        residual = pde_residual(model, x_int, t_int)
        weights = causal_weights(t_int.detach(), epsilon)
        loss_pde = torch.mean(weights * residual ** 2)

        # ── initial displacement loss ────────────────────────────
        u_ic_pred = model(x_ic, t_ic)
        phi_vals = torch.tensor(
            phi(x_ic.detach().cpu().numpy()), dtype=torch.float32, device=device
        )
        loss_ic_u = torch.mean((u_ic_pred - phi_vals) ** 2)

        # ── initial velocity loss  u_t(x, 0) = 0 ────────────────
        x_ic_v = x_ic.detach().clone().requires_grad_(True)
        t_ic_v = torch.zeros_like(x_ic_v, requires_grad=True)
        u_for_vel = model(x_ic_v, t_ic_v)
        u_t_ic = torch.autograd.grad(
            u_for_vel, t_ic_v, torch.ones_like(u_for_vel), create_graph=True
        )[0]
        loss_ic_v = torch.mean(u_t_ic ** 2)

        # ── total loss ───────────────────────────────────────────
        loss = loss_pde + 20.0 * loss_ic_u + 20.0 * loss_ic_v

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()

        # ── wandb logging ────────────────────────────────────────
        wandb.log({
            "adam/loss_total": loss.item(),
            "adam/loss_pde": loss_pde.item(),
            "adam/loss_ic_u": loss_ic_u.item(),
            "adam/loss_ic_v": loss_ic_v.item(),
            "adam/causal_epsilon": epsilon,
            "adam/lr": scheduler.get_last_lr()[0],
            "adam/epoch": epoch,
        })

        if epoch % log_every == 0 or epoch == 1:
            print(
                f"epoch {epoch:>6d} | "
                f"loss {loss.item():.3e} | "
                f"pde {loss_pde.item():.3e} | "
                f"ic_u {loss_ic_u.item():.3e} | "
                f"ic_v {loss_ic_v.item():.3e} | "
                f"eps {epsilon:.1f}"
            )

    return model


def lbfgs_finetune(model: PINN, steps: int = 500, log_every: int = 100):
    """L-BFGS refinement after Adam pre-training.

    L-BFGS uses full-batch second-order information and can push the
    loss significantly lower once Adam has found a good basin.
    Note: L-BFGS does not support MPS, so we move to CPU for this phase.
    """
    was_mps = next(model.parameters()).device.type == "mps"
    if was_mps:
        model = model.to("cpu")
        print("(L-BFGS phase runs on CPU)")

    dev = next(model.parameters()).device

    # fixed collocation set for L-BFGS (deterministic)
    torch.manual_seed(0)
    x_int = torch.rand(N_INTERIOR, 1, device=dev) * L
    t_int = torch.rand(N_INTERIOR, 1, device=dev) * T_MAX
    x_ic = torch.linspace(0, L, N_IC, device=dev).unsqueeze(1)
    t_ic = torch.zeros(N_IC, 1, device=dev)
    phi_vals = torch.tensor(phi(x_ic.cpu().numpy()), dtype=torch.float32, device=dev)

    optimizer = torch.optim.LBFGS(
        model.parameters(), lr=0.5, max_iter=20, history_size=50,
        line_search_fn="strong_wolfe",
    )

    for step in range(1, steps + 1):
        def closure():
            optimizer.zero_grad()
            r = pde_residual(model, x_int.clone(), t_int.clone())
            loss_pde = torch.mean(r ** 2)

            u_ic_pred = model(x_ic, t_ic)
            loss_ic_u = torch.mean((u_ic_pred - phi_vals) ** 2)

            x_v = x_ic.detach().clone().requires_grad_(True)
            t_v = torch.zeros_like(x_v, requires_grad=True)
            u_v = model(x_v, t_v)
            u_t_v = torch.autograd.grad(
                u_v, t_v, torch.ones_like(u_v), create_graph=True
            )[0]
            loss_ic_v = torch.mean(u_t_v ** 2)

            loss = loss_pde + 20.0 * loss_ic_u + 20.0 * loss_ic_v
            loss.backward()
            return loss

        loss = optimizer.step(closure)
        wandb.log({"lbfgs/loss_total": loss.item(), "lbfgs/step": step})
        if step % log_every == 0 or step == 1:
            print(f"L-BFGS step {step:>4d} | loss {loss.item():.3e}")

    if was_mps:
        model = model.to("mps")

    return model


# ── evaluation & animation ──────────────────────────────────────────
@torch.no_grad()
def evaluate(model: PINN, x_np: np.ndarray, t_vals: np.ndarray):
    """Evaluate the trained PINN on a grid of (x, t) values."""
    dev = next(model.parameters()).device
    results = []
    for t_val in t_vals:
        x_t = torch.tensor(x_np, dtype=torch.float32, device=dev).unsqueeze(1)
        t_t = torch.full_like(x_t, t_val)
        u_pred = model(x_t, t_t).cpu().numpy().flatten()
        u_ref = fourier_u(x_np, t_val)
        for xi, ui, ur in zip(x_np, u_pred, u_ref):
            results.append(
                {"x": xi, "u_pinn": ui, "u_fourier": ur, "t": f"t = {t_val:.2f}"}
            )
    return pd.DataFrame(results)


def create_animation(df: pd.DataFrame, out_path: str):
    """Build an interactive Plotly animation comparing PINN vs Fourier."""
    fig = px.line(
        df,
        x="x",
        y="u_pinn",
        animation_frame="t",
        labels={"x": "x", "u_pinn": "u(x, t)"},
        range_x=[-0.06, L + 0.06],
        range_y=[-1.1, 1.1],
        color_discrete_sequence=["#2563eb"],
    )
    fig.data[0].name = "PINN"
    fig.data[0].showlegend = True

    # Fourier reference (dashed red)
    t0_label = df["t"].unique()[0]
    df_t0 = df[df["t"] == t0_label]
    fig.add_scatter(
        x=df_t0["x"],
        y=df_t0["u_fourier"],
        mode="lines",
        line=dict(color="red", dash="dash"),
        name="Fourier (100 terms)",
        showlegend=True,
    )

    for frame in fig.frames:
        t_label = frame.name
        df_t = df[df["t"] == t_label]
        fourier_trace = dict(
            type="scatter",
            x=df_t["x"].tolist(),
            y=df_t["u_fourier"].tolist(),
            mode="lines",
            line=dict(color="red", dash="dash"),
            name="Fourier (100 terms)",
            showlegend=True,
        )
        frame.data = (*frame.data, fourier_trace)

    fig.add_scatter(
        x=[0, L], y=[0, 0],
        mode="markers",
        marker=dict(color="black", size=10),
        showlegend=False,
    )

    t_vals = df["t"].unique()
    fig.update_layout(
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.7)"),
        height=350,
        margin=dict(l=10, r=30, t=30, b=10),
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [
                            None,
                            {
                                "frame": {"duration": 200, "redraw": True},
                                "fromcurrent": True,
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                        "label": "Play",
                        "method": "animate",
                    },
                    {
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                        "label": "Pause",
                        "method": "animate",
                    },
                ],
                "type": "buttons",
                "direction": "left",
                "showactive": True,
                "x": 0.2,
                "y": 0.3,
                "xanchor": "right",
                "yanchor": "top",
            }
        ],
        sliders=[
            {
                "active": 0,
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 16},
                    "visible": True,
                    "xanchor": "right",
                },
                "transition": {"duration": 500, "easing": "cubic-in-out"},
                "pad": {"b": 10, "t": 50},
                "len": 1,
                "x": 0,
                "y": 0,
                "steps": [
                    {
                        "args": [
                            [t_label],
                            {
                                "frame": {
                                    "duration": 500,
                                    "easing": "cubic-in-out",
                                    "redraw": True,
                                },
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                        "label": t_label.split("= ")[1],
                        "method": "animate",
                    }
                    for t_label in t_vals
                ],
            }
        ],
    )

    config = {
        "displayModeBar": True,
        "displaylogo": False,
        "toImageButtonOptions": {"height": 500, "width": 800},
    }
    fig.write_html(out_path, include_plotlyjs=True, full_html=True, auto_play=False, config=config)
    print(f"Animation saved to {out_path}")


# ── main ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # ── wandb init ───────────────────────────────────────────────
    config = {
        "hidden_dim": 128,
        "n_hidden": 5,
        "n_freq": 32,
        "adam_epochs": 30_000,
        "adam_lr": 1e-3,
        "lbfgs_steps": 500,
        "n_interior": N_INTERIOR,
        "n_ic": N_IC,
        "ic_weight": 20.0,
        "causal_eps_start": 1.0,
        "causal_eps_end": 50.0,
        "L": L,
        "a": a,
        "T_max": T_MAX,
    }
    wandb.init(
        project="pinn-wave-equation",
        config=config,
        name="fixed-string-v2",
    )

    print(f"Device: {device}")
    print(f"String length L = {L:.4f}, wave speed a = {a:.4f}, T_max = {T_MAX}")

    model = PINN(
        hidden_dim=config["hidden_dim"],
        n_hidden=config["n_hidden"],
        n_freq=config["n_freq"],
    ).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Network parameters: {n_params:,}")
    wandb.config.update({"n_params": n_params, "device": str(device)})

    # Phase 1: Adam with causal weighting
    model = train(model, epochs=config["adam_epochs"], lr=config["adam_lr"], log_every=2_000)

    # Phase 2: L-BFGS fine-tuning
    model = lbfgs_finetune(model, steps=config["lbfgs_steps"], log_every=100)

    # evaluate
    x_eval = np.linspace(0, L, 101)
    t_eval = np.linspace(0, T_MAX, 31)
    df = evaluate(model, x_eval, t_eval)

    mae = np.mean(np.abs(df["u_pinn"] - df["u_fourier"]))
    max_err = np.max(np.abs(df["u_pinn"] - df["u_fourier"]))
    print(f"\nComparison with Fourier (100-term) reference:")
    print(f"  Mean Absolute Error : {mae:.6f}")
    print(f"  Max  Absolute Error : {max_err:.6f}")

    wandb.log({"eval/mae": mae, "eval/max_error": max_err})

    anim_path = "content/code/2025-01-04-fourier-method-fixed-string/fixed_string_pinn_animation.html"
    create_animation(df, anim_path)

    # log the animation HTML as a wandb artifact
    artifact = wandb.Artifact("pinn-animation", type="result")
    artifact.add_file(anim_path)
    wandb.log_artifact(artifact)

    wandb.finish()
