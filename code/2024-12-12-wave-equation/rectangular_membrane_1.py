import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def rectangular_membrane_1(t_max: int = 6):
    t = np.linspace(0, t_max, 100)  # Time points for animation
    x = np.linspace(0, np.pi, 51)  # x grid
    y = np.linspace(0, np.pi, 51)  # y grid
    X, Y = np.meshgrid(x, y)

    # Define the solution function
    def solution(x, y, t):
        return (
            np.cos(np.sqrt(2) * t) * np.sin(x) * np.sin(y)
            + np.sin(5 * t) * np.sin(4 * x) * np.sin(3 * y) / 5
        )

    # Set up the figure and axis for animation
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(0, np.pi)
    ax.set_ylim(0, np.pi)
    ax.set_zlim(-1, 1)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("u(x,y,t)")
    ax.set_title("Rectangular Membrane")

    # Update function for FuncAnimation
    def update(frame):
        ax.clear()  # Clear the previous frame
        Z = solution(X, Y, frame)  # Compute the new Z values
        _ = ax.plot_surface(X, Y, Z, cmap="viridis", vmin=-1, vmax=1)
        ax.set_xlim(0, np.pi)
        ax.set_ylim(0, np.pi)
        ax.set_zlim(-1, 1)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("u(x,y,t)")
        ax.set_title("Rectangular Membrane")

    # Create and save the animation
    anim = FuncAnimation(fig, update, frames=t, interval=50)
    anim.save("rectangular_membrane_1_animation.gif", writer="imagemagick", fps=20)

    plt.show()
