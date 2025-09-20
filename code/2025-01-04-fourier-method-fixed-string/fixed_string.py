import numpy as np
import pandas as pd
import plotly.express as px

# Define constants
L = np.pi * np.sqrt(5)
a = 2 / 3
tmax = 30
x = np.linspace(0, L, 101)
t = np.linspace(0, tmax, 31)  # Fewer points for smoother interaction


# Define the initial condition phi(x)
def phi(x):
    y = np.zeros_like(x)
    y[(1 < x) & (x < 3)] = np.sin(np.pi * x[(1 < x) & (x < 3)]) ** 3
    return y


# Define the initial velocity psi(x)
def psi(x):
    return np.zeros_like(x)


# Define the Fourier solution for u(x, t)
def fourier_u(x, t):
    y = np.zeros_like(x)
    for k in range(1, 101):
        Xk = np.sin(k * np.pi * x / L)
        Ak = (2 / L) * np.trapezoid(phi(x) * Xk, x)
        Bk = (2 / (a * k * np.pi)) * np.trapezoid(psi(x) * Xk, x)
        Tk = Ak * np.cos(a * k * np.pi * t / L) + Bk * np.sin(a * k * np.pi * t / L)
        y += Tk * Xk
    return y


# Create animation data
data = []
for t_val in t:
    y = fourier_u(x, t_val)
    for x_val, y_val in zip(x, y):
        data.append({"x": x_val, "y": y_val, "t": f"t = {t_val:.2f}"})

# Create DataFrame and plot
df = pd.DataFrame(data)
fig = px.line(
    df,
    x="x",
    y="y",
    animation_frame="t",
    # title="String Motion",
    labels={"x": "x", "y": "u(x, t)"},
    range_x=[-0.06, L + 0.06],
    range_y=[-1.1, 1.1],
    color_discrete_sequence=["red"],
)

# Add fixed points as black dots
fixed_points = pd.DataFrame(
    {
        "x": [0, L],
        "y": [0, 0],
    }
)

fig.add_scatter(
    x=fixed_points["x"],
    y=fixed_points["y"],
    mode="markers",
    marker=dict(color="black", size=10),
    showlegend=False,
)

fig.update_layout(
    showlegend=False,
    height=280,
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
            "currentvalue": {"font": {"size": 16}, "visible": True, "xanchor": "right"},
            "transition": {"duration": 500, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 1,
            "x": 0,
            "y": 0,
            "steps": [
                {
                    "args": [
                        [f"t = {t:.2f}"],
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
                    "label": f"{t:.0f}",
                    "method": "animate",
                }
                for t in t
            ],
        }
    ],
)

config = {
    "displayModeBar": True,  # Show the toolbar
    # "modeBarButtonsToRemove": ["lasso2d", "select2d"],  # Remove unused buttons
    "displaylogo": False,
    "toImageButtonOptions": {"height": 500, "width": 800},  # Image export size
}
fig.write_html(
    "content/code/2025-01-04-fourier-method-fixed-string/fixed_string_animation.html",
    include_plotlyjs=True,
    full_html=True,
    auto_play=False,
    config=config,
)
