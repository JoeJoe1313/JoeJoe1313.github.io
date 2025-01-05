import numpy as np
import plotly.graph_objects as go

# Define constants
L = np.pi * np.sqrt(5)
a = 2 / 3
tmax = 30
x = np.linspace(0, L, 501)
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


# Generate data for each t value
data = [fourier_u(x, ti) for ti in t]

# Create initial plot
initial_y = data[0]
fig = go.Figure()

# Add trace for initial plot
fig.add_trace(
    go.Scatter(
        x=x,
        y=initial_y,
        mode="lines",
        line=dict(color="red", width=2),
        showlegend=False,
    )
)
fig.add_trace(
    go.Scatter(
        x=[0],
        y=[0],
        mode="markers",
        marker=dict(color="black", size=10),
        showlegend=False,
    )
)
fig.add_trace(
    go.Scatter(
        x=[L],
        y=[0],
        mode="markers",
        marker=dict(color="black", size=10),
        showlegend=False,
    )
)


# Add a slider to control t
steps = []
for i, ti in enumerate(t):
    step = dict(
        method="update",
        args=[
            {"y": [data[i]]},
            # {"title": f"String Vibration at t = {int(ti)}"},
        ],
        label=f"{ti:.1f}",
    )
    steps.append(step)

sliders = [dict(active=0, currentvalue={"prefix": "t = "}, steps=steps)]
# Update layout with slider
fig.update_layout(
    # title="String Vibration with Interactive Slider",
    xaxis=dict(title="x", range=[0, L]),
    yaxis=dict(title="u(x, t)", range=[-1, 1]),
    sliders=sliders,
    # width=800,
    # autosize=True,
    margin=dict(l=10, r=30, t=50, b=50),
)

# Save to HTML
config = {
    "displayModeBar": True,  # Show the toolbar
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],  # Remove unused buttons
    "displaylogo": False,
    "toImageButtonOptions": {"height": 500, "width": 800},  # Image export size
}
fig.write_html(
    "content/code/2025-01-04-fourier-method-fixed-string/string_vibration_slider.html",
    config=config,
)
print("Done")
