import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def Rmembrana2():
    a = 1
    b = 2
    c = np.pi
    snapshots = [0, 2, 4.5]  # Specific time points for snapshots
    x = np.linspace(0, a, 50)  # x grid
    y = np.linspace(0, b, 50)  # y grid
    X, Y = np.meshgrid(x, y)

    # Define the solution function
    def solution(x, y, t):
        z = 0
        for n in range(1, 31):  # Sum over n
            for m in range(1, 31):  # Sum over m
                lambda_nm = np.pi**2 * (n**2 / a**2 + m**2 / b**2)
                # Compute the coefficient Anm
                xx = np.linspace(0, a, 100)
                yy = np.linspace(0, b, 100)
                Anm = (
                    4
                    * np.trapz(
                        np.cos(np.pi / 2 + np.pi * xx / a) * np.sin(n * np.pi * xx / a),
                        xx,
                    )
                    * np.trapz(
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

    # Save snapshots for specified time points
    for t in snapshots:
        Z = solution(X, Y, t)  # Compute the Z values for this time

        # Set up the figure
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Y, Z, cmap="viridis", vmin=-1, vmax=1)
        ax.set_xlim(0, a)
        ax.set_ylim(0, b)
        ax.set_zlim(-1, 1)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("u(x,y,t)")
        ax.set_title(f"Rectangular Membrane at t = {t}")

        # Save the snapshot
        plt.savefig(f"rectangular_membrane_2_t{t:.1f}.png")
        plt.close(fig)


Rmembrana2()
