---
Title: Lissajous Curves
Date: 2025-04-22 07:00
Category: Mathematics
Tags: mathematics, python
Slug: 2025-04-22-lissajous-curves
Status: draft
---

Lissajous (/ˈlɪsəʒuː/) curves or also Lissajous figures or even Bowditch curves are the family of curves described by the following parametric equations

$$
x(t)	=	A \cos{\left(\omega_x t - \delta_x\right)} \\
y(t)	=	B \cos{\left(\omega_y t - \delta_y\right)}
$$

sometimes also written in the form

$$
x(t)	=	a \sin{\left(\omega t + \delta\right)} \\
y(t)	=	b \sin{t}.
$$

Lissajous curves find applications in physics, astronomy, and other sciences.

# Introduction

# Connection between Lissajous Curves and Chebyshev Polynomials

## Padua Points

# Lissajous Knots

# Spherical Lissajous Curves

# Aerial Search Patterns

# Planning Multi-Agent Trajectories

# Lissajous Curves

## Introduction  
**Definition:** A *Lissajous curve* (or *Bowditch curve*) is the trajectory of a point defined by two perpendicular harmonic motions. In a typical parametric form, one can write: 

\[ x(t) = A\cos(a t + \delta), \qquad y(t) = B\sin(b t), \] 

