---
Title: My super title 2 test
Date: 2024-12-10 10:20
Modified: 2024-12-10 10:27
Category: Python
Tags: sth
Slug: my-super-post-2
Summary: Short version for index and feeds
---

# Wave Equation

## Introduction

Test

The following equation

$$u(x, y, t)$$

$$\frac{\partial^2 u}{\partial t^2} - c^2 (\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}) = 0$$

$$u_{tt} - c^2 (u_{xx} + u_{yy}) = 0$$

is

## Circular Membrane

Pass

Test some code:

```{python}
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import root_scalar
from scipy.special import jv as besselj


def circular_membrane():
    a = 0.5
    r = 3
    rho = np.linspace(0, r, 51)
    phi = np.linspace(0, 2 * np.pi, 51)
```

Test code collapse:

<details>
<summary>Click to expand code</summary>

```{python}
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import root_scalar
from scipy.special import jv as besselj


def circular_membrane():
    a = 0.5
    r = 3
    rho = np.linspace(0, r, 51)
    phi = np.linspace(0, 2 * np.pi, 51)

    tmax = 30
    t = np.linspace(0, tmax, 100)
    N = 40

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

    # Solution function
    def solution(R, t):
        y = np.zeros_like(R)
        for m in range(N):
            s = tau(R[0, :]) * R[0, :] * besselj(0, mju[m] * R[0, :] / r)
            A0m = 4 * np.trapz(s, R[0, :]) / ((r**2) * (besselj(1, mju[m]) ** 2))
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
    ax.set_title("Circular membrane")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("u(x,y,t)")

    # Update function for FuncAnimation
    def update(frame):
        ax.clear()
        Z = solution(R, frame)
        # ax.plot_surface(X, Y, Z, cmap="viridis")
        ax.plot_surface(X, Y, Z, cmap="viridis", vmin=-30, vmax=30)
        ax.set_xlim(-r, r)
        ax.set_ylim(-r, r)
        ax.set_zlim(-30, 30)
        ax.set_title("Circular membrane")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("u(x,y,t)")

    # Create the animation
    anim = FuncAnimation(fig, update, frames=t, interval=50)

    # Save the animation in GIF format:
    anim.save("circular_membrane_animation.gif", writer="imagemagick", fps=20)

    plt.show()
```
</details>

![Membrane](/images/circular_membrane_animation.gif)
