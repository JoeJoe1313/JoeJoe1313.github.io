---
Title: Orthogonal Functions
Date: 2025-01-17 07:00
Category: Mathematics
Tags: mathematics, python
Slug: 2025-01-17-orthogonal-functions
Status: draft
---

In this post we are going to explore the so called orthogonal functions, followed by orthogonal polynomials and some of their properties. We are also going to show that these orthogonal functions (polynomials) are closely related to the least-squares approximation method. This alternative to the least-suqares approximation can be helpful in certain cases when the least-squares produces a hard to solve linear system.

# Orthogonal Functions

First, we should introduce some important theory. Let's begin by stating that two $n$-dimensional **vectors** $x$ and $y$ are **orthogonal** if their components satisfy

$$
\sum_{i = 1}^{n} x_i y_i = 0. 
$$

Now, if we increase the dimensions $n$ to infinity such that we can replace the vectors in the limit with continous functions ($f_{1}(x)$ and $f_{2}(x)$), and their sum approaches an integral, we have that two **functions** are **orthogonal** over the intevral $a \leq x \leq b$ if

$$\label{eq:1}
\int_a^b f_{1}(x) f_{2}(x) \mathrm{d}x = 0.\tag{1}
$$

In some cases a weight $w(x) \geq 0$ is included, and then \eqref{eq:1} becomes

$$
\int_a^b w(x) f_{1}(x) f_{2}(x) \mathrm{d}x = 0.
$$

Similarly, if we have a set of functions $f_{i}(x)$, $i = 0, 1, ...$ they are said to be mutually orthogonal if

$$
\int_a^b f_{i}(x) f_{j}(x) \mathrm{d}x = \left\{
\begin{align*}
0, \quad i \neq j \\
\lambda_i > 0, \quad i = j
\end{align*}
\right.
.
$$

Once again, a weight term $w(x) \geq 0$  can be included, and then

$$
\int_a^b w(x) f_{i}(x) f_{j}(x) \mathrm{d}x = \left\{
\begin{align*}
0, \quad i \neq j \\
\lambda_i > 0, \quad i = j
\end{align*}
\right.
.
$$

The above system is called **orthonormal** if

$$
\int_a^b w(x) f_{i}^{2}(x) \mathrm{d}x = 1.
$$

## Example

One of the most famous systems (families) of orthogonal functions is

$$
1, \cos{(x)}, \sin{(x)}, \cos{(2x)}, \sin{(2x)}, \cos{(3x)}, ...
$$

Part of the family is visualised below.

<center>
![Orthogonal Functions Example](/images/2025-01-17-orthogonal-functions/orthogonal_functions_example.svg){ width=75% }
</center>

We can easily show that the functions are orthogonal over the interval $0 \leq x \leq 2\pi$ because the following equations hold (by using a fundamental trigonometric formulas)

$$
\int_{0}^{2\pi} \cos{(mx)} \cos{(nx)} \mathrm{d}x = \left\{
\begin{align*}
2\pi, \quad m = n = 0 \\
\pi, \quad m = n \neq 0 \\
0, \quad m \neq n
\end{align*}
\right.
,
$$

$$
\int_{0}^{2\pi} \cos{(mx)} \sin{(nx)} \mathrm{d}x = 0,
$$

and

$$
\int_{0}^{2\pi} \sin{(mx)} \sin{(nx)} \mathrm{d}x = \left\{
\begin{align*}
\pi, \quad m = n \neq 0 \\
0, \quad m \neq n
\end{align*}
\right.
.
$$

Now, let's take a look at one possible application of these orthogonal functions. Let's assume that for a function $F(x)$, $0 \leq x \leq 2\pi$ we have

$$\label{eq:2}
F(x) = \frac{a_0}{2} + a_1 \cos{(x)} + b_1 \sin{(x)} + a_2 \cos{(2x)} + b_2 \sin{(2x)} + ... = \\
= \frac{a_0}{2} + \sum_{k = 1}^{\infty} (a_k \cos{(kx)} + b_k \sin{(kx)}).\tag{2}
$$

If we multiply \eqref{eq:2} with $\cos{(mx)}$ and integrate over the range of $x$, we get

$$\label{eq:3}
\int_{0}^{2\pi} F(x)\cos{(mx)} \mathrm{d}x = \pi a_m, \quad m = 0, 1, ...\tag{3}
$$

If we multiply \eqref{eq:2} with $\sin{(mx)}$ and integrate over the range of $x$, we get

$$\label{eq:4}
\int_{0}^{2\pi} F(x)\sin{(mx)} \mathrm{d}x = \pi b_m, \quad m = 1, 2, ...\tag{4}
$$

But why did we even mention that? In fact, with \eqref{eq:3} and \eqref{eq:4} we can compute the coefficients in the function expansion. Moreover, this way of computing the $a_m$ and $b_m$ coefficients gives them the name **Fourier coefficeints**. This is also valid for the general case of a system of orthogonal functions, meaning

$$
\int_{a}^{b} w(x) f_{i}(x) f_{j}(x) \mathrm{d}x = \left\{
\begin{align*}
0, \quad i \neq j \\
\lambda_i, \quad i = j
\end{align*}
\right.
.
$$

If we have the function expansion

$$
F(x) = \sum_{i = 0}^{\infty} a_i f_{i}(x),
$$

then the coefficients

$$
a_j = \frac{1}{\lambda_j} \int_{a}^{b} w(x) F(x) f_{j}(x) \mathrm{d}x
$$

are the Fourier coefficients.

# Linear Independence and Orthogonality: Connection

Here, we are going to show that linear independence and orthogonality are closely connected. For this purpose the first thing we have to show is that a system of orthogonal functions $f_i(x)$ is linearly independent over the interval of interest.

Let's assume there exists a linear dependence between the functions $f_i(x)$ with non-zero coefficients, or

$$
c_1 f_1(x) + c_2 f_2(x) + ... + c_N f_N(x) = 0
$$

for some $c_j \neq 0$. Then, we multiply with $w(x) f_j(x)$, $w(x) \geq 0$ and integrate over the interval and get

$$
c_1 \int_a^b w(x) f_1(x) f_j(x) + c_2 \int_a^b w(x) f_2(x) f_j(x) + ... + c_N \int_a^b w(x) f_N(x) f_j(x) = 0
$$

# Orthogonal Polynomials
