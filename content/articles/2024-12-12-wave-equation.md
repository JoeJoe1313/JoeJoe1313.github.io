---
Title: Wave Equation
Date: 2024-12-12 13:15
Category: Mathematics
Tags: mathematics, python
Slug: 2024-12-12-wave-equation
---

Partial differential equations...

# Introduction

Let $u(x, y, t)$ be ...
 
The homogenous wave equation is given by

$$\frac{\partial^2 u}{\partial t^2} - c^2 (\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}) = 0$$

or

$$u_{tt} - c^2 (u_{xx} + u_{yy}) = 0.$$

# Physical interpretation

The wave equation is a simplified model for a vibrating
string (𝑛 = 1), membrane (𝑛 = 2), or elastic solid (𝑛 = 3). In these
physical interpretations 𝑢(𝑥, 𝑡) represents the displacement in some direction
of the point 𝑥 at time 𝑡 ≥ 0.

1D and 2D Equations

# Rectangular Membrane

Pass

$$D := \{0 < x < a, 0 < y < b\}
$$

...

$$\left\{\begin{align*}
u_{tt} - c^2 (u_{xx} + u_{yy}) = 0, (x,y,t) \in G = D \times (0, +\infty), \\ 
u|_{t=0} = \varphi(x, y), u_t |_{t=0} = \psi(x, y), (x, y) \in \bar{D}, \\
u|_{\partial D} = 0, t \geq 0.
\end{align*}\right.$$

...

$$\varphi(x, y) \in C^3 (\bar{D}), \psi(x, y) \in C^2 (\bar{D})
$$

and ...

$$\varphi |_{\partial D} = \varphi_{xx} |_{x = 0} = \varphi_{xx} |_{x = a} = \varphi_{yy} |_{y =0} = \varphi_{yy} |_{y = b} = \psi |_{\partial D} = 0.
$$

Solution... :

$$u(x, y, t) = \sum_{n, m = 1}^{\infty} \left(A_{n, m} \cos{\sqrt{\lambda_{n, m}} ct} + B_{n, m} \sin{\sqrt{\lambda_{n, m}} ct} \right) \sin{\frac{\pi n}{a}} x \sin{\frac{\pi m}{b}} y,
$$

where

$$\lambda_{n, m} = \left(\frac{\pi n}{a} \right)^2 + \left(\frac{\pi m}{b} \right)^2.
$$

From the initial conditions it follows

$$A_{n, m} = \frac{4}{ab} \int_D \varphi(x, y) \sin{\frac{\pi n}{a}} x \sin{\frac{\pi m}{b}} y \mathrm{d}x \mathrm{d}y,
$$

and

$$B_{n, m} = \frac{4}{abc\sqrt{\lambda_{n, m}}} \int_D \psi(x, y) \sin{\frac{\pi n}{a}} x \sin{\frac{\pi m}{b}} y \mathrm{d}x \mathrm{d}y.
$$

## Example 1

...

$$\left\{\begin{align*}
u_{tt} - u_{xx} - u_{yy} = 0, 0 < x < \pi, 0 < y < \pi, t > 0, \\
u|_{t=0} = \sin{x} \sin{y}, u_t |_{t=0} = \sin{4x} \sin{3y}, x, y \in (0, \pi), \\
u|_{x = 0} = 0, u|_{x = \pi} = 0, 0 < y < \pi, t > 0, \\
u|_{y = 0} = 0, u|_{y = \pi} = 0, 0 < x < \pi, t > 0.
\end{align*}\right.$$

Solution:

$$u(x, y, t) = \sum_{n, m = 1}^{\infty} \left(A_{n, m} \cos{\sqrt{\lambda_{n, m}} t} + B_{n, m} \sin{\sqrt{\lambda_{n, m}} t} \right) \sin{n} x \sin{m} y,
$$

where

$$\lambda_{n, m} = n^2 + m^2,
$$

$$A_{n, m} = \frac{4}{\pi^2} \int_0^\pi \sin{x} \sin{nx} \mathrm{d}x \int_0^\pi \sin{y} \sin{my} \mathrm{d}y,
$$

$$B_{n, m} = \frac{4}{\pi^2\sqrt{\lambda_{n, m}}} \int_0^\pi \sin{4x} \sin{nx} \mathrm{d}x \int_0^\pi \sin{3y} \sin{my} \mathrm{d}y.
$$

Therefore, $A_{1, 1} = 1$, $B_{4, 3} = \frac{1}{5}$, and every other coefficients is equal to $0$. Finally, 

$$u(x, y, t) = \cos{\sqrt{2}t} \sin{x} \sin{y} + \frac{1}{5} \sin{5t} \sin{4x} \sin{3y}.
$$

For $t \in [0, 6]$:

![Rectangular Membrane 1](/images/rectangular_membrane_1_animation.gif)

Snaphots:

![t0](/images/rectangular_membrane_1_t0.png)![t1](/images/rectangular_membrane_1_t1.png)![t6](/images/rectangular_membrane_1_t6.png)

## Example 2

...

# Circular Membrane

Pass

$$\left\{\begin{align*}
u_{tt} - \frac{1}{4} (u_{xx} + u_{yy}) = 0, x^2 + y^2 < 9, t > 0, \\ 
u|_{t=0} = (x^2 + y^2) \sin^3(\pi \sqrt{x^2 + y^2}), u_t |_{t=0} = 0, x^2 + y^2 \leq 9, \\
u|_{x^2 + y^2 = 9} = 0, t \geq 0.
\end{align*}\right.$$

Fourier method: Change to polar coordinates

$$\left\{\begin{align*}
x = \rho \cos(\varphi), \\
y = \rho \sin(\varphi)
\end{align*}\right.
$$

...

Then the function in the first initial condition $u |_{t=0}$ becomes

$$\tau(\rho) = \rho^2 \sin^3(\pi \rho)
$$

which is radially symmetric and hence the solution will be also radially symmetric. It is given by

$$u(\rho, t) = \sum_{m=1}^{\infty} A_m \cos{\frac{a \mu_m^{(0)}t}{r}} J_0\left(\frac{\mu_m^{(0)}}{r}\rho\right),
$$

where

$$A_m = \frac{4}{r^2 J_1^2(\mu_m^{(0)})} \int_0^r \rho^3 \sin^3(\pi \rho) J_0\left(\frac{\mu_m^{(0)}}{r}\rho\right) d\rho,
$$

and $\mu_m^{(0)}$ are the positive solutions to $J_0(\mu) = 0$.

...

![Bessel Functions](/images/BesselJ_800.svg)

...

Test some code:

```
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

![Matlab Membrane](/images/CircularMembrane.gif)

# References

- [1](https://www.amazon.co.uk/Partial-Differential-Equations-Graduate-Mathematics/dp/1470469421/ref=sr_1_3?crid=2BINQDJ5R7XUB&dib=eyJ2IjoiMSJ9.GgU4uQBUKYO960lL6EjVJjksjFysLhCJKEHP436_saFGnfKf4uvgqyl_3WBjV779K4AwonOY5XnkRxVFCIqqGZCCE3I8YEjIC7mzvLwUa2lBPvByBCoFxTvGhrSKGLiAKlAvTVFSlbwklqyWEj4o852csy80_D3G2Gk9pedHKz22vqyc8UI8HAxWZ1wfu5bNoaqOOEDhy0W2XLaSijLCENnzVXjxTLS5xZkMCXr72G0.NeT6LdhY-WV9xVA26fbGHp37FbAKGo7mLwpV9m_2Rdk&dib_tag=se&keywords=partial+differential+equations&nsdOptOutParam=true&qid=1734133658&sprefix=partial+diff%2Caps%2C129&sr=8-3)
- [2](https://mathworld.wolfram.com/BesselFunctionoftheFirstKind.html)
