---
Title: Chebyshev Polynomials: Part 1
Date: 2025-01-06 07:00
Category: Mathematics
Tags: mathematics, polynomials
Slug: chebyshev-polynomials
Status: published
Series: Chebyshev Polynomials
---

Chebyshev polynomials are a sequence of orthogonal polynomials that play a central role in numerical analysis, approximation theory, and applied mathematics. They are named after the Russian mathematician Pafnuty Chebyshev and come in two primary types: Chebyshev polynomials of the first kind ($T_n(x)$) and Chebyshev polynomials of the second kind ($U_n(x)$). In this post we are going to focus on the Chebyshev polynomials of the first kind.

# Chebyshev Polynomials of the First Kind

There are many different ways to define the Chebyshev polynomials of the first kind. The one that seems most logical to me and most useful in terms of outlining various properties of the polynomials is

$$\label{eq:1}
T_{n}(x) = \cos{\left(n \arccos{x}\right)}, \quad x \in [-1, 1].\tag{1}
$$

Looking at \eqref{eq:1} it is not obvious why $T_{n}(x)$ would be a polynomial. In order to show it is indeed a polynomial let's recall the de Moivre's formula

$$
\cos{(n \theta)} + i\sin{(n \theta)} = (\cos(\theta) + i \sin{\theta})^n.
$$

We can apply binomial expansion and take the real part from it to obatin

$$\label{eq:2}
\cos(n \theta) = \sum_{k = 0}^{\frac{n}{2}} C(n, 2k) (-1)^k \cos^{n - 2k}\theta \sin^{2k}{\theta}. \tag{2}
$$

where 

$$
C(n, 2k) = \frac{n!}{(2k)!(n-2k)!}, \quad n \geq 2k, k \in N, n \in N
$$ 

denotes the binomal coefficient. We can also notice that

$$
\sin^{2k}\theta = (\sin^2{\theta})^k = (1 - \cos^2{\theta})^k,
$$

showing that \eqref{eq:2} is a polynomial of $\cos{\theta}$ of degree $n$. Now, let

$$
\theta = \arccos{x},
$$

and by utilising $\cos{\left(\arccos{x}\right)} = x$ we get

$$
x = \cos{\theta}.
$$

This transforms \eqref{eq:1} to 

$$\label{eq:3}
T_{n}(\cos{\theta}) = \cos{\left(n \theta\right)} \tag{3}
$$

which we already showed is a polynomial of degree $n$. From here, because $\cos(.)$ is an even function, we can note that

$$
T_{n}(x) = T_{-n}(x) = T_{|n|}(x.)
$$

From \eqref{eq:3} it is also obvious that the values of $T_n$ in the interval $[-1, 1]$ are bounded in $[-1, 1]$ because of the cosine.

## Chebyshev Nodes of the First Kind

Before we continue with exploring the roots of the polynomials, let's recall some trigonometry. 

---

The **unit circle** is a circle with a radius of 1, centered at the origin of the Cartesian coordinate system. Below is shown part of the unit circle corresponding to the region from $0$ to $\frac{\pi}{2}$.

<center>
![alt text](/images/2025-01-06-chebyshev-polynomials/unit_circle.svg){ class="zoomable" style="display: block; margin: 0 auto"}
</center>

The cosine of an angle $\theta$ corresponds to the $x$-coordinate of the point where the terminal side of the angle (measured counterclockwise from the positive $x$-axis) intersects the unit circle. In other words, $\cos(\theta)$ gives the horizontal distance from the origin to this intersection point. 

The **arccosine** is the inverse function of cosine, and it maps a cosine value back to its corresponding angle in the range $[0, \pi]$ radians. For a given $x$-coordinate on the unit circle, the arccosine gives the angle $\theta$ such that $\cos(\theta) = x$, meaning

$$
\arccos(x) = \theta, \quad \text{where } \theta \in [0, \pi].
$$

Moreover, a **radian** is defined as the angle subtended at the center of a circle by an arc whose length is equal to the radius of the circle. For any circle, the length of an arc $s$ is given by

$$
s = r \cdot \theta,
$$

where $r$ is the radius of the circle, $\theta$ is the angle subtended by the arc at the center. This means that on the unit circle the length of the arc equals the measure of the angle in radians because $r = 1$, and hence

$$
s = \theta.
$$

---

Now, let's find the roots of the polynomial $T_{n}(x)$. If we take the definition in \eqref{eq:1} we have to solve

$$
\cos{\left(n \arccos{x}\right)} = 0, k \in N.
$$

