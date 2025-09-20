---
Title: Trigonometric Identities the Euler Way
Date: 2025-08-04 07:00
Category: Mathematics
Tags: trigonometry
Slug: trigonometric-identities
Status: published
---

I have always believed that mathematics is about thinking rather than memorizing. The trigonometric identities were among the things we were told to memorize at school, and not only I struggled with that but I also actively rebelled against this approach. For me, mathematics is fundamentally about having a minimal but sufficient set of definitions and axioms, understanding them deeply, and then deriving everything else from these foundations. During one of my Complex Analysis lectures in my undergraduate Applied Mathematics studies, I was introduced to Euler's formula. When I discovered how it could be used to derive some of the most important trigonometric identities, I was more than relieved. I could finally derive the identities easily whenever I needed them, instead of relying on rote memorization, or panicking about my failure to memorize them.

# Euler's Formula

**Euler's formula** states that for any real number $\theta$,

$$\label{eq:1}
e^{i \theta} = \cos\theta + i \sin\theta, \tag{1}
$$

where $i$ is the imaginary unit, defined as $i^2 = -1$. The formula has a geometric interpretation in the complex plane that provides insight into trigonometry and complex numbers, **Figure 1**.

<figure>
  <img src="../images/2025-08-04-trigonometric-identities/Euler's_formula.svg" alt="Euler" class="zoomable" style="display: block; margin: 0 auto; width: 35%">
  <figcaption style="text-align: center">Figure 1. Euler's formula in the complex plane</figcaption>
</figure>

In **Figure 1**, the horizontal axis represents the real part, the vertical axis represents the imaginary part, and any complex number $z = x + i y$ is plotted as the point $(x, y)$. Euler's formula represents a point on the unit circle at angle $\theta$ from the positive real axis, where:

- **Real part**: $\cos\theta$ (horizontal coordinate)
- **Imaginary part**: $\sin\theta$ (vertical coordinate)
- **Magnitude**: $|e^{i\theta}| = \sqrt{\cos^2\theta + \sin^2\theta} = 1$

As $\theta$ varies from $0$ to $2\pi$, the point $e^{i\theta}$ traces out the entire unit circle. The famous **Euler's identity** emerges naturally:

$$
e^{i \pi} = \cos(\pi) + i \sin(\pi) = -1 + 0 i = -1,
$$

or

$$
e^{i \pi} + 1 = 0.
$$

Now, let's go back to $\eqref{eq:1}$. We know that $\cos(x)$ is an even function, meaning $\cos(-x) = \cos(x)$, and $\sin(x)$ is an odd function, meaning $\sin(-x) = -\sin(x)$. Using that, we can derive the following identity:

$$\label{eq:2}
e^{-i \theta} = e^{i (-\theta)} = \cos(-\theta) + i \sin(-\theta) = \cos\theta - i \sin\theta. \tag{2}
$$

# Cosine and Sine Expressions

If we add $\eqref{eq:1}$ and $\eqref{eq:2}$, we can derive the cosine function:

$$\label{eq:3}
\cos\theta = \frac{e^{i\theta} + e^{-i\theta}}{2}. \tag{3}
$$

If we subtract $\eqref{eq:2}$ from $\eqref{eq:1}$, we can derive the sine function:

$$\label{eq:4}
\sin\theta = \frac{e^{i\theta} - e^{-i\theta}}{2i}. \tag{4}
$$

# Angle Addition Formulas

Let's say we want to derive the angle addition formulas for sine and cosine using Euler's formula. We start with

$$
e^{i(\alpha + \beta)}  = e^{i\alpha + i\beta} = e^{i\alpha} e^{i\beta}.
$$

Applying the Euler's formula to the left side, we have:

$$
e^{i(\alpha + \beta)} = \cos(\alpha + \beta) + i \sin(\alpha + \beta).
$$

Now, applying the Euler's formula to the right side, we have:

$$
e^{i\alpha} e^{i\beta} = (\cos\alpha + i \sin\alpha)(\cos\beta + i \sin\beta) =
$$

$$
= \cos\alpha \cos\beta - \sin\alpha \sin\beta + i (\sin\alpha \cos\beta + \cos\alpha \sin\beta).
$$

Equating the real parts of the above two expressions, we get the **cosine addition formula**

$$
\cos(\alpha + \beta) = \cos\alpha \cos\beta - \sin\alpha \sin\beta.
$$

Equating the imaginary parts, we get the **sine addition formula**

$$
\sin(\alpha + \beta) = \sin\alpha \cos\beta + \cos\alpha \sin\beta.
$$

# Product-to-Sum Formulas

Let's derive the identity for the product of cosine and cosine functions. Using $\eqref{eq:3}$ and $\eqref{eq:4}$, we have

$$
\cos\alpha \cos\beta = \frac{1}{4}\left(e^{i\alpha} + e^{-i\alpha}\right)\left(e^{i\beta} + e^{-i\beta}\right) =
$$

$$
= \frac{1}{4}\left[e^{i(\alpha + \beta)} + e^{i(\alpha - \beta)} + e^{-i(\alpha - \beta)} + e^{-i(\alpha + \beta)}\right] =
$$

$$
= \frac{1}{2}\left[\cos(\alpha + \beta) + \cos(\alpha - \beta)\right].
$$

# Conclusion

The key advantage of using Euler's formula is that it transforms trigonometric problems into algebraic manipulations with exponentials, and I find this beautiful.
