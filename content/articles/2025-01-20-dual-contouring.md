---
Title: Dual Contouring
Date: 2025-01-20 07:00
Category: Mathematics
Tags: mathematics, geometry
Slug: 2025-01-20-dual-contouring
Status: draft
---

This post is going to cover the so called **Dual Contouring** introduced [here](https://www.cs.rice.edu/~jwarren/papers/dualcontour.pdf). Dual Contouring is a surface extraction technique that builds on ideas from methods like Marching Cubes but uses “dual” grid information to place vertices in cells based on Hermite data (i.e. both the intersection points of the isosurface with grid edges and the corresponding normals). The algorithm is particularly good at capturing sharp features and generating crack‐free meshes. In what follows, we are goig to walk through the main ideas and steps in detail.

# Introduction

Traditional methods like **Marching Cubes** compute the intersection of an isosurface with the edges of a uniform grid and then connect these intersection points based on a lookup table. In contrast, dual contouring:

- Collects **Hermite data** along cell edges—this data consists of both the point where the isosurface intersects an edge and the surface normal (the gradient) at that point.
- Places a vertex per cell (the “dual” vertex) by optimally fitting these intersection constraints via minimization of a **quadratic error function** (QEF).
- Constructs the mesh by connecting these vertices in the dual grid, ensuring that adjacent cells yield coherent connectivity.

This approach not only results in a lower polygon count but is also more adept at preserving sharp features (edges and corners) inherent in the underlying surface.

![DC vs MC](../images/2025-01-20-dual-contouring/dc_tee_comparison.svg){ style="display: block; margin: 0 auto"}

# Octree

What is an octree?

![Cube](../images/2025-01-20-dual-contouring/octree_cube.jpg){ width=60% style="display: block; margin: 0 auto"}

Octree:

![Octree](../images/2025-01-20-dual-contouring/octree.jpg){ width=50% style="display: block; margin: 0 auto"}

![Octree](../images/2025-01-20-dual-contouring/octree_p.png){ width=50% style="display: block; margin: 0 auto"}

TBD

Dual Contouring: 2D Circle Example

![alt text](../images/2025-01-20-dual-contouring/circle_grid.png){ width=75% style="display: block; margin: 0 auto" }

![alt text](../images/2025-01-20-dual-contouring/dc.png){ width=50% }![alt text](../images/2025-01-20-dual-contouring/dc_quad.png){ width=50% }

Dual Contouring 3D Sphere:

<iframe src="{static}/code/2025-01-20-dual-contouring/dc_3d.html" width="100%" height="600px" frameborder="10"></iframe>
