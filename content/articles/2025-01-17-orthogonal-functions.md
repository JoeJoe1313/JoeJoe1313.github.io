---
Title: Orthogonal Functions
Date: 2025-01-17 07:00
Category: Mathematics
Tags: mathematics
Slug: orthogonal-functions
Status: published
---

In this post we are going to explore the so called orthogonal functions, and some of their properties. We are also going to show that these orthogonal functions are closely related to the least-squares approximation method. This alternative to the least-squares method can be helpful in certain cases when the least-squares produces a hard to solve linear system.

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
c_1 \int_a^b w(x) f_1(x) f_j(x) \mathrm{d}x + c_2 \int_a^b w(x) f_2(x) f_j(x) \mathrm{d}x + ... + c_N \int_a^b w(x) f_N(x) f_j(x) \mathrm{d}x = 0
$$

From the orthogonal properties it follows

$$
c_j \int_{a}^{b} w(x) f_{j}^{2}(x) \mathrm{d}x = c_j \lambda_j = 0,
$$

meaning $c_j = 0$ for every $j$. Thus, the assumed relation doesn't exist, and the functions are independent.

We are left with proving the opposite, that from a system of linearly independent functions we can construct an orthogonal system. We can do this with the help of the **Schmidt process**. Let $f_i(x)$ be the set of linearly independent functions. We have

$$
\int_{a}^{b} w(x) f_{0}^2(x) \mathrm{d}x = \lambda_0 > 0, \quad w(x) > 0.
$$

Then

$$
g_{0} = \frac{f_{0}(x)}{\sqrt{\lambda_0}}
$$

would be our first orthonormal function. By induction, we can assume we have constructed the first $j$ orthonormal functions $g_{i}(x)$, $i = 0, 1, ..., j-1$. Let

$$
F_{j}(x) = a_{0} g_{0}(x) + a_{1} g_{1}(x) + ... + a_{j-1} g_{j-1}(x) + f_j.
$$

We have that the functions $f_i(x)$ are linearly independent, and that every $g_{i}(x)$ is a linear combination of $f_{k}(x)$, $k \leq i$, thus

$$
F_j(x) \not\equiv 0.
$$

We need

$$
\int_{a}^{b} w(x) F_j(x) g_j(x) \mathrm{d}x = 0, \quad 0 \leq i \leq j-1.
$$

From the definition of $F_j(x)$ the above equation becomes

$$
a_i + \int_{a}^{b} w(x) g_i(x) f_j(x) \mathrm{d}x = 0.
$$

From here we can determine $a_i$, and hence $F_j(x)$ as well. We have to "norm" $F_j(x)$ so we have to compute

$$
\int_{a}^{b} w(x) F_j^2(x) \mathrm{d}x = \lambda_j > 0, \quad w(x) \geq 0,
$$

and let

$$
g_j(x) = \frac{F_j(x)}{\sqrt{\lambda_j}}.
$$

This ends the induction step.

If we have a finite number $N$ of nodes $x_m$, there exist at least $N$ linearly independent functions $f_j(x_m)$. But these $N$ functions exist because of the following system

$$
g_j(x_m) = \left\{
\begin{align*}
0, \quad m \neq j \\
1, \quad m = j
\end{align*}
\right.
, \quad j = 1, 2, ..., N,
$$

where no subset of these $N$ functions $g_j(x_m)$ can be linearly dependant.

# Least Squares and the Fourier Coefficients

Finally, we are at the point of showing that the least-squares method is closely connected to orthogonality.

---

<b>Theorem 1.</b> <i>The Fourier coefficients $a_j$ give the best leas-squares approximation when the function $F(x)$ is expanded over an orthogonal system of functions $g_j(x)$.</i>

In order to prove the theorem we have to minimize the arbitrary expansion 

$$
m = \int_{a}^{b} w(x) \left[F(x) - \sum_{j=0}^{M} c_j g_j(x) \right]^2 \mathrm{d}x = \\
= \int_a^b w(x) F^2(x) \mathrm{d}x - 2 \sum_{j=0}^{M} c_j \int_{a}^{b} w(x) F(x) g_j(x) \mathrm{d}x + \sum_{i=0}^{M} \sum_{j=0}^{M} c_j c_i \int_{a}^{b} w(x) g_i(x) g_j(x) \mathrm{d}x = \\
= \int_{a}^{b} w(x) F^2(x) \mathrm{d}x - 2\sum_{i=0}^{M}c_i a_i + \sum_{i=0}^{M} c_i^2 = \\
= \int_{a}^{b} w(x) F^2(x) \mathrm{d}x - \sum_{i=0}^{M} a_i^2 + \sum_{i=0}^{M} (a_i - c_i)^2.
$$

The above equation achieves its minimum only when $c_i = a_i$, which is what we wanted.

---

It is useful to note that regarding the best approximation with orthogonal functions every coefficient $a_i$ is determined independently of the others. Thus, if we dedcide to change the amount of the used functions $g_i(x)$ there is no need to reevaluate the coefficients we have already evaluated. This motivates us to explore the next problem.

If the coefficients $c_i$ of the function $F(x)$ when approximating with the least-squares method via the system $\mu_i(x)$ do not change when we change the number of used functions $\mu_i(x)$, then the functions $\mu_i(x)$ are orthogonal. Let

$$
g(c_0, c_1, ..., c_n) = \int_a^b w(x) \left[F(x) - \sum_{i=0}^{M}c_i\mu_i(x)\right]^2 \mathrm{d}x.
$$

Once again, we have to minimze $g$. Thus,

$$
\frac{\partial{g}}{\partial{c_i}} = 0 = -2 \int_a^b w(x) \left[F(x) - \sum_{i=0}^{M}c_i \mu_i(x)\right] \mu_j(x) \mathrm{d}x,
$$

or

$$
\int_a^b w(x) F(x) \mu_j(x) \mathrm{d}x = \sum_{i=0}^{M} c_i \int_a^b w(x) \mu_i(x) \mu_j(x) \mathrm{d}x.
$$

If the above property is true for all $M$, then it should be true for $M+1$ as well:

$$
\int_a^b w(x) F(x) \mu_j(x) dx = \sum_{i=0}^{M+1} c_i \int_a^b w(x) \mu_i(x) \mu_j(x) \mathrm{d}x, \quad c_{M+1} \neq 0.
$$

Now, after subtracting it from the previous equation, we get

$$
c_{M+1} \int_a^b w(x) \mu_{M+1}(x) \mathrm{d}x = 0, 
$$

for every $j$. Simply said, $\mu_j(x)$ is orthogonal to $\mu_{M+1}$ for an arbitrary $M$.

To summarise, we saw that the orthogonal functions, the Fourier coefficients, and the approxiamtion via the least-squares method are closely connected.
