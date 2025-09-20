---
Title: Fourier Method for the 1D Wave Equation: Fixed String
Date: 2025-01-04 07:00
Category: Mathematics
Tags: mathematics, pde
Slug: fourier-method-fixed-string
Status: published
Series: The Wave Equation
Modified: 2025-09-15 07:00
---

In this post we are going to explore the Fourier method for solving the 1D wave equation. The method is more known under the name of the **method of separation of variables**. For the 1D wave equation we are going to show the application of the method to a fixed string. We are also going to attempt to outline some of the physical interpretations of the fixed string.

# 1D Wave Equation

The 1D wave equation is of the form

$$
u_{tt} = a^2 u_{xx}.
$$

## Fixed String

First, let's take a look at the model of a string with length $l$ which is also fixed at both ends:

$$
\left\{\begin{aligned}
u_{tt} = a^2 u_{xx}, \\ 
u(x, 0) = \varphi_1(x),\\
u_t(x, 0) = \varphi_2(x), \\
u(0, t) = u(l, t) = 0.
\end{aligned}\right.
$$

A visualisation of the string can be seen in the figure below.

<center>
![Fixed String](/images/2025-01-04-fourier-method-fixed-string/fixed_string.svg){ class="zoomable" width=60% }
</center>

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

We have two functions of independent variables which are equal. This is only possible if they are equal to the same constant. Therefore, let

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

for some arbitrary constants $\alpha_n$ is a solution to the system if the series converges uniformly and is twice differentiable termwise. This generalisation is a Lemma and should be prooved.

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

Now, we have to expand both $\varphi_1(x)$ and $\varphi_2(x)$ into series in terms of sines only. We have

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

or

$$
A_k = \frac{2}{l} \int_{0}^{l} \varphi_1(x) \sin{\left(\frac{k \pi}{l}x\right)} \mathrm{d}x
$$

and

$$
B_k = \frac{2}{ak\pi} \int_{0}^{l} \varphi_2(x) \sin{\left(\frac{k \pi}{l}x\right)} \mathrm{d}x.
$$

We are left with the task of the covergence of the infinite series. We have to explore the following series

$$
|u(x, t)| \leq \sum_{k=1}^{\infty}(|A_k| + |B_k|),
$$

$$
|u_t(x, t)| \leq \sum_{k=1}^{\infty}\frac{ak\pi}{l}(|A_k| + |B_k|),
$$

$$
|u_x(x, t)| \leq \sum_{k=1}^{\infty}\frac{k\pi}{l}(|A_k| + |B_k|),
$$

$$
|u_{tt}(x, t)| \leq \sum_{k=1}^{\infty}\frac{a^2 k^2 \pi^2}{l^2}(|A_k| + |B_k|),
$$

$$
|u_{xx}(x, t)| \leq \sum_{k=1}^{\infty}\frac{k^2 \pi^2}{l^2}(|A_k| + |B_k|).
$$

If the series on the right side (majorizing series) converge then the series on the left would also converge and the needed differentiation would exist. It is enough for the following series to converge

$$
\sum_{k=1}^{\infty} k^j \left(|\varphi_k^{(1)}| + \frac{2}{ak\pi}|\varphi_k^{(2)}|\right), j = 0, 1, 2.
$$

This is possible only if 

$$
\left\{\begin{align*}
\sum_{k=1}^{\infty} k^j |\varphi_k^{(1)}|, \\
\sum_{k=1}^{\infty} k^{j-1} |\varphi_k^{(2)}|,
\end{align*}\right. \quad j = 0, 1, 2.
$$

converge. From Calculus we know (theorem) that if $\varphi(x)$ is $m$-times differentiable then

$$
\sum_{k=1}^{\infty} k^{m-1} |\varphi_k|
$$

convergres. Therefore, in order for all the majorzing series to converge it is enough $\varphi_1(x)$ to be $3$-times differentiable, and $\varphi_2(x)$ to be $2$-times differentiable.

Finally, we should note a few things about the expansion of $\varphi_1(x)$ and $\varphi_2(x)$ into sine series. We have to note that in order to do that the function needs to be continued as an odd function which my lead to loss of the regularity of the lower derivatives. Let $\tilde{\varphi}_1(x)$ be the continuation of $\varphi_1(x)$ as an odd function (see the Figure below) defined as

<center>
![Odd continuation of a function](/images/2025-01-04-fourier-method-fixed-string/odd_continuation.png){ class="zoomable" width=50% }
</center>

$$
\tilde{\varphi}_1(x) = \left\{\begin{align*}
\varphi_1(x), \quad 0 \leq x \leq l, \\
-\varphi_1(-x), \quad -l \leq x \leq 0.
\end{align*}\right.
$$

Hence, in order for it to be continous and continously differentibale we need to enforce the following condition

$$
\varphi_1(0) = \varphi_1(l) = 0.
$$

To summarise, in order for $\sum_{k=1}^{\infty} \varphi_k^{(1)} \sin{\left( \frac{k\pi}{l}x\right)}$ to converge in $[0, l]$ it is necessary to enforce the above conditions to have zero values at both ends of the interval. As for the second derivative, if it exists it would be continuous as well. Similarly, for the third derivative to exist we enforce

$$
\varphi_1^{\prime\prime}(0) = \varphi_1^{\prime\prime}(l) = 0
$$

and obtain the corresponding necessary condition

$$
\varphi_2(0) = \varphi_2(l) = 0.
$$

Finally, after these enforced conditions we can conclude that (tehorem)

$$
u(x, t) = \sum_{k=1}^{\infty} \left(A_k \cos{\left(\frac{ak\pi}{l}t\right)} + B_k \sin{\left(\frac{ak\pi}{l}t\right)}\right) \sin{\left(\frac{k \pi x}{l}\right)}
$$

is a regular solution of the problem.

**Physical interpretation:**

If we go back to the eigenfunction

$$
u_k(x,t) = \left(A_k \cos{\left(\frac{ak\pi}{l}t\right)} + B_k \sin{\left(\frac{ak\pi}{l}t\right)}\right) \sin{\left(\frac{k \pi}{l}x\right)}, \quad k > 0, k \in N
$$

we can rewrite it as

$$
u_k(x,t) = \sqrt{A_k^2 + B_k^2} \sin{\left(\frac{k \pi}{l}x\right)} \sin{\left(\frac{ak\pi}{l}t + \phi_k\right)}, \quad k \in N,
$$

where

$$
\tan{(\phi_k)} = \frac{A_k}{B_k}.
$$

We can translate this as the points of the string to oscillate at the frequency $\omega_k = \frac{ak\pi}{l}$ with phase $\phi_k$. The amplitude is dependant on $x$ and is given by
$$
F_k = \sqrt{A_k^2 + B_k^2} \sin{\left(\frac{k\pi}{l}x\right)}.
$$

The $u_k(x, t)$ waves are called **standing-waves**. Depending on the values of $k$ we have the following scenarios:

- When $k = 1$ there are $2$ motionless points which are the ends of the (fixed) string
- When $k = 2$ a third moitonless point $x = \frac{l}{2}$ is added

These motionless points are called **nodes** of the standing wave. In general, $u_k(x, t)$ has $(k + 1)$ nodes located ate $0, \frac{1}{k}l, \frac{2}{k}l, ..., \frac{k-1}{k}l, l$. The maximum amplitude is achieved in the middle points between two nodes. These points are called **crests**. The fundamental tone, or the lowest tone, has frequency of $\omega_1 = \frac{a\pi}{l}$. The frequencies $\omega_k$ are called **harmonics**, while the higher tones corresponding to $\omega_k$, $k = 2, 3, ...$ are called **overtones**. It is quite natural to notice that the higher the value of $k$ the rapidly lower the amplitude of $u_k(x, t)$ becomes. Meaning, the effect from the higher harmonics all combined influences the quality of the sound. The below figure shows the harmonics for $k = 1, 2, 3$.

<center>
![Fixed Strings](/images/2025-01-04-fourier-method-fixed-string/harmonics.svg){ class="zoomable" width=70% }
</center>

### Example

Here, we are going to show an example of a fixed string. We are going to show an animated solution with the help of Python. The fixed string problem is given by

$$
\left\{\begin{aligned}
u_{tt} = \left(\frac{2}{3}\right)^2 u_{xx}, \\ 
u(x, 0) = \left\{\begin{align*}
\sin^3{(\pi x)}, \quad 1 \leq x \leq3, \\
0, \quad x \in R \backslash [1, 3],
\end{align*}\right.,\\
u_t(x, 0) = 0, \\
u(0, t) = u(\pi \sqrt{5}, t) = 0.
\end{aligned}\right.
$$

Using the $100$-th partial Fourier sum, below is shown the animated solution for $t \in [0, 30]$.

{% include_code_collapsible 2025-01-04-fourier-method-fixed-string/fixed_string.py lang:python :hideall: %}

<iframe src="{static}/code/2025-01-04-fourier-method-fixed-string/fixed_string_animation.html" width="100%" height="700px" frameborder="0"></iframe>