The solutions in the interval $(-1, 1)$ are given by

$$
x_k = \cos{\left(\frac{2k - 1}{2n}\pi\right)}, n \in N, k = 1, 2, ...n.
$$

These roots are known as the **Chebyshev nodes of the first kind**, or the **Chebyshev zeros**. If we are working with an arbitrary interval $(a, b)$ the affine transformation 

$$
x_k = \frac{a + b}{2} + \frac{b - a}{2}\cos{\left(\frac{2k - 1}{2n}\pi\right)}, n \in N, k = 1, 2, ...n
$$

is needed. From the cosine properties we can also note that the nodes are symmetric with respect to the midpoint of the interval, and that the extrema of $T_n(x)$ over the interval $[-1, 1]$ alternate between $-1$ and $1$. Also, a very useful fact is that these nodes are used in polynomial interpolation to minimize the **Runge phenomenon**.

In the figure below we have shown the roots of $T_{8}(x)$ in blue. We have also built the perpendiculars from the roots to their interesction with the upper half of the unit circle, and marked these points in red.

<center>
![alt text](/images/2025-01-06-chebyshev-polynomials/chebyshev_nodes_visualization.svg){ class="zoomable" width=45% }![alt text](/images/2025-01-06-chebyshev-polynomials/chebyshev_nodes.png){ class="zoomable" width=45% }
</center>

Looking at the figure we can notice that the arc lengths between the red points seem to be of the same length. Let's show that this is indeed the truth.

We showed the roots are the cosine functions $\cos{\left(\frac{2k - 1}{2n}\pi\right)}, n \in N, k = 1, 2, ...n$. Thus, in the unit circle we have that the length of the corresponding arcs are equal to $\left( \frac{2k - 1}{2n}\pi \right), n \in N, k = 1, 2, ...n$. Let's take two red points which are direct neighbours, or in other words let's take two red points corresponding to the randomly chosen $m$ and $m + 1$ roots, $m \in k = \{1, 2, ..., n\}$. If we subtract them we are going to determine the length of the arc between them. We have

$$
\frac{2(m + 1) - 1}{2n}\pi - \frac{2m - 1}{2n}\pi = \frac{\pi}{n},
$$

meaning that between every two nodes the arc length is equal and has a value of $\frac{\pi}{n}$. A polynomial of degree $n$ has $n$ roots, which in our case are in the open interval $(-1, 1)$, meaning the arcs corresponding to every two neighbouring roots are $n - 1$, and the two arcs between the $x$-axis and the first and last roots due to the symmetry of roots have lenghts of

$$
\frac{1}{2}\left(\pi - \frac{n-1}{n}\pi\right) = \frac{\pi}{2n}.
$$

## Recurrence relation

This is probably a bit out of nowhere, but let's take a look at the following trigonometric identity

$$\label{eq:4}
\cos{\left((n + 1)\theta\right)} + \cos{\left((n - 1)\theta\right)} = 2 \cos{(\theta)} \cos{(n\theta)},\tag{4}
$$

and show that the left side indeed is equal to the right one. We are going to need the following two fundamental formulas of angle addition in trigonometry

$$
\cos{(\alpha + \beta)} = \cos{\alpha} \cos{\beta} - \sin{\alpha} \sin{\beta},
$$

and

$$
\cos{(\alpha - \beta)} = \cos{\alpha} \cos{\beta} + \sin{\alpha} \sin{\beta}.
$$

In our case we have

$$
\cos{\left((n + 1)\theta\right)} = \cos{\left(n\theta + \theta\right)} = \cos{(n\theta)} \cos{\theta} - \sin{(n\theta)} \sin{\theta},
$$

and

$$
\cos{\left((n - 1)\theta\right)} = \cos{\left(n\theta - \theta\right)} = \cos{(n\theta)} \cos{\theta} + \sin{(n\theta)} \sin{\theta}.
$$

Adding the above equations leads to the wanted result.

Now, we can see that the terms of \eqref{eq:4} are exactly in the form of the right side of \eqref{eq:1}, \eqref{eq:3}, hence we get

$$
T_{n + 1}(x) + T_{n - 1}(x) = 2T_{n}(x)T_{1}(x),
$$

or we get the useful **recurrence relation**

$$\label{eq:5}
T_{n + 1}(x) - 2xT_{n}(x) + T_{n - 1}(x) = 0.\tag{5}
$$

This relation along with adding $T_{0}(x) = 1$ and $T_{1}(x) = x$ is another famous way to define the Chebyshev polynomials of the first kind, or