where $A, B$ are amplitudes, $a, b$ are frequencies (constants), and $\delta$ is a phase shift ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=A%20Lissajous%20curve%20%2F%20%CB%88,a%20system%20of%20parametric%20equations)). An equivalent form uses sine on both axes (since a cosine is just a sine with phase shift). For example, another common parametrization is $x(t) = A\sin(a t + \delta), \; y(t) = B\sin(b t)$ ([ Lissajous curves - Jose M Sallan blog ](https://jmsallan.netlify.app/blog/liisajous-curves/#:~:text=A%20Lissajous%20curve%20is%20a,parametric%20equations%20of%20the%20form)). In either case, the resulting curve is the superposition of two sinusoidal oscillations along $x$ and $y$ axes, generally tracing a closed figure in the rectangle $[-A,A]\times[-B,B]$. 

**Basic Properties:** The appearance of a Lissajous figure is governed by the frequency ratio $a:b$ and the phase $\delta$. If the ratio $a/b$ is a rational number (say $p/q$ in lowest terms), the curve is closed (it eventually repeats) ([ Lissajous curves - Jose M Sallan blog ](https://jmsallan.netlify.app/blog/liisajous-curves/#:~:text=Lissajous%20curves%20represent%20complex%20harmonic,vertical%20and%20horizontal%20lobes%2C%20respectively)) ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=motion%20and%20so%20the%20ellipse,%E2%81%A0a%2Fb%E2%81%A0%20is%20rational)). In fact, such a rational ratio produces a stationary pattern on an oscilloscope. If $a/b$ is irrational, the curve never exactly closes; instead, it densely fills a region, often appearing to continuously precess or rotate ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=Visually%2C%20the%20ratio%20%E2%81%A0a%2Fb%E2%81%A0%20determines,For%20example%2C%20%CE%B4%20%3D%200)). The case $a:b = 1:1$ yields an ellipse (special cases: a straight line when $\delta=0$, or a circle when $A=B$ and $\delta=\pi/2$) ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=The%20appearance%20of%20the%20figure,%E2%81%A0a%2Fb%E2%81%A0%20is%20%20103)). More generally, the ratio determines the number of lobes: for example, $a:b = 3:1$ produces three large lobes, $5:4$ produces a pattern with five horizontal lobes and four vertical lobes ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=Visually%2C%20the%20ratio%20%E2%81%A0a%2Fb%E2%81%A0%20determines,For%20example%2C%20%CE%B4%20%3D%200)). (In a Lissajous parametric equation as above, the integer $a$ typically corresponds to lobes along the horizontal direction, and $b$ to lobes vertically.) The amplitudes $A,B$ simply scale the figure’s width and height ([ Lissajous curves - Jose M Sallan blog ](https://jmsallan.netlify.app/blog/liisajous-curves/#:~:text=Lissajous%20curves%20represent%20complex%20harmonic,vertical%20and%20horizontal%20lobes%2C%20respectively)), and the phase $\delta$ effectively rotates or slants the figure in the plane ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=The%20ratio%20%E2%81%A0A%2FB%E2%81%A0%20determines%20the,depending%20on%20the%20ratio%20%E2%81%A0a%2Fb%E2%81%A0)). 

**Example:** For $a=3, b=2$ and phase $\delta=\pi/2$, one obtains a closed Lissajous curve with three horizontal loops and two vertical loops.  ([image]()) *Lissajous curve for frequency ratio $3:2$ and phase $\pi/2$. This figure has 3 lobes along the $x$-axis and 2 along $y$, illustrating a typical closed Lissajous figure.* The curve repeats every $2\pi$ in $t$ since $3:2$ is rational. If we were to slightly detune one frequency (making the ratio irrational), the path would not close; it would wind indefinitely, covering the area inside the bounding box over time (a property useful for scanning or search patterns, as discussed later).

## Connection between Lissajous Curves and Chebyshev Polynomials  
Lissajous figures have a deep connection to **Chebyshev polynomials** through trigonometric identities. In particular, if one of the Lissajous frequencies is an integer multiple of the other, the curve can be associated with a Chebyshev polynomial of that degree ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=Lissajous%20figures%20where%20a%20%3D,and)). For instance, consider a Lissajous parametric equation with $a=1$ and $b=N$ (and choose phases such that $x=\cos t$, $y=\cos(Nt)$ for convenience). Using the identity $\cos(Nt) = T_N(\cos t)$, where $T_N(x)$ is the Chebyshev polynomial of the first kind of degree $N$, we see that the curve satisfies $y = T_N(x)$. In other words, the parametric equations 

\[x = \cos t, \qquad y = \cos(Nt)\]

trace out the graph of the Chebyshev polynomial $T_N(x)$ ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=The%20relation%20of%20some%20Lissajous,functions%20rather%20than%20sine%20functions)). The resulting Lissajous figure is an algebraic curve of degree $N$ in the $xy$-plane. For example, with $N=5$, the elimination of the parameter $t$ yields the implicit polynomial equation $16x^5 - 20x^3 + 5x - y = 0$ (since $T_5(x)=16x^5-20x^3+5x$). The figure below demonstrates this relationship: the points generated by $x=\cos t,\;y=\cos(5t)$ lie exactly on the curve $y=T_5(x)$ in the interval $-1\le x \le 1$. 

 ([image]()) *Parametric plot (orange points) of $x=\cos t$, $y=\cos(5t)$, which corresponds to a Lissajous figure with ratio $1:5$. The blue curve is $y=T_5(x)=16x^5-20x^3+5x$. The parametric Lissajous points perfectly satisfy the Chebyshev polynomial equation ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=Lissajous%20figures%20where%20a%20%3D,and)).* 

This connection arises from the trigonometric identity $\cos(Nt) = T_N(\cos t)$ and shows that certain Lissajous figures can be seen as graphical representations of Chebyshev polynomials. The Chebyshev polynomials themselves are crucial in approximation theory (minimizing error on $[-1,1]$) and have many theoretical properties. Here, the Lissajous perspective provides a geometric insight: as $t$ runs from $0$ to $2\pi$, the Lissajous curve $x=\cos t,\;y=\cos(Nt)$ oscillates $N$ times in the vertical direction for each single oscillation in the horizontal direction, producing the $N$-th degree Chebyshev waveform in $y$ vs $x$. 

