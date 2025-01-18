---
Title: Orthogonal Functions
Date: 2025-01-17 07:00
Category: Mathematics
Tags: mathematics, python
Slug: 2025-01-17-orthogonal-functions
Status: draft
---

In this post we are going to explore the so called orthogonal functions, followed by orthogonal polynomials and some of their properties. We are also going to show that these orthogonal functions (polynomials) are closely related to the least-squares approximation method. This alternative to the least-suqares approximation can be helpful in certain cases when the leas-squares produces a hard to solve linear system.

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

We can show that the functions are orthogonal over the interval $0 \leq x \leq 2\pi$.
