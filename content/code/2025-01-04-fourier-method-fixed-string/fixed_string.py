import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Define constants
L = np.pi * np.sqrt(5)
a = 2 / 3
tmax = 30
x = np.linspace(0, L, 501)
t = np.linspace(0, tmax, 31)


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


# Set up the figure for animation
fig, ax = plt.subplots(figsize=(16, 2))
ax.set_xlim(0, L)
ax.set_ylim(-1, 1)
ax.set_xlabel("x")
ax.set_ylabel("u(x, t)")
ax.set_title("String Vibration")
(line,) = ax.plot([], [], lw=2, color="r")
(marker_left,) = ax.plot([], [], "ko", markerfacecolor="k")
(marker_right,) = ax.plot([], [], "ko", markerfacecolor="k")


def init():
    line.set_data([], [])
    marker_left.set_data([], [])
    marker_right.set_data([], [])
    return line, marker_left, marker_right


def update(frame):
    y = fourier_u(x, frame)
    line.set_data(x, y)
    marker_left.set_data([0], [y[0]])
    marker_right.set_data([L], [y[-1]])
    return line, marker_left, marker_right


# Create the animation
anim = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True)
anim.save(
    "content/images/2025-01-04-fourier-method-fixed-string/string_vibration_animation.gif",
    writer="pillow",
    fps=20,
)

plt.show()