## Padua Points  
The **Padua points** are a set of points in the unit square that are important in bivariate polynomial interpolation. Remarkably, they can be generated from Lissajous curves ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=Lissajous%20figures%20where%20a%20%3D,and)). In fact, the Padua points (for a given total degree $n$) correspond to the intersection points of a particular Lissajous figure that oscillates $n$ and $n+1$ times along the two axes ([Padua points - Wikipedia](https://en.wikipedia.org/wiki/Padua_points#:~:text=The%20generating%20curve%20of%20Padua,of%20the%20first%20family%20is)) ([Padua points - Wikipedia](https://en.wikipedia.org/wiki/Padua_points#:~:text=The%20generating%20curve%20of%20Padua,of%20the%20third%20family%20is)). One way to define the *generating curve* for Padua points of degree $n$ is: 

\[ \gamma_{1}(t) = \big(-\cos((n+1)t),\; -\cos(nt)\big), \qquad t\in[0,\pi]. \] 

This is a Lissajous curve with frequency ratio $(n+1):n$. As $t$ runs from $0$ to $\pi$, the curve $\gamma_1(t)$ intersects itself at certain points inside the square $[-1,1]\times[-1,1]$. These self-intersection points (together with some boundary points) are exactly the Padua points for total degree $n$ ([Padua points - Wikipedia](https://en.wikipedia.org/wiki/Padua_points#:~:text=match%20at%20L161%20points%20lie,4)). By sampling the function to be interpolated at those intersection points, one obtains an interpolation scheme with near-optimal properties (Padua points are known to have minimal growth of the Lebesgue constant) ([Padua points - Wikipedia](https://en.wikipedia.org/wiki/Padua_points#:~:text=In%20polynomial%20interpolation%20%20of,2)) ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=Lissajous%20figures%20where%20a%20%3D,and)). 

 ([image]()) *Padua points for $n=5$ (red crosses), generated by the Lissajous curve $x=-\cos(6t),\;y=-\cos(5t)$ shown as a dashed loop. The $5\times 6=30$ interior intersection points (and one additional boundary point) form the Padua set for degree 5 ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=Lissajous%20figures%20where%20a%20%3D,and)). Such points provide an optimal node set for bivariate polynomial interpolation in $[-1,1]^2$. Note how the Lissajous curve passes through every red point.*  

In summary, certain Lissajous curves (sometimes called *Lissajous-Chebyshev* curves in this context) provide a convenient parameterization of the Padua points ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=Lissajous%20figures%20where%20a%20%3D,and)). This ties together harmonic motion with polynomial interpolation theory: the trigonometric sampling via Lissajous figures yields nodes that mirror the tensor-product Chebyshev nodes in a two-dimensional, scattered fashion, enabling stable interpolation and quadrature on a square domain.

## 3D Lissajous Curves  
One can extend the concept of Lissajous figures to three dimensions by introducing a third harmonic motion. A *3D Lissajous curve* is given by parametric equations in $\mathbb{R}^3$, for example: 

\[ x(t) = A\cos(n_x t + \phi_x), \qquad 
   y(t) = B\cos(n_y t + \phi_y), \qquad 
   z(t) = C\cos(n_z t + \phi_z), \] 

