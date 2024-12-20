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

- If $\lambda = 0$, then $r_1 = r_2 = 0$ and the general solution is
$$
X(x) = c_1 + c_2 x.
$$
Substituing it into the boundary conditions $\eqref{eq:ref2}$ again lead to $c_1 = c_2 = 0$, hence no non-zero solutions of our Sturm-Liouville problem for $\lambda \leq 0$.

- If $\lambda > 0$, then $r_{1, 2} = \pm i \sqrt{\lambda}$, and the general solution becomes
$$
X(x) = c_1 \cos{\left( \sqrt{\lambda} x \right)} + c_2 \sin{\left(\sqrt{\lambda}x\right)}.
$$
Substituting into the boundary conditions $\eqref{eq:ref2}$ results in
$$
\left\{\begin{align*}
c_1 = 0, \\
c_2 \sin{\left(\sqrt{\lambda}l\right)} = 0
\end{align*}\right.
$$
If $c_2 = 0$, then $X(x) \equiv 0$ which is a trivial solution. Therefore, we set $c_2 \neq 0$ and hence
$$
\sin{\left(\sqrt{\lambda}l\right)} = 0,
$$
giving $\sqrt{\lambda}l = k \pi$, $k = \pm 1, \pm 2, ...$. Theerfore,
$$
\lambda = \lambda_k = \left(\frac{k \pi}{l}\right)^2,
$$
meaning eigenvalues exist when $\lambda > 0$. The eigenfunctions corresponding to the above eigenvalues are
$$
X_k(x) = \sin{\left(\frac{k \pi x}{l}\right)}, \quad k > 0, k \in N.
$$

Going back to $T^{\prime\prime}(t) + a^2 \lambda T(t) = 0$, solving in analogical way, when $\lambda = \lambda_k$ the solution becomes

$$
T_k(t) = A_k \cos{\left(\frac{ak\pi}{l}t\right)} + B_k \sin{\left(\frac{ak\pi}{l}t\right)}
$$

for some constants $A_k$ and $B_k$. Hence,

$$
u_k(x,t) = X_k(x) T_k(t) = \left(A_k \cos{\left(\frac{ak\pi}{l}t\right)} + B_k \sin{\left(\frac{ak\pi}{l}t\right)}\right) \sin{\left(\frac{k \pi x}{l}\right)}, \quad k > 0, k \in N
$$

are solutions to our wave equation, also satisfying the boundary conditions. Since our equation is linear, forming a linear system with its conditions, the **principle of superposition** is valid. In other words, if $u_1, u_2, ..., u_n$ are solutions of our system, then

$$
\alpha_1 u_1 + \alpha_2 u_2 + ... + \alpha_n u_n
$$

for some constants $\alpha_1, \alpha_2, ..., \alpha_n$ is also a solution of the system. But in our case we have an infinite number of functions $u_1, u_2, ...$ which satisfy the linear system. Therefore, we need the **generalised superposition principle** stating that in such case

$$
u = \sum_n^{\infty} \alpha_n u_n
$$

for some arbitrary constants $\alpha_n$ is a solution to the system if the series converges uniformly and is twice differentiable termwise. This generalisation is a Lemma and should be prooved. The proof can be found in ...

Assuming we have prooved the said Lemma, we can state that our system has a solution of the form

$$
u(x, t) = \sum_{k=1}
^{\infty} u_k(x, t) = \sum_{k=1}^{\infty} \left(A_k \cos{\left(\frac{ak\pi}{l}t\right)} + B_k \sin{\left(\frac{ak\pi}{l}t\right)}\right) \sin{\left(\frac{k \pi x}{l}\right)}.
$$

The next task we have to tackle is to determine the coefficients $A_k$ and $B_k$. We can achieve this by using the initial conditions 

$$
u(x, 0) = \varphi_1(x), \quad \text{and} \quad u_t(x, 0) = \varphi_2(x).
$$

We get

$$
u(x, 0) = \sum_{k=1}
^{\infty} A_k \sin{\left(\frac{k \pi x}{l}\right)} = \varphi_1(x)
$$

and

$$
u_t(x, 0) = \sum_{k=1}^{\infty} \frac{ak\pi}{l} B_k \sin{\left(\frac{k \pi x}{l}\right)} = \varphi_2(x).
$$

Now, we have to expand both $\varphi_1(x)$ and $\varphi_2(x)$ into series in terms of sines only (why?). We have

$$
\varphi_1(x) = \sum_{k=1}^{\infty} \varphi_k^{(1)} \sin{\left(\frac{k \pi}{l}x\right)}
$$

and

$$
\varphi_2(x) = \sum_{k=1}^{\infty} \varphi_k^{(2)} \sin{\left(\frac{k \pi}{l}x\right)}.
$$

By the Fourier series theroem of uniqueness, we get

$$
A_k = \varphi_k^{(1)} \quad \text{and} \quad B_k = \frac{l}{ak\pi} \varphi_k^{(2)},
$$

or (why?)

$$
A_k = \frac{2}{l} \int_{0}^{l} \varphi_1(x) \sin{\left(\frac{k \pi}{l}x\right)} \mathrm{d}x
$$

and

$$
B_k = \frac{2}{ak\pi} \int_{0}^{l} \varphi_2(x) \sin{\left(\frac{k \pi}{l}x\right)} \mathrm{d}x.
$$

...