$$
\left\{\begin{align*}
T_{0}(x) = 1, \\
T_{1}(x) = x, \\
T_{n + 1}(x) - 2xT_{n}(x) + T_{n - 1}(x) = 0.
\end{align*}\right.\label{eq:6}\tag{6}
$$

Let's write the first $6$ polynomials by using \eqref{eq:6}:

$$
\left\{\begin{align*}
T_{0}(x) = 1, \quad \text{(even)}\\
T_{1}(x) = x, \quad \text{(odd)}\\
T_{2}(x) = 2x^2 - 1, \quad \text{(even)}\\
T_{3}(x) = 4x^3 - 3x, \quad \text{(odd)}\\
T_{4}(x) = 8x^4 - 8x^2 + 1, \quad \text{(even)}\\
T_{5}(x) = 16x^5 - 20x^3 + 5x. \quad \text{(odd)}
\end{align*}\right.
$$

We can notice that

$$
T_{k}(x) = 2^{k-1}x^k + ...,
$$

and $T_{k}(x)$ is alternating between an even and an odd polynomial depending on whether $k$ is even or odd respectively.

Before we continue with some visualisations and more facts, let's mention that an interesting way to represent the recurrence relation \eqref{eq:5} is via the determinant

$$
T_{k}(x) = \det \begin{bmatrix}
x & 1 & 0 & \dots & 0 \\
1 & 2x & 1 & \ddots & \vdots \\
0 & 1 & 2x & \ddots & 0 \\
\vdots & \ddots & \ddots & \ddots & 1 \\
0 & \dots & 0 & 1 & 2x
\end{bmatrix}.
$$

Now, let's visualise the first $8$ polynomials.

![Chebyshev Polynomials](/images/2025-01-06-chebyshev-polynomials/chebyshev_polynomials.png){ class="zoomable" style="display: block; margin: 0 auto" }

But what can we notice if we stack them together?

![Chebyshev Polynomials Stacked](/images/2025-01-06-chebyshev-polynomials/chebyshev_polynomials_stacked.png){ class="zoomable" style="display: block; margin: 0 auto"}

It is quite obvious that at the roots of the $N$-th Chebyshev polynomial there is an **aliasing** effect, meaning higher order polynomials look like lower order ones. We can formally show it by fixing $N$, at the roots $x_k$ of $T_{N}(x) = 0$, and using the Chebyshev identity

$$
\cos{\left((m + N)\theta\right)} + \cos{\left((m - N)\theta\right)} = 2\cos{(m\theta)}\cos{(N\theta)},
$$

or equivalently

$$
T_{m + N}(x) + T_{m - N}(x) = 2T_{m}(x)T_{N}(x).
$$

Now, having $T_{N}(x) = 0$ leads to

$$
T_{m + N}(x) = -T_{m - N}(x).
$$

If we consecutevly set $m = N$, $m = 2N$, ..., $m = 6N$, etc. we would get

$$
\left\{\begin{align*}
T_{2N}(x_k) = -T_{0}(x_k) = -1, \\
T_{3N}(x_k) = 0, \\
T_{4N}(x_k) = 1, \\
T_{5N}(x_k) = 0, \\
T_{6N}(x_k) = -1, \\
\text{etc}.
\end{align*}\right.
$$

We can safely say that any higher-order Chebyshev polynomial $T_{N}(x)$ can be reduced to a lower-order $j, 0 \leq j \leq N$ Chebyshev polynomial at the sample points $x_k$ which are the roots of $T_{N}(x)$. In the figure below we attempt to visualise this statement.

![alt text](/images/2025-01-06-chebyshev-polynomials/reduction.svg){ class="zoomable" style="display: block; margin: 0 auto"}

The horizontal axis represents the order of Chebyshev polynomials, and the blue wavy line represents a "folded ribbon". Think of it as taking the sequence of polynomial orders and folding it back and forth. This folding happens at specific points where higher-order polynomials can be reduced to lower-order ones, which are the red **x** marks showing the sample points: the roots of $T_n(x)$. The key insight is that at these special sample points, we don't need to work with the higher-order polynomials because we can use equivalent lower-order ones instead. This is incredibly useful in numerical computations as it can help reduce computational complexity, and makes the Chebyshev polynomials very computationally efficient.

Let's illustarte this with a simple example. Let $N = 2$, then for even $m$ we have

$$
\left\{\begin{align*}
T_{4}(x_k) = -T_{0}(x_k) = -1, \\
T_{6}(x_k) = - T_{2}(x_k) = 0, \\
T_{8}(x_k) = - T_{4}(x_k) = 1, \\
T_{10}(x_k) = -T_{6}(x_k) = 0,  \\
\text{etc}.
\end{align*}\right.
$$

In the figure below we can see the even polynomials and that indeed $T_{10}(x)$ behaves like $-T_{6}(x)$ which behaves like $T_{2}(x)$ at the roots having value $0$, $T_{8}(x)$ behaves like $-T_{4}(x)$ at the roots with value $1$ as in $T_{0}(x)$, $T_{6}(x)$ behaves like $-T_{2}(x)$ with value $0$, and $T_{4}(x)$ behaves like $-T_{0}(x)$ with value $-1$.

{% include_code_collapsible 2025-01-06-chebyshev-polynomials/chebyshev_polynomials_aliasing_even.py lang:python :hideall: %}

![alt text](/images/2025-01-06-chebyshev-polynomials/chebyshev_polynomials_aliasing_even.png){ class="zoomable" style="display: block; margin: 0 auto"}

For odd $m$ we have
$$
\left\{\begin{align*}
T_{3}(x_k) = - T_{1}(x_k) = - x\\
T_{5}(x_k) = - T_{3}(x_k) = x\\
T_{7}(x_k) = - T_{5}(x_k) = -x, \\
T_{9}(x_k) = - T_{7}(x_k) = x, \\
\text{etc}.
\end{align*}\right.
$$

In the figure below we can see the odd polynomials and the aliasing as in the previous example.

{% include_code_collapsible 2025-01-06-chebyshev-polynomials/chebyshev_polynomials_aliasing_odd.py lang:python :hideall: %}

![alt text](/images/2025-01-06-chebyshev-polynomials/chebyshev_polynomials_aliasing_odd.png){ class="zoomable" style="display: block; margin: 0 auto"}

## Radial Plots

An interesting plot can be observed by plotting $T_n(x)$ radially. This means that instead of evaluating the polynomials over $[-1, 1]$ in a Cartesian plane we are evaluating them at $\frac{\theta}{\pi} - 1$, and plotting $r = n + T_n(\frac{\theta}{\pi} - 1)$ on polar axes. In other words, the input domain has been shifted and extended, and the results are drawn as radial distances $r$ around a circle defined by $\theta$. This creates a polar visualization where each $n$ produces a distinct spiral-like ornament. We are also filling in the areas between the curves for a visual effect.

{% include_code_collapsible 2025-01-06-chebyshev-polynomials/polar_plot.py lang:python :hideall: %}

![alt text](/images/2025-01-06-chebyshev-polynomials/polar_init_1.png){ class="zoomable" width=50% }![alt text](/images/2025-01-06-chebyshev-polynomials/polar_init_2.png){ class="zoomable" width=41% }

More visualusations can be achieved by doing other domain changes. They can be seen below.

![alt text](/images/2025-01-06-chebyshev-polynomials/polar_0.png){ class="zoomable" width=25% }![alt text](/images/2025-01-06-chebyshev-polynomials/polar_1.png){ class="zoomable" width=25% }![alt text](/images/2025-01-06-chebyshev-polynomials/polar_2.png){ class="zoomable" width=25% }![alt text](/images/2025-01-06-chebyshev-polynomials/polar_3.png){ class="zoomable" width=25% }

![alt text](/images/2025-01-06-chebyshev-polynomials/polar_4.png){ class="zoomable" width=25% }![alt text](/images/2025-01-06-chebyshev-polynomials/polar_5.png){ class="zoomable" width=25% }![alt text](/images/2025-01-06-chebyshev-polynomials/polar_6.png){ class="zoomable" width=25% }![alt text](/images/2025-01-06-chebyshev-polynomials/polar_7.png){ class="zoomable" width=25% }

![alt text](/images/2025-01-06-chebyshev-polynomials/polar_8.png){ class="zoomable" width=25% }![alt text](/images/2025-01-06-chebyshev-polynomials/polar_9.png){ class="zoomable" width=25% }![alt text](/images/2025-01-06-chebyshev-polynomials/polar_10.png){ class="zoomable" width=25% }![alt text](/images/2025-01-06-chebyshev-polynomials/polar_11.png){ class="zoomable" width=25% }

In a separate post, Chebyshev Polynomials, Part 2, we are going to explore the Chebyshev polynomials of the second kind, and their relations to the polynomials of the first kind.