with $n_x, n_y, n_z$ being frequency parameters (often integers) and $\phi_x,\phi_y,\phi_z$ phase offsets ([Lissajous knot - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_knot#:~:text=Image%3A%20,21%7D%20knot)). This represents a point moving in 3D whose $x$, $y$, $z$ coordinates each undergo independent sinusoidal oscillations. The projections of this space curve onto the coordinate planes are classic 2D Lissajous figures ([Lissajous knot - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_knot#:~:text=The%20projection%20of%20a%20Lissajous,to%20properties%20of%20Lissajous%20curves)). 

The geometry of 3D Lissajous curves is rich. If the frequency ratios $n_x:n_y:n_z$ are rational, the curve will eventually close in 3D, forming a closed loop in space (possibly after multiple oscillation cycles). If at least one of the ratios is irrational, the path will never exactly repeat, tending to densely fill a volume or surface region over time (in practice, it will appear as a thick “tube” as the curve comes arbitrarily close to every point in some region). The shape of a 3D Lissajous curve can range from simple toroidal or helical loops to very complex knotted structures, depending on the frequencies and phases. The figure below shows an example of a 3D Lissajous curve for frequencies $(9,4,1)$: the $x$ oscillates 9 times, $y$ 4 times, and $z$ once for the fundamental period. 

 ([File:3D Lissajous figure (9, 4, 1).jpg - Wikipedia](https://en.wikipedia.org/wiki/File:3D_Lissajous_figure_(9,_4,_1).jpg)) *Example of a 3D Lissajous figure with frequency ratio $9:4:1$. The curve winds in three dimensions, and its projections on the $xy$, $xz$, and $yz$ planes are Lissajous figures. When viewed from certain angles, such a curve may appear as a twisted lobe or a 3D knot-like shape.* 

Analytically, 3D Lissajous curves can be understood as a special case of **3D Fourier curves** (where only one frequency component is present in each coordinate). They are sometimes used in physics demonstrations and art due to their intricate shapes. When parametrized with integer frequency ratios, these curves lie on a torus (the product of circles in each coordinate). In fact, a 3D Lissajous with rational ratios can be seen as a closed loop embedded on the surface of a torus in $\mathbb{R}^3$. This viewpoint is what leads to the notion of *Lissajous knots*, discussed next.

## Lissajous Knots  
In knot theory, a *Lissajous knot* is defined as a closed 3D Lissajous curve whose frequencies are all integers ([Lissajous knot - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_knot#:~:text=Image%3A%20,21%7D%20knot)). Concretely, a Lissajous knot has parametric equations:

\[ x(t) = \cos(n_x t + \phi_x), \qquad 
   y(t) = \cos(n_y t + \phi_y), \qquad 
   z(t) = \cos(n_z t + \phi_z), \] 

with $n_x, n_y, n_z$ integers, and it forms a **knot** (a non-self-intersecting closed loop in 3D). All three planar projections of such a curve ($xy$, $yz$, and $xz$ projections) are 2D Lissajous figures ([Lissajous knot - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_knot#:~:text=The%20projection%20of%20a%20Lissajous,to%20properties%20of%20Lissajous%20curves)). Not every choice of $(n_x,n_y,n_z,\phi_x,\phi_y,\phi_z)$ yields a non-self-intersecting knot; certain conditions must hold. In particular, for the curve to be a knot (no self-intersections), the frequencies should be pairwise coprime (sharing no common divisors) and the phase differences must be incommensurate with $\pi$ (to avoid the curve lying in a plane) ([Lissajous knot - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_knot#:~:text=Because%20a%20knot%20cannot%20be,and%20none%20of%20the%20quantities)). Essentially, if $n_x, n_y, n_z$ have a common factor, or if the phases are too “rational” relative to $\pi$, the curve might intersect itself or even simplify to a planar curve. Under appropriate conditions, however, one obtains a true knot in 3D space. For example, one famous Lissajous knot is given by $(n_x,n_y,n_z)=(3,2,7)$ with certain phase choices, which produces a knot of a particular topological type ([Lissajous knot - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_knot#:~:text=Here%20are%20some%20examples%20of,z%7D%3D0)). 

 ([image]()) *A Lissajous knot (specifically the $8_{21}$ knot) generated by $x=\cos(3t+0.7),\,y=\cos(2t+0.2),\,z=\cos(7t)$ ([Lissajous knot - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_knot#:~:text=Here%20are%20some%20examples%20of,z%7D%3D0)). This closed 3D curve is non-self-intersecting and forms a knotted loop.* 

Topologically, Lissajous knots are a special family of knots that are highly symmetric. Research has shown that not all knots can be represented in Lissajous form; those that can are subject to certain parity constraints on their crossing numbers (often $n_x$ or $n_y$ must be odd for nontrivial knots, etc., as discussed in knot theory literature). Still, many small knots (knots with few crossings) are Lissajous. These knots are interesting because their harmonic parametrization makes them amenable to mathematical analysis. For instance, one can study their symmetry or Fourier spectrum (they have a single frequency in each coordinate). Lissajous knots also relate to so-called **Fourier knots**, which are more general Fourier-parametrized closed curves; in that sense, Lissajous knots are the simplest “harmonic” knots ([Lissajous and Fourier Knots](https://typeset.io/pdf/lissajous-and-fourier-knots-om4mjrxjbo.pdf#:~:text=Lissajous%20and%20Fourier%20Knots%20Fourier,BHJS%5D%29%20are%20the%20simplest)).

## Spherical Lissajous Curves  
A *spherical Lissajous curve* is a path traced on the surface of a sphere, driven by harmonic motion in two angular coordinates. One way to define it is in terms of spherical coordinates: for integers $m_1, m_2$, one can set the polar (colatitude) angle $\theta(t)$ and azimuthal angle $\varphi(t)$ to oscillate as $\theta(t)=m_2 t$ and $\varphi(t)=m_1 t - \alpha\pi$ for some phase $\alpha$ ([Wolfgang Erb | Spherical Lissajous Curves ](https://www.math.unipd.it/~erb/LSphere.html#:~:text=A%20spherical%20Lissajous%20curve%20is,and%20a%20longitudinal%20harmonic%20motion)). Mapping to Cartesian coordinates on the unit sphere $\mathbb{S}^2$, a spherical Lissajous curve can be written as: 

\[ 
x(t) = \sin(m_2 t)\cos(m_1 t - \alpha\pi), \qquad 
y(t) = \sin(m_2 t)\sin(m_1 t - \alpha\pi), \qquad 
z(t) = \cos(m_2 t), 
\] 

which indeed lies on $x^2+y^2+z^2=1$ for all $t$ ([Wolfgang Erb | Spherical Lissajous Curves ](https://www.math.unipd.it/~erb/LSphere.html#:~:text=A%20spherical%20Lissajous%20curve%20is,and%20a%20longitudinal%20harmonic%20motion)). Here $m_1$ controls the number of longitudinal oscillations (around the equator) and $m_2$ controls the number of latitudinal oscillations (from pole to pole). The result is a closed curve on the sphere that resembles a loxodrome or some “weaving” path on the spherical surface.

Just as in the planar case, the properties depend on the ratio $m_1:m_2$. If $m_1/m_2$ is rational, the spherical Lissajous will eventually close after a certain period, forming a closed loop on the sphere ([Wolfgang Erb | Spherical Lissajous Curves ](https://www.math.unipd.it/~erb/LSphere.html#:~:text=If%20the%20frequencies%20,and%20the%20period%20of)). If the ratio is irrational, the path will densely cover a band on the sphere. However, unlike planar Lissajous figures (which can self-intersect in the plane), a spherical Lissajous cannot self-intersect *on the sphere* unless it retraces its steps, because on a sphere any two distinct times give two distinct points unless the curve is periodic and closes. What can happen is that the curve may pass through itself in 3D space (one segment of the curve goes over or under another segment on the sphere), but this is not a true intersection on the surface.

Spherical Lissajous curves are of interest in understanding satellite ground tracks and other scenarios of motion on a spherical surface. They generalize the idea of great circle or loxodrome paths to oscillatory motions. The example below (left) shows a spherical Lissajous for $(m_1,m_2)=(6,5)$, which wraps around the sphere in a complex way, creating a lattice-like pattern of intersections on the sphere. 

 ([Wolfgang Erb | Spherical Lissajous Curves ](https://www.math.unipd.it/~erb/LSphere.html)) *A spherical Lissajous curve for $m_1=5, m_2=6, \alpha=0$ plotted on the unit sphere ([Wolfgang Erb | Spherical Lissajous Curves ](https://www.math.unipd.it/~erb/LSphere.html#:~:text=A%20spherical%20Lissajous%20curve%20is,and%20a%20longitudinal%20harmonic%20motion)). The curve oscillates 5 times around in longitude for 6 oscillations in latitude, creating a closed loop on the sphere with multiple self-crossings (blue points) when viewed in 3D. Such curves are studied for their intersection patterns ([Wolfgang Erb | Spherical Lissajous Curves ](https://www.math.unipd.it/~erb/LSphere.html#:~:text=Fig,7%2C6%29%7D_%7B0)).* 

Mathematically, spherical Lissajous curves can be studied by projecting them to a plane (e.g., via stereographic projection or simple cylindrical projection), relating them to planar Lissajous or **rhodonea (rose) curves**. They have a discrete set of self-intersection points determined by the frequency parameters ([Wolfgang Erb | Spherical Lissajous Curves ](https://www.math.unipd.it/~erb/LSphere.html#:~:text=,spherical%20Lissajous%20curves)). These intersection points on the sphere correspond to times when the two oscillatory motions “sync up” in certain ways. Counting and characterizing these intersections is a nontrivial problem in spherical geometry ([Wolfgang Erb | Spherical Lissajous Curves ](https://www.math.unipd.it/~erb/LSphere.html#:~:text=Corollary%202%20Let%20%5C%28%5Cmathrm,even.%20Then)).

## Aerial Search Patterns  
Lissajous curves find practical use in the design of efficient search patterns for unmanned aerial vehicles (UAVs) and other robotic agents. The idea is to exploit the property that a Lissajous path covers a rectangular area in a thorough but non-repetitive way. For search and surveillance, one often wants a path that eventually visits every region of an area without large gaps, and preferably in a pattern that can be systematically followed. A Lissajous curve (with appropriate frequency ratio and scaling) is a good candidate for this ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=fly%2C%20optimal%20deterministic%20search%20pattern,recently%20caught%20attention%20as%20excellent)). It produces a scanning trajectory that **sweeps the area** both horizontally and vertically in a cyclic manner. 

One advantage of using a Lissajous pattern is that it is deterministic and easily parameterized by a small number of parameters (the frequency ratio and phase). This makes it straightforward to generate and follow for an aircraft. Moreover, because Lissajous curves are always inscribed in a rectangle, one can fit a Lissajous pattern to a given rectangular search region ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=As%20Fig,of%20a%20rectangular%20search%20space)) by choosing $A, B$ to match the half-dimensions of the area. The phase $\delta$ can be adjusted to start the pattern at a corner or edge of the area, which is often practical for search (e.g. starting at a boundary of the search zone) ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=Open%20in%20a%20new%20tab)). The figure of the Lissajous path can also be rotated or translated to align with the search area if needed ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=The%20first%20original%20contribution%20of,and%20shifted%20in%202D%20space)).

A key parameter is the frequency ratio $a/b$. If $a/b$ is chosen to be **nearly rational**, the Lissajous path will come close to retracing itself periodically, which may cause certain regions to be visited repeatedly while leaving others less covered ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=pattern%20and%20any%20local%20maximum,frequency%20ratio%20is%20indicative%20of)). On the other hand, if $a/b$ is irrational (or a rational with a large denominator), the path will be more uniformly spread out. In fact, recent analyses have shown that *avoiding* low-order rational ratios improves search performance, since highly rational ratios lead to “spikes” of redundant coverage at the repeat interval ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=pattern%20and%20any%20local%20maximum,frequency%20ratio%20is%20indicative%20of)). An irrational ratio yields a more ergodic coverage of the area (the path eventually passes arbitrarily close to every point in the domain) at the cost of never exactly repeating. Designers often pick a ratio like $a/b \approx \phi$ (the golden ratio) or another irrational number to maximize uniform coverage ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=Effect%20of%20varying%20Lissajous%20frequency,%2C%20%2C)) ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=Open%20in%20a%20new%20tab)).

In a representative use-case, imagine a UAV that must search a $1 \times 1$ square area for a target with no prior location information. A Lissajous path can be planned such that the UAV oscillates in $x$ and $y$ within this square. Over time, the path will produce a dense coverage, reducing the longest time any given cell in the area goes unvisited. Analytical results have shown that the average distance from any random target to the searcher decreases as the Lissajous pattern progresses ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=the%20field%20in%20Lissajous%20curves,the%20average%20searcher%20speed%20was)) ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=pattern%20and%20any%20local%20maximum,frequency%20ratio%20is%20indicative%20of)). Furthermore, Lissajous patterns inherently have $90^\circ$ rotational symmetry in their coverage (when $a$ and $b$ are swapped, the pattern is rotated), which is useful when no directional bias is desired for the search ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=with%20near,frequency%20ratio%20is%20indicative%20of)). 

