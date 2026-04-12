---
Title: Solving the 1D Wave Equation: A Deep Dive into PINNs vs Fourier
Date: 2026-04-12 12:00
Category: Machine Learning
Tags: pde, machine-learning, pinn, wave-equation
Slug: pinn-wave-equation-fixed-string
Status: published
Series: The Wave Equation
---

[TOC]

In a previous post, we explored the [Fourier method for solving the 1D wave equation for a fixed string]({filename}/articles/2025-01-04-fourier-method-fixed-string.md). The analytical approach is beautiful and provides an exact standing-wave solution, but as an alternative, we can turn to a very modern approach: **Physics-Informed Neural Networks (PINNs)** [1]. 

PINNs promise to solve differential equations simply by turning the PDE into a loss function and optimizing a neural network. The wave equation is a particularly interesting test case — Moseley, Markham & Nissen-Meyer [8] demonstrated that PINNs can successfully learn wavefield solutions for the 2D acoustic wave equation across homogeneous, layered, and even Earth-realistic velocity models. However, they also noted that the wave equation presents unique challenges due to the **multi-scale, propagating, and oscillatory** nature of its solutions.

In this article, we'll apply a PINN to our 1D fixed-string problem — a setting with long-time propagation and multiple boundary reflections — and discover exactly where these challenges become insurmountable for a vanilla PINN approach.

# The Problem Recap

Recall our fixed string problem:

$$
\left\{\begin{aligned}
u_{tt} &= \left(\frac{2}{3}\right)^2 u_{xx}, \quad x \in [0, \pi\sqrt{5}], \quad t \in [0, 30] \\ 
u(x, 0) &= \begin{cases} \sin^3{(\pi x)}, & 1 \leq x \leq 3 \\ 0, & \text{otherwise} \end{cases} \\
u_t(x, 0) &= 0 \\
u(0, t) &= u(\pi \sqrt{5}, t) = 0
\end{aligned}\right.
$$

In the Fourier method, we painstakingly calculate eigenvalues, enforce boundary conditions via sines, and compute an infinite expansion of coefficients. 

For the PINN, we train a network $u_\theta(x,t)$ to minimize:

1. **PDE Loss:** The residual of $u_{tt} - a^2 u_{xx} \approx 0$
2. **Initial Condition Loss:** Matching $u(x,0)$ and $u_t(x,0)$

To handle the strict Dirichlet boundary conditions $u(0,t)=u(L,t)=0$, we hard-code them into the network's output to guarantee compliance:
$$
u_{net}(x,t) = x(L-x) \cdot \text{MLP}_\theta(x,t)
$$

The full architecture is shown below:

<center>
![PINN Architecture](/images/2025-04-12-pinn-wave-equation-fixed-string/pinn_architecture.png){ class="zoomable" width=100% }
</center>

# The Training Setup

To give the network the highest chance of success, we armed it with several standard "best practices" from the PINN literature:

- **Fourier Features:** To help the network learn high-frequency wave oscillations, the inputs passed through a learnable sine/cosine embedding layer.
- **Input Normalization:** Scaling $x$ and $t$ to approximately $[-1, 1]$.
- **Causal Weighting:** We applied an exponential weight $w(t) = \exp(-t/\epsilon)$ to the PDE loss, where $\epsilon$ gradually increases over time. This forces the network to learn the near-initial dynamics first before propagating forward in time.
- **Two-phase Optimization:** We trained with Adam for 30,000 epochs, followed by L-BFGS for 500 steps to find a sharp local minimum.

The total loss plunged impressively, reaching `1.12e-03` after L-BFGS. The initial condition losses vanished to nearly zero ($2 \times 10^{-5}$ for displacement, $8 \times 10^{-7}$ for velocity). By the numbers, it looked like a successful training run. 

But when we visualize the network predictions, a different story unfolds.

# Visual Comparison: PINN vs Fourier

We rendered the trained PINN solution (solid blue) alongside the exact 100-term Fourier series solution (dashed red) to evaluate the network's true performance.

### t = 0 — Exploring the Initial Condition

<center>
![t=0: Excellent match](/images/2025-04-12-pinn-wave-equation-fixed-string/pinn_t0.png){ class="zoomable" width=80% }
</center>

At $t=0$, the PINN perfectly reconstructs the analytical initial displacement bump on $[1, 3]$. Both curves align almost exactly. The network successfully learned the initial condition mapping.

### t ≈ 5.0 — The Beginning of Divergence

<center>
![t=5: Divergence begins](/images/2025-04-12-pinn-wave-equation-fixed-string/pinn_t5.png){ class="zoomable" width=80% }
</center>

As time progresses, things begin to break down. The Fourier solution cleanly demonstrates the initial pulse splitting into left- and right-traveling waves. The PINN captures a vague oscillation near $x \approx 5$, but it severely underestimates the amplitude and completely misses the sharp features near $x \approx 1$.

### t ≈ 15.0 — Mid-Horizon

<center>
![t=15: PINN nearly flat](/images/2025-04-12-pinn-wave-equation-fixed-string/pinn_t15.png){ class="zoomable" width=80% }
</center>

By $t=15$, the PINN has decayed to a near-zero state. The Fourier reference still shows active wave patterns with high amplitude, but the PINN output is essentially flat. The network has learned a trivial solution!

### t ≈ 30.0 — Total Failure

<center>
![t=30: Complete failure](/images/2025-04-12-pinn-wave-equation-fixed-string/pinn_t30.png){ class="zoomable" width=80% }
</center>

At the end of the simulation, the PINN is entirely flat while the Fourier solution continues to show highly-structured wave activity reflecting off the boundaries.

For a full interactive look at the failure, check out the animation of the PINN solving the Fixed string:

<iframe src="{static}/code/2025-01-04-fourier-method-fixed-string/fixed_string_pinn_animation.html" width="100%" height="400px" frameborder="0"></iframe>

# Diagnosis: Why Does the PINN "Fade to Zero"?

The progressive flattening we observe — where the PINN learns the initial condition well but produces $u \approx 0$ for later times — is not a bug in our specific implementation. It is a **well-documented and actively-studied failure mode** of physics-informed neural networks applied to hyperbolic and convection-dominated PDEs.

The landmark paper by Krishnapriyan et al. [2], presented at NeurIPS 2021, titled *"Characterizing Possible Failure Modes in Physics-Informed Neural Networks"*, investigated exactly this class of problems. Their central finding is striking: **the failures are not caused by a lack of expressivity in the neural network**, but rather by the fact that the soft PDE-based loss function creates an optimization landscape that is extremely difficult to navigate. In other words, the network has the capacity to represent the true solution — it simply cannot find it through gradient-based optimization.

Let's break down the specific failure mechanisms at play in our experiment.

## 1. The Trivial Solution Attractor

Consider what happens when the optimizer evaluates the candidate $u(x,t) = 0$ against our loss:

* **PDE residual:** $u_{tt} - a^2 u_{xx} = 0 - 0 = 0$. Perfectly satisfied.
* **Boundary conditions:** Hard-encoded via $x(L-x) \cdot \text{net}$, so $u(0,t)=u(L,t)=0$ is guaranteed. Also perfectly satisfied.
* **Initial displacement:** $u(x,0) - \varphi_1(x) \neq 0$. This is the **only** cost.
* **Initial velocity:** $u_t(x,0) = 0$. Also perfectly satisfied.

The zero function satisfies every constraint *except* the initial displacement — and that constraint is localized entirely at $t=0$. For the vast majority of the spatio-temporal domain $[0, L] \times (0, T]$, the trivial solution is a perfect minimizer. The optimizer is essentially drawn toward $u \equiv 0$ in a landscape where the initial condition acts as a small, localized bump pushing it away from that attractor. As training progresses, the network learns a compromise: match $\varphi_1(x)$ at $t=0$ and smoothly decay to zero shortly after. This is not just our observation — Wang, Teng, and Perdikaris [3] documented this exact pathology in their SIAM 2021 paper on gradient flow pathologies in PINNs.

## 2. Spectral Bias (The Frequency Principle)

Neural networks with smooth activations inherently exhibit what Rahaman et al. [4] termed **spectral bias** at ICML 2019: they learn low-frequency components of a target function first and struggle to capture high-frequency details. This phenomenon is also known as the **F-Principle** (Frequency Principle) in the literature [5].

For the wave equation, this is particularly devastating. The Fourier solution of our fixed string is a superposition of modes $\sin(k\pi x/L)$ for $k = 1, 2, \ldots, 100$. The initial $\sin^3(\pi x)$ pulse splits into left- and right-traveling waves that reflect off the boundaries and interfere, producing increasingly complex high-frequency spatial patterns over time. A network biased toward low frequencies will naturally suppress these oscillations, producing the overly-smooth, amplitude-decayed solutions we observe.

While Fourier feature embeddings [6] can alleviate spectral bias for static function approximation, they are less effective in our setting because the frequency content of the solution *evolves over time* — the network must maintain high-frequency components at all time steps simultaneously.

## 3. Violation of Temporal Causality

The standard PINN training procedure samples collocation points uniformly across the entire spatio-temporal domain and optimizes all of them simultaneously. This fundamentally violates the **causal structure** of the wave equation: the state at time $t_2$ depends on the state at time $t_1 < t_2$, not the other way around.

Wang, Sankaran, and Perdikaris [7] argued in their 2022 paper *"Respecting Causality is All You Need for Training Physics-Informed Neural Networks"* that this causality violation is a root cause of PINN failures on time-dependent problems. When the optimizer tries to satisfy the PDE residual at $t = 25$ before it has correctly learned the dynamics at $t = 5$, it receives misleading gradient signals that corrupt the learned solution.

Although we implemented a version of causal weighting in our experiment (exponential decay $w(t) = \exp(-t/\varepsilon)$ with a linearly increasing $\varepsilon$), it was ultimately insufficient. The linear schedule increased $\varepsilon$ too quickly, relaxing the causal focus before the network had fully captured the early-time dynamics. Additionally, causal weighting alone does not address the deeper issue of trying to represent the entire solution with a single monolithic network.

## 4. Gradient Flow Pathologies

Wang, Teng, and Perdikaris [3] identified that PINNs suffer from **stiff gradient dynamics** when multi-term loss functions create conflicting gradient signals. In our case, the PDE loss, the initial displacement loss, and the initial velocity loss compete during each optimization step. The PDE residual produces gradients at scales orders of magnitude different from the initial condition gradients — a multi-task learning problem where the different tasks have wildly different sensitivities.

We can see evidence of this in our training log: the IC losses converged beautifully ($\sim 10^{-5}$ and $\sim 10^{-7}$), but the PDE loss plateaued at $\sim 10^{-2}$, never breaking below that floor. The optimizer found it much easier to satisfy the initial conditions than to propagate the physics forward.

## 5. The Long Time Horizon

All of the above issues are amplified by our time domain. With wave speed $a = 2/3$ and string length $L \approx 7.02$, a wave traverses the full string in $\Delta t = L/a \approx 10.5$ time units. Over $T_{max} = 30$, there are roughly **3 full round-trip reflections**, each producing increasingly complex interference patterns. Krishnapriyan et al. [2] showed that PINN accuracy degrades systematically as the complexity of the PDE increases — and a longer time horizon directly increases the effective complexity of the solution the network must capture.

# What Comes Next

Our experiment demonstrates that "vanilla" PINNs — even when equipped with Fourier features, causal weighting, input normalisation, and L-BFGS fine-tuning — fundamentally struggle with the 1D wave equation over long time horizons. This is not a failure of neural networks per se, but of the training strategy.

The literature offers several promising remedies that directly address the failure modes we've identified:

- **Sequence-to-Sequence Learning** (Krishnapriyan et al. [2]): Decompose the time domain into small windows and train the network sequentially, using the solution at $t = T_k$ as the initial condition for the window $[T_k, T_{k+1}]$. This respects causality by construction and limits the complexity per window.
- **Curriculum Regularisation** (Krishnapriyan et al. [2]): Gradually increase the temporal extent of the training domain, starting from $T_{max}=5$ and progressively extending to $30$.
- **Causal PINNs** (Wang et al. [7]): A more sophisticated causality-respecting loss formulation that dynamically adjusts per-timestep weights based on the current PDE residual.
- **Energy-Preserving Penalties**: Add an explicit loss term enforcing $E(t) \approx E(0)$, directly addressing the lack of energy conservation.

In the next article, we will implement and compare these approaches to see which ones can tame the wave equation and produce a PINN that matches the Fourier series solution.

{% include_code_collapsible 2025-01-04-fourier-method-fixed-string/fixed_string_pinn.py lang:python :hideall: %}

# References

1. **Raissi, M., Perdikaris, P., & Karniadakis, G. E.** (2019). *Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations*. Journal of Computational Physics, 378, 686–707. [doi:10.1016/j.jcp.2018.10.045](https://doi.org/10.1016/j.jcp.2018.10.045)

2. **Krishnapriyan, A. S., Gholami, A., Zhe, S., Kirby, R. M., & Mahoney, M. W.** (2021). *Characterizing Possible Failure Modes in Physics-Informed Neural Networks*. Advances in Neural Information Processing Systems (NeurIPS), 34. [arXiv:2109.01050](https://arxiv.org/abs/2109.01050)

3. **Wang, S., Teng, Y., & Perdikaris, P.** (2021). *Understanding and Mitigating Gradient Flow Pathologies in Physics-Informed Neural Networks*. SIAM Journal on Scientific Computing, 43(5), A3055–A3081. [doi:10.1137/20M1318043](https://doi.org/10.1137/20M1318043)

4. **Rahaman, N., Baratin, A., Arpit, D., Draxler, F., Lin, M., Hamprecht, F. A., Bengio, Y., & Courville, A.** (2019). *On the Spectral Bias of Neural Networks*. Proceedings of the 36th International Conference on Machine Learning (ICML). [arXiv:1806.08734](https://arxiv.org/abs/1806.08734)

5. **Xu, Z.-Q. J., Zhang, Y., Luo, T., Xiao, Y., & Ma, Z.** (2020). *Frequency Principle: Fourier Analysis Sheds Light on Deep Neural Networks*. Communications in Computational Physics, 28(5), 1746–1767. [arXiv:1901.06523](https://arxiv.org/abs/1901.06523)

6. **Tancik, M., Srinivasan, P. P., Mildenhall, B., Fridovich-Keil, S., Raghavan, N., Singhal, U., Ramamoorthi, R., Barron, J. T., & Ng, R.** (2020). *Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains*. Advances in Neural Information Processing Systems (NeurIPS), 33. [arXiv:2006.10739](https://arxiv.org/abs/2006.10739)

7. **Wang, S., Sankaran, S., & Perdikaris, P.** (2024). *Respecting Causality for Training Physics-Informed Neural Networks*. Computer Methods in Applied Mechanics and Engineering, 421, 116813. [arXiv:2203.07404](https://arxiv.org/abs/2203.07404)

8. **Moseley, B., Markham, A., & Nissen-Meyer, T.** (2020). *Solving the wave equation with physics-informed deep learning*. [arXiv:2006.11894](https://arxiv.org/abs/2006.11894)
