import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.optimize import root_scalar
from scipy.special import jv as besselj


def CircularMembrane(a=0.5, r=3, tmax=30, N=40):
    rho = np.linspace(0, r, 51)  # Radial grid points
    phi = np.linspace(0, 2 * np.pi, 51)  # Angular grid points
    t = np.linspace(0, tmax, 100)  # Time steps

    # Find the first 40 positive zeros of the Bessel function J0
    mju = []
    for n in range(1, N + 1):
        zero = root_scalar(
            lambda x: besselj(0, x), bracket=[(n - 1) * np.pi, n * np.pi]
        )
        mju.append(zero.root)
    mju = np.array(mju)

    # Define the initial position function
    def tau(rho):
        return rho**2 * np.sin(np.pi * rho) ** 3

    # Compute the solution for given R and t
    def solution(R, t):
        y = np.zeros_like(R)
        for m in range(N):
            s = tau(R[0, :]) * R[0, :] * besselj(0, mju[m] * R[0, :] / r)
            A0m = 4 * np.trapezoid(s, R[0, :]) / ((r**2) * (besselj(1, mju[m]) ** 2))
            y += A0m * np.cos(a * mju[m] * t / r) * besselj(0, mju[m] * R / r)
        return y

    # Create a grid of points
    R, p = np.meshgrid(rho, phi)
    X = R * np.cos(p)
    Y = R * np.sin(p)

    # Set up the figure and axis for animation
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(-r, r)
    ax.set_ylim(-r, r)
    ax.set_zlim(-30, 30)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("u(x,y,t)")
    ax.set_title("Circular Membrane")

    # Update function for animation
    def update(frame):
        ax.clear()
        Z = solution(R, frame)
        ax.plot_surface(X, Y, Z, cmap="viridis", vmin=-30, vmax=30)
        ax.set_xlim(-r, r)
        ax.set_ylim(-r, r)
        ax.set_zlim(-30, 30)
        ax.set_title("Circular Membrane")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("u(x,y,t)")

    # Create and save the animation
    anim = FuncAnimation(fig, update, frames=t, interval=50)
    anim.save("circular_membrane_animation.gif", writer="imagemagick", fps=20)

    plt.show()
