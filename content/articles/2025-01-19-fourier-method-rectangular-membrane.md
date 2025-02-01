---
Title: Fourier Method for the 2D Wave Equation: Rectangular Membrane
Date: 2025-01-19 07:00
Category: Mathematics
Tags: mathematics, pde
Slug: 2025-01-19-fourier-method-rectangular-membrane
Status: draft
---

In this post we are going to explore the Fourier method for solving the 2D wave equation. For the 2D wave equation we are going to show the application of the method to a rectangular membrane. We are also going to attempt to outline some of the physical interpretations of the rectangular membrane.

# 2D Wave Equation

The 2D wave equation is of the form

$$\label{eq:tdwave}
\frac{\partial^2 u}{\partial t^2} = a^2 \Delta{u} = a^2\left(\frac{\partial^2 u}{\partial^2 x^2} + \frac{\partial^2 u}{\partial y^2}\right). \tag{1}
$$

## Rectangular Membrane

Let's assume we have a rectangular membrane with sides of length $l_1$ and $l_2$. Let's also assume it is fastened along the edges. A visaulisation can be seen below.

<center>
![Rectangular Membrane](/images/2024-12-19-fourier-method-wave-equation/rectangular_membrane.svg){width=50%}
</center>

We can describe the problem via the model

$$
\left\{\begin{align*}
\frac{\partial^2 u}{\partial t^2} = a^2 \Delta{u} = a^2\left(\frac{\partial^2 u}{\partial^2 x^2} + \frac{\partial^2 u}{\partial y^2}\right), \quad 0 < x < l_1, \quad 0 < y < l_2, \\
u|_{\Gamma} = 0, \\
u|_{t=0} = \varphi(x, y), u_t|_{t=0} = \psi(x, y),
\end{align*}\right.
$$

also with boundary conditions coming from the rectangular boundary $\Gamma$

$$
\left\{\begin{align*}
u(0, y, t) = 0, \quad u(x, 0, t) = 0, \\
u(l_1, y, t) = 0, \quad u(x, l_2, t) = 0.
\end{align*}\right.
$$

A visualisation of the problem can be seen below.

<center>
![Rectangular Membrane 3D](/images/2024-12-19-fourier-method-wave-equation/rectangular_membrane_3d.svg){width=50%}
</center>

As in the 1D wave equation, we are going to apply the Fourier method, meaning we are looking for a solution of the form

$$
U(x, y, t) = T(t)W(x, y).
$$

Substituting into the 2D wave equation $\eqref{eq:tdwave}$ we get

$$
T^{\prime\prime}W = a^2 T \Delta{W}.
$$

Then, we divide by $a^2TW$ and get

$$
\frac{T^{\prime\prime}}{a^2T} = \frac{\Delta{W}}{W} = - \lambda^2,
$$

leading to the following equations

$$
T^{\prime\prime} + \lambda^2 a^2 T = 0
$$

and

$$
\Delta{W} + \lambda^2 W = 0. \quad \text{(Helmholtz equation)}
$$

Now, we should do the same and apply the Fourier method to the Helmoltz equation. We are looking for a solution of the form

$$
W(x, y) = X(x) Y(y).
$$

Substitution leads to

$$
X^{\prime\prime}Y + XY^{\prime\prime} + \lambda^2 XY = 0.
$$

Further, dividing by $XY$ gives

$$
-\frac{X^{\prime\prime}}{X} = \frac{Y^{\prime\prime}}{Y} + \lambda^2 = \alpha^2.
$$

Once again, we obtain the following to equations

$$
X^{\prime\prime} + \alpha^2 X = 0,
$$

and

$$
Y^{\prime\prime} + \beta^2Y = 0,
$$

where

$$
\lambda^2 = \alpha^2 + \beta^2.
$$

Now, the boundary conditions take the forms

$$
X(0) Y(y) T(t) = 0, \quad \text{and} \quad X(l_1) Y(y) T(t) = 0,
$$

and because we are looking for non-trivial solutions meaning $T(t) \neq 0$ and $Y(y) \neq 0$ identically, it follows

$$
X(0) = X(l_1) = 0.
$$

Now, with the same logic first we have the boundary conditions

$$
X(x)Y(0)T(t) = 0, \quad \text{and} \quad X(x)Y(l_2)T(t) = 0,
$$

then since $X(x) \neq 0$, and $T(t) \neq 0$ it follows

$$
Y(0) = Y(l_2) = 0.
$$

We obtain the following Sturm-Liouville problms

$$
\left\{\begin{align*}
X^{\prime\prime} + \alpha^2 X = 0, \\
X(0) = X(l_1) = 0,
\end{align*}\right.
$$

and

$$
\left\{\begin{align*}
Y^{\prime\prime} + \beta^2Y = 0, \\
Y(0) = Y(l_2) = 0,
\end{align*}\right.
$$

with eigenvalues and corresponing eigenfunctions, respectively,

$$
\alpha_k = \frac{k\pi}{l_1}, k = 1,2,..., \quad X_k(x) = \sin{\left(\frac{k\pi}{l_1}x\right)}
$$

and

$$
\beta_k = \frac{n\pi}{l_2}, n = 1,2,..., \quad Y_n(y) = \sin{\left(\frac{n\pi}{l_2}y\right)}.
$$

As defined earlier, to every pair $\alpha_k$, $\beta_k$ there is a corresponding $\lambda_{kn}^2 = \alpha_k^2 + \beta_k^2$. This is a Dirichlet eigenvalue of the Laplacian in our rectangular membrane. For each $\lambda_{kn}$ we have

$$
\lambda_{kn} = \sqrt{\alpha_k^2 + \beta_k^2} = \pi \sqrt{\frac{k^2}{l_1^2} + \frac{n^2}{l_2^2}}
$$

and hence the corresponding general solution of $T^{\prime\prime} + \lambda_{kn}^2 a^2 T = 0$ is

$$
T_{kn}(t) = A_{kn}\cos{(a\lambda_{kn}t)} + B_{kn}\sin{(a\lambda_{kn}t)}.
$$

Again, by the superposition principle, the solution of our 2D wave equation on rectangular membrane is sought in the form

$$
u(x, y, t) = \sum_{k,n=1}^{\infty}\left(A_{kn}\cos{(a\lambda_{kn}t)} + B_{kn}\sin{(a\lambda_{kn}t)}\right)\sin{\left(\frac{k\pi}{l_1}x\right)}\sin{\left(\frac{n\pi}{l_2}y\right)}.
$$

...

$$
u(x, y, 0) = \sum_{k,n=1}^{\infty}A_{kn}\sin{\left(\frac{k\pi}{l_1}x\right)}\sin{\left(\frac{n\pi}{l_2}y\right)} = \varphi(x, y),
$$

and

$$
u_t(x, y, 0) = \sum_{k,n=1}^{\infty}B_{kn}a\lambda_{kn}\sin{\left(\frac{k\pi}{l_1}x\right)}\sin{\left(\frac{n\pi}{l_2}y\right)} = \psi(x, y).
$$

...

$$
\omega_{kn}(x, y) := \sin{\left(\frac{k\pi}{l_1}x\right)}\sin{\left(\frac{n\pi}{l_2}y\right)}
$$

...

$$
\int_0^{l_1} \int_0^{l_2} \omega_{kn}(x, y) \omega_{rs}(x, y) \mathrm{d}x \mathrm{d}y = \left\{\begin{align*}
0, \quad k \neq r \quad \text{or} \quad n \neq s, \\
\frac{l_1 l_2}{4}, \quad k = r \quad \text{and} \quad n = s.
\end{align*}\right.
$$

...

$$
A_{kn} = \frac{4}{l_1 l_2} \int_0^{l_1} \int_0^{l_2} \varphi(x, y) \sin{\left(\frac{k\pi}{l_1}x\right)} \sin{\left(\frac{n\pi}{l_2}y\right)} \mathrm{d}x \mathrm{d}y,
$$

and

$$
B_{kn} = \frac{4}{l_1 l_2 a \lambda_{kn}} \int_0^{l_1} \int_0^{l_2} \psi(x, y) \sin{\left(\frac{k\pi}{l_1}x\right)} \sin{\left(\frac{n\pi}{l_2}y\right)} \mathrm{d}x \mathrm{d}y.
$$
