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

...

$$
\frac{1}{a^2} \frac{T^{\prime\prime}(t)}{T(t)} = \frac{X^{\prime\prime}(x)}{X(x)} = -\lambda,
$$

producing the following two equeations:

$$
T^{\prime\prime}(t) + a^2 \lambda T(t) = 0
$$

and

$$\label{eq:ref}
X^{\prime\prime}(x) + \lambda X(x) = 0. \tag{*}
$$

Let's begin with solving the second equation. The boundary conditions give

$$
X(0)T(t) = 0 \quad \text{and} \quad X(l)T(t) = 0.
$$

Because we are interested only in non-trivial solutions and thus $T \neq 0$, we have

$$\label{eq:ref2}
X(0) = 0 \quad \text{and} \quad X(l) = 0. \tag{**}
$$

Now, we have to find the non-trivial solutions for $X(x)$ satisfying

$$
\left\{\begin{align*}
X^{\prime\prime}(x) + \lambda X(x) = 0, \\
X(0) = 0, \quad X(l) = 0.
\end{align*}\right.
$$

The above problem is an example of the so called **Sturm-Liouville problem**. In order to find the general solution of the second order linear homogeneous differential equation with constant coefficients $\eqref{eq:ref}$ we should solve its characteristic equation

$$
r^2 + \lambda = 0.
$$

- If $\lambda < 0$, then $r_{1, 2} = \pm \sqrt{-\lambda}$, hence the general solution is
$$
X(x) = c_1 e^{\sqrt{-\lambda}x} + c_2 e^{-\sqrt{-\lambda}x}
$$
for some constants $c_1$ and $c_2$. In order to determine the constants we substitute the above solution into the boundary conditions $\eqref{eq:ref2}$ and get the system
$$
\left\{\begin{align*}
c_1 + c_2 = 0, \\
c_1 e^{\sqrt{-\lambda}l} + c_2 e^{-\sqrt{-\lambda}l} = 0. 
\end{align*}\right.
$$
This results in $c_1 = c_2 = 0$, meaning our Sturm-Liouville problem doesn't have a non-zero solution for $\lambda < 0$.

- If $\lambda = 0$, ...
