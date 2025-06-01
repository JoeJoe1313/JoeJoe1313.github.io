---
Title: Thinking Backwards: The "Reversal Blessing" in LLM Multiple-Choice Reasoning
Date: 2025-05-29 07:00
Category: Machine Learning
Tags: ai, ml, llm
Slug: 2025-05-29-reversal-blessing
Status: draft
---

Most modern languages are written from left to right, thus we assume that thinking from left to right is the most natural way to process information expressed with these languages. This is particularly true for **Large Language Models (LLMs)** which are typically trained to predict the next word in a sequence, known as **left-to-right (L2R)** language models. But what if, for certain tasks, thinking backward could actually be better? A recent paper from Apple researchers, titled **_"Reversal Blessing: Thinking Backward May Outpace Thinking Forward in Multi-choice Questions"_**, explores a counterintuitive approach to data augmentation: training LLMs on "reversed" sequences. It delves into the potential of **right-to-left (R2L)** language models, and their effectiveness in tackling some tasks such as **multiple-choice questions (MCQs)**. The paper can be found [here](https://arxiv.org/abs/2502.18435v2), and the supporting code can be found in the GitHub repository [here](https://github.com/apple/ml-reversal-blessing?tab=readme-ov-file).

# Introduction

## Left‐to‐right (L2R) Autoregressive Factorization

Most LLMs are trained to predict text in a strictly left‐to‐right order. L2R models any sequence $x = (x_1, x_2, ..., x_T)$ via

$$
p_{L2R}(x) = \prod_{t=1}^{T} p_{L2R}(x_{t}\mid x_{<t}),
$$

where $x_{<t} = (x_{1}, x_{2}, ..., x_{t-1})$. At each timestep $t$, the model predicts the next token $x_t$ given the full prefix $x_{<t}.$ This aligns with human writing in left to right languages, and is computationally efficient, but can introduce inductive biases. This factorization is not unique—any valid factorization of the joint probability yields the same marginal $p(x)$.

## Right‐to‐left (R2L) Autoregressive Factorization

R2L training simply reverses every sequence, modelling

$$
p_{R2L}(x) \;=\; \prod_{t=1}^{T} p_{R2L}(x_{t}\mid x_{>t}),
$$

where $x_{>t} = (x_{t+1}, x_{t+2}, ..., x_T)$. In simple words, R2L is predicting earlier tokens given later ones. 

Although both factorizations represent the same distribution $p(x)$ in theory, neural approximations break symmetry: reversed factorization leads to different learned behaviors, calibration properties, and uncertainties.
