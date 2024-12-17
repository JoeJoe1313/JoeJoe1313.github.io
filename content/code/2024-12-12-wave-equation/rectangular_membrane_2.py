import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def rectangular_membrane_2(a: float = 1, b: float = 2, c: float = np.pi, tmax: int = 6):
    t = np.linspace(0, tmax, 100)  # Time points for animation
    x = np.linspace(0, a, 50)  # x grid
    y = np.linspace(0, b, 50)  # y grid
    X, Y = np.meshgrid(x, y)

    # Define the solution function
    def solution(x, y, t):
        z = 0
        for n in range(1, 31):
            for m in range(1, 31):
                lambda_nm = np.pi**2 * (n**2 / a**2 + m**2 / b**2)
                # Compute the coefficient Anm
                xx = np.linspace(0, a, 100)
                yy = np.linspace(0, b, 100)
                Anm = (
                    4
                    * np.trapezoid(
                        np.cos(np.pi / 2 + np.pi * xx / a) * np.sin(n * np.pi * xx / a),
                        xx,
                    )
                    * np.trapezoid(
                        np.cos(np.pi / 2 + np.pi * yy / b) * np.sin(m * np.pi * yy / b),
                        yy,
                    )
                    / (a * b)
                )
                z += (
                    Anm
                    * np.cos(c * np.sqrt(lambda_nm) * t)
                    * np.sin(n * np.pi * x / a)
                    * np.sin(m * np.pi * y / b)
                )
        return z

    # Set up the figure and axis for animation
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(0, a)
    ax.set_ylim(0, b)
    ax.set_zlim(-1, 1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("u(x,y,t)")
    ax.set_title("Rectangular Membrane")

    # Update function for FuncAnimation
    def update(frame):
        ax.clear()
        Z = solution(X, Y, frame)  # Compute the new Z values
        ax.plot_surface(X, Y, Z, cmap="viridis", vmin=-1, vmax=1)
        ax.set_xlim(0, a)
        ax.set_ylim(0, b)
        ax.set_zlim(-1, 1)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("u(x,y,t)")
        ax.set_title("Rectangular Membrane")

    # Create and save the animation
    anim = FuncAnimation(fig, update, frames=t, interval=50)
    anim.save("rectangular_membrane_2_animation.gif", writer="imagemagick", fps=20)

    plt.show()