It is worth noting that Lissajous-based search is typically used for *systematic lawnmower-style searches* when on-board computation is limited or when one wants a predefined guarantee of coverage. In contrast to random or information-driven search patterns, a Lissajous pattern requires no real-time decision-making—an advantage for small UAVs with limited processing power ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=match%20at%20L246%20in%20aerial,is%20known%20or%20made%20available)). Recent research is exploring how to optimize Lissajous search patterns (e.g., adjusting frequencies, phases, or switching between patterns) to balance thoroughness and time efficiency ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=candidates%20for%20all%20kinds%20of,to%20establish%20the%20state%20of)). Overall, Lissajous curves provide a family of **cyclic, covering paths** that are analytically tractable and have proven useful for aerial search and survey missions.

## Planning Multi-Agent Trajectories  
When multiple robots or drones are deployed, coordinating their trajectories is critical to ensure efficient coverage and avoid collisions. Lissajous curves can serve as a foundation for multi-agent trajectory design by assigning agents to follow Lissajous paths in a synchronized manner. Two main strategies emerge:

**1. Shared Lissajous Formation:** All agents move along the *same* Lissajous curve, but spaced out in time (phase-shifted). For example, consider a team of drones patrolling a rectangular region following a Lissajous path with frequency ratio $a:b$. If there are $N$ drones, one can initialize them at equally spaced phase intervals (e.g., one at phase $0$, another at phase $2\pi/N$, etc.). They will all trace the same figure but will be at different points on the curve at any given time, effectively forming a moving “train” of agents. This achieves **complete and periodic coverage** of the area (the entire Lissajous figure is traced repeatedly), and by proper phase spacing one can guarantee **collision-free** operation since the agents never converge to the same point at the same time ([](https://arxiv.org/pdf/1812.04904#:~:text=and%20so%20on,detection%20of%20a%20rogue%20element)). In fact, prior work shows that if agents move with constant speed on a Lissajous path and are spaced by appropriate phase differences, they can patrol without ever getting too close, provided the agents’ size and speed are within certain limits ([](https://arxiv.org/pdf/1812.04904#:~:text=The%20prior%20work%20in%20,was%20de%02rived%20in%20order%20to)) ([](https://arxiv.org/pdf/1812.04904#:~:text=and%20so%20on,detection%20of%20a%20rogue%20element)). This setup also allows for **cooperative target detection**: if a moving target is somewhere in the area, at least one of the agents will eventually encounter it, and multiple agents can trap the target by approaching from different lobes of the Lissajous pattern ([](https://arxiv.org/pdf/1812.04904#:~:text=O1%20Complete%20and%20periodic%20coverage,detection%20of%20a%20rogue%20element)) (for instance, one strategy positions a “rogue element” or target at the center of the Lissajous figure, and the pattern ensures agents repeatedly encircle that center ([](https://arxiv.org/pdf/1812.04904#:~:text=and%20so%20on,detection%20of%20a%20rogue%20element))).

**2. Complementary Lissajous Paths:** Alternatively, different agents can be assigned different Lissajous patterns that complement each other. For example, one agent might take a pattern with ratio $a:b$, and another might take $b:a$ (swapping frequencies) or a pattern rotated by 90 degrees. Each agent covers the area in a distinct way, and together they achieve faster coverage. The challenge is to ensure the paths do not cause collisions at intersections. This can be handled by slight differences in frequency or phase offsets so that agents rarely, if ever, cross the same point simultaneously. Another approach is to partition the area and have each agent run a Lissajous search in its sub-region, effectively tiling the space with Lissajous trajectories.

Researchers have proposed trajectory planning algorithms that utilize Lissajous curves for multi-agent systems. In one such approach, agents are constrained to a Lissajous path but can adjust their speed or wait at certain points to avoid conflicts, enabling **reconfiguration** of the formation when needed ([](https://arxiv.org/pdf/1812.04904#:~:text=This%20paper%20proposes%20trajectory%20planning,trajectories%20have%20been%20employed%20in)). For instance, agents can transition from one Lissajous formation to another (with different $a,b$) smoothly, by temporarily changing speed along the curve and then resuming patrol on the new curve ([](https://arxiv.org/pdf/1812.04904#:~:text=This%20paper%20proposes%20trajectory%20planning,trajectories%20have%20been%20employed%20in)). The benefits of Lissajous-based coordination include: (a) **Predictability** – each agent’s route is known and periodic, simplifying coordination; (b) **Coverage guarantees** – the pattern ensures every area is observed within a bounded time; and (c) **Scalability** – adding more agents is as simple as adding additional phase-shifted copies or new Lissajous loops, without needing complex new trajectories. 

An example outcome from literature: using a 3-agent formation on a single Lissajous curve (with agents phased $120^\circ$ apart), researchers achieved full coverage of a region with each point being visited periodically, no inter-agent collisions, and the ability to “entrain” a target in the center by all agents eventually surrounding it ([](https://arxiv.org/pdf/1812.04904#:~:text=and%20so%20on,detection%20of%20a%20rogue%20element)). This satisfied multiple objectives simultaneously: *O1*: complete area coverage, *O2*: collision-free patrolling, and *O3*: guaranteed detection/entrapment of a target ([](https://arxiv.org/pdf/1812.04904#:~:text=and%20so%20on,detection%20of%20a%20rogue%20element)). These are precisely the kinds of outcomes that demonstrate the utility of Lissajous trajectories in multi-robot coordination. 

In summary, Lissajous curves provide a structured yet flexible framework for multi-agent path planning. They strike a balance between randomness and rigidity – offering predictable, repeatable coverage (crucial for validation and safety) while still covering areas in a sweeping manner. As autonomous systems continue to evolve, such mathematically grounded trajectory designs are valuable for tasks requiring high reliability and performance, from surveillance swarms to coordinated drone light shows (where Lissajous-like Lissajous figures are sometimes used to generate pleasing periodic motions for multiple drones). The theoretical foundations laid out above – spanning from simple harmonic motion to Chebyshev polynomials and optimal interpolation nodes – illustrate the surprising breadth and depth of the Lissajous curve, a classical concept finding renewed relevance in modern applications. 

**Sources:** Lissajous curve fundamentals ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=The%20appearance%20of%20the%20figure,%E2%81%A0a%2Fb%E2%81%A0%20is%20%20103)) ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=Visually%2C%20the%20ratio%20%E2%81%A0a%2Fb%E2%81%A0%20determines,For%20example%2C%20%CE%B4%20%3D%200)) ([ Lissajous curves - Jose M Sallan blog ](https://jmsallan.netlify.app/blog/liisajous-curves/#:~:text=Lissajous%20curves%20represent%20complex%20harmonic,vertical%20and%20horizontal%20lobes%2C%20respectively)); Chebyshev and Padua connections ([Lissajous curve - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_curve#:~:text=Lissajous%20figures%20where%20a%20%3D,and)); Lissajous knots and 3D forms ([Lissajous knot - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_knot#:~:text=Image%3A%20,21%7D%20knot)) ([Lissajous knot - Wikipedia](https://en.wikipedia.org/wiki/Lissajous_knot#:~:text=Because%20a%20knot%20cannot%20be,and%20none%20of%20the%20quantities)); spherical Lissajous definition ([Wolfgang Erb | Spherical Lissajous Curves ](https://www.math.unipd.it/~erb/LSphere.html#:~:text=A%20spherical%20Lissajous%20curve%20is,and%20a%20longitudinal%20harmonic%20motion)); UAV search patterns and multi-agent applications ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=fly%2C%20optimal%20deterministic%20search%20pattern,recently%20caught%20attention%20as%20excellent)) ([
            Lissajous curves as aerial search patterns - PMC
        ](https://pmc.ncbi.nlm.nih.gov/articles/PMC11096320/#:~:text=pattern%20and%20any%20local%20maximum,frequency%20ratio%20is%20indicative%20of)) ([](https://arxiv.org/pdf/1812.04904#:~:text=and%20so%20on,detection%20of%20a%20rogue%20element)).