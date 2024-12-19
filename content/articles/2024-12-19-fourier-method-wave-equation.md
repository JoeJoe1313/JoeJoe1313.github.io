---
Title: Fourier Method for the Wave Equation
Date: 2024-12-19 07:00
Category: Mathematics
Tags: mathematics
Slug: 2024-12-19-fourier-method-wave-equation
---

In this post we are going to explore the Fourier method for solving the 1D and 2D wave equations. The method is more known under the name of the method of separation of variables.

# Fixed String (1D Wave Equation)

First, let's take a look at the model of a string with length $l$ which is also fixed at both ends:

$$
\left\{\begin{align*}
u_{tt} = a^2 u_{xx}, \\ 
u(x, 0) = \varphi_1(x),\\
u_t(x, 0) = \varphi_2(x), \\
u(0, t) = u(l, t) = 0.
\end{align*}\right.
$$

We start solving the equation by taking into account only the boundary conditions $u(0, t) = u(l, t) = 0$. The idea is to find solution $u(x, t)$ of the form

$$
u(x, t) = X(x)T(t).
$$

We substitute this form of the solution into the wave equation and get 

$$
\frac{1}{a^2} T^{\prime\prime}(t)X(x) = T(t)X^{\prime\prime}(x),
$$

further divding by $X(x)T(t)$ leads to

$$
\frac{1}{a^2} \frac{T^{\prime\prime}(t)}{T(t)} = \frac{X^{\prime\prime}(x)}{X(x)}.
$$
