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

First, we should introduce some important theory. Let's begin by stating that two function $f_{1}(x)$ and $f_{2}(x)$ are orthogonal over the intevral $a \leq x \leq b$ if
$$
\int_a^b f_{1}(x) f_{2}(x) \mathrm{d}x = 0.
$$
