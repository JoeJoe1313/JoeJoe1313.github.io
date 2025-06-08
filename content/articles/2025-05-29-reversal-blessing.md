---
Title: Thinking Backwards: The "Reversal Blessing" in LLM Multiple-Choice Reasoning
Date: 2025-05-29 07:00
Category: Machine Learning
Tags: ai, ml, llm
Slug: 2025-05-29-reversal-blessing
Status: draft
---

Most modern languages are written from left to right, thus we assume that thinking from left to right is the most natural way to process information expressed with these languages. This is particularly true for **Large Language Models (LLMs)** which are typically trained to predict the next word in a sequence, known as **left-to-right (L2R)** language models. But what if, for certain tasks, thinking backward could actually be better? A recent paper from Apple researchers, titled **_"Reversal Blessing: Thinking Backward May Outpace Thinking Forward in Multi-choice Questions"_**, explores a counterintuitive approach to data augmentation: training LLMs on "reversed" sequences. It delves into the potential of **right-to-left (R2L)** language models, and their effectiveness in tackling some tasks such as **multiple-choice questions (MCQs)**. The paper can be found [here](https://arxiv.org/abs/2502.18435v2), and the supporting code can be found in the GitHub repository [here](https://github.com/apple/ml-reversal-blessing?tab=readme-ov-file).

# Left‐to‐right (L2R) Autoregressive Factorization

Most LLMs are trained to predict text in a strictly left‐to‐right order. Left-to-right autoregressive (**L2R**) factorization is the fundamental mathematical principle underlying how large language models generate text. It's based on decomposing the probability of a sequence into conditional probabilities. 

## The Theory

Given a sequence of tokens $x_1,x_2, \dots , x_n$​, the joint probability can be factorized using the chain rule of probability:

$$
p(x_1,x_2,\dots,x_n) = p(x_1)p(x_2∣x_1)p(x_3∣x_1,x_2) \dots p(x_n∣x_1,\dots,x_{n−1})
$$

This can be written more compactly as:

$$
p(x_1,x_2,\dots,x_n) = \prod_{i=1}^n p(x_i∣x_1,\dots,x_{i−1})
$$

The key insight is that we model each token's probability as dependent only on the tokens that came before it (hence "left-to-right"). This creates a causal dependency structure where future tokens cannot influence past tokens. Unfortunately, this approach can introduce inductive biases, errors compounding at each step, and may not be optimal for all reasoning or knowledge‐retrieval tasks 


Now, let's formally define the L2R factorization with the notation we are going to use throughout the post. For any sequence $x = (x_1, x_2, \dots, x_T)$, we can express the joint probability as

$$
\fbox{
    $p_{L2R}(x) = \prod_{t=1}^{T} p_{L2R}(x_{t}\mid x_{<t})$,
}
$$

where $x_{<t} = (x_{1}, x_{2}, \dots, x_{t-1})$. At each timestep $t$, the model predicts the next token $x_t$ given the full prefix $x_{<t}.$ This factorization is not unique, any valid factorization of the joint probability yields the same marginal $p(x)$.

We are also going to need the log-lokielhood of the sequence, which is

$$
\fbox{
    $\log p_{L2R}(x) = \sum_{t=1}^{T} \log p_{L2R}(x_{t}\mid x_{<t})$.
}
$$

You might wonder why we are going to use the log-likelihood. The most straightforward reasons are:

- **Numerical stability**: Multiplying many small probabilities leads to underflow, whereas adding logs is stable
- **Training objective**: LLMs minimize negative log-likelihood (cross-entropy loss)
- **Easier optimization**: Sums are easier to differentiate than products

For _"The cat sat."_ we would have:

$$
\log p = \log p(\text{The}) + \log p(\text{cat}|\text{The}) + \log p(\text{sat}|\text{The, cat}) + \log p(\text{.}|\text{The, cat, sat})
$$

## How LLMs Implement This

Language models learn to approximate each conditional probability $P(x_i | x_1, \dots, x_{i-1})$ through:

- **Encoder layers** that build rich contextual representations of the preceding tokens
- **Attention mechanisms** that allow each position to attend to all previous positions (but not future ones via causal masking)
- **Output layer** that converts the contextual representation into a probability distribution over the vocabulary

During training, the model sees the entire sequence but uses causal masking to ensure position $i$ only sees tokens $1$ through $i-1$. During inference, generation happens token by token, with each new token sampled from the predicted distribution.

## Example

For the sequence _"The cat sat."_:

| Step $t$ | Context $x_{<t}$      | Model outputs distribution over next token    |     Picked token    |
| :------: | :-------------------- | :-------------------------------------------- | :-----------------: |
|     1    | ( )                   | $P(\text{The})=0.4,\ P(\text{A})=0.3,\dots$ |        The        |       |
|     2    | (The)               | $P(\text{cat}\mid   \text{The})=0.5,\dots$   | cat |
|     3    | (The, cat)        | $P(\text{sat}\mid \text{The cat})=0.6,\dots$ | sat |
|     4    | (The, cat, sat) | $P(\text{.}\mid…)=0.8,\dots$     | .   |

# Right‐to‐left (R2L) Autoregressive Factorization

Right-to-left autoregressive factorization is the mathematical "mirror image" of left-to-right, where we factorize the probability by conditioning each token on all the tokens that come after it instead of before.

## The Theory

Given a sequence of tokens $x_1, x_2, \dots, x_n$​, we can factorize using the chain rule in reverse order:

$$
P(x_1, x_2, \dots, x_n) = P(x_n) P(x_{n-1}|x_n) P(x_{n-2}|x_{n-1}, x_n) \dots P(x_1|x_2, \dots, x_n)
$$

This can be written as:

$$
P(x_1, x_2, \dots, x_n) = \prod_{i=1}^{n} P(x_i | x_{i+1}, \dots, x_n)
$$

This is a bit strange to say it like that, but now each token's probability depends on all the tokens that come after it in the sequence. In simple words, R2L is predicting earlier tokens given later ones. You probably immediately asked "But how?", and later you are going ot see the answer is "With the help of Bayes' rule".

Now, let's also formally define the R2L factorization. For any sequence $x = (x_1, x_2, \dots, x_T)$, we can express the joint probability as

$$
\fbox{
    $p_{R2L}(x) \;=\; \prod_{t=1}^{T} p_{R2L}(x_{t}\mid x_{>t})$,
}
$$

where $x_{>t} = (x_{t+1}, x_{t+2}, \dots, x_T)$. And for the log-likelihood, we have

$$
\fbox{
    $\log p_{R2L}(x) \;=\; \sum_{t=1}^{T} \log p_{R2L}(x_{t}\mid x_{>t})$.
}
$$

Although both L2R and R2L factorizations represent the same distribution $p(x)$ in theory, neural approximations break symmetry: reversed factorization leads to different learned behaviors, calibration properties, and uncertainties.

## Example

| Step $t$ |   Context $x_{>t}$  | Model outputs distribution over $x_t$    | Picked token |
| :----------------: | :----------------- | :--------------------------------------- | :----------: |
|          4         |         ( )         | $P(\text{.})=0.7,\dots$                  |      .     |
|          3         |        (.)        | $P(\text{sat}\mid .)=0.6,\dots$        |     sat    |
|          2         |     (sat, .)    | $P(\text{cat}\mid\text{sat.})=0.5,\dots$     |     cat    |
|          1         | (cat, sat, .) | $P(\text{The}\mid\text{cat sat.})=0.4,\dots$ |     The    |

# Key Questions

The paper investigates the following three questions:

- How to evaluate R2L models on knowledge extraction and basic reasoning tasks? 
- Can R2L factorization match or surpass L2R’s capabilities in knowledge extraction and reasoning for downstream tasks?
- What are underlying factors determining the preference of L2R or R2L factorizations?

# Multiple‐Choice Questions

Multiple‐choice questions (MCQs) are a common benchmark for evaluating an LLM’s knowledge, reasoning, and calibration. As we can see in **Figure 1**, in their simplest form, an MCQ comprises:

- A **question** $q$
- A set of $n$ **candidate answers** $a_1, \dots, a_n$
- Exactly **one correct answer** $a^{*}$ among these $n$ choices

<figure>
  <img src="../images/2025-05-29-reversal-blessing/mcq_fig.jpeg" alt="MCQ figure" style="display: block; margin: 0 auto">
  <figcaption style="text-align: center">Figure 1. MCQ</figcaption>
</figure>

## L2R on MCQs

Let $q$ be a question with answer candidates $\{a_1, a_2, \dots, a_n\}$. Most L2R‐based LLMs approach MCQs by computing, for each candidate $a_i$, the conditional log‐probability:

$$
\log p_{L2R}(a_i \mid ​q) = \sum_{l=1}^{N_i} \log p_{L2R}(a_i^{(l)} \mid q, a_i^{(<l)}),
$$

where $N_i = |a_i|$ is the token length of answer $a_i$. Normalizing by the answer length $N_i$, we obtain the **forward‐thinking score**

$$
s_i^{(L2R)} = \frac{1}{N_i} \log p_{L2R}(a_i \mid ​q),
$$

and the chosen answer index is

$$
\hat{i} = \arg \max_{i \in \{1, \dots, n\}} s_i^{(L2R)}.
$$

Because the model is trained to maximize $\log p(x)$ in the L2R direction, it is inherently good at predicting a short correct answer string next given a fixed question prefix. However, if the correct answer has multiple valid encodings (e.g., synonyms, morphological variants), the probability mass $p_{L2R}(a_i \mid q)$ may be spread across these variants, reducing the normalized score $s_i^{(L2R)}$.

However, L2R forward thinking can suffer from **surface‐form competition** and calibration issues. For example, if two semantically equivalent answers (“dog” vs. “puppy”) each capture only a portion of the probability mass, the true answer may be penalized just because its mass is split.

## R2L on MCQs

At inference, given a candidate answer $a_i$ and a question $q$, R2L-based LLMs score each candidate by evaluating

$$
\log p_{R2L}(q \mid ​a_i) = \sum_{l=1}^{M_i} \log p_{R2L}(q^{(l)} \mid a_i, q^{(>l)}),
$$

where we concatenate $a_i$ and $q$ into a single sequence $a_i, q$. Denote $M_i = \mid (a_i, q) \mid$, the combined token length.

By Bayes’ rule, for each candidate $a_i$ it follows

$$
\log p(a_i \mid q) = \log p(q \mid a_i) + \log p(a_i) - \log p(q).
$$


Discarding the constant $\log p(q)$ and approximating $\log p(a_i)$ with $\log p_{R2L}(a_i)$, one can define three reverse‐thinking paradigms:

- **Paradigm 1 (Normalized + Prior):**

$$
s_i^{(1)} = \frac{1}{M_i} \log p_{R2L}(q \mid a_i) + \log p_{R2L}(a_i)
$$

- **Paradigm 2 (Unnormalized + Prior):**

$$
\tilde{s}_i^{(2)} = \log p_{R2L}(q \mid a_i) + \log p_{R2L}(a_i)
$$

- **Paradigm 3 (Unnormalized, Uniform Prior):**

$$
s_i^{(3)} = \log p_{R2L}(q \mid a_i)
$$

Empirically, Paradigm 3 — which ignores $\log p(a_i)$ — consistently yields the highest MCQ accuracy across a variety of tasks. By treating all $a_i$ as equally likely apriori, it eliminates the need to estimate $\log p(a_i)$ (which can be noisy) and removes length biases.

Hence, the **reverse‐thinking MCQ** predictor is:

$$
\hat{i}^{(R2L)} = \arg \max_{i \in \{1, \dots, n\}} s_i^{(3)} = \arg \max_{i \in \{1, \dots, n\}} \log p_{R2L}(q \mid a_i).
$$

In practice, one concatenates “answer choice” followed by “question” into a single sequence - each reversed internally for the R2L model—and computes the joint probability of generating the question given the answer.
