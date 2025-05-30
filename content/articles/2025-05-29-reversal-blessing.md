---
Title: Thinking Backwards: The "Reversal Blessing" in LLM Multiple-Choice Reasoning
Date: 2025-05-29 07:00
Category: Machine Learning
Tags: ai, ml, llm
Slug: 2025-05-29-reversal-blessing
Status: draft
---

Most modern languages are written from left to right, thus we assume that thinking from left to right is the most natural way to process information expressed with these languages. This is particularly true for **Large Language Models (LLMs)** which are typically trained to predict the next word in a sequence, known as **left-to-right (L2R)** language models. But what if, for certain tasks, thinking backward could actually be better? A recent paper from Apple researchers, titled **_"Reversal Blessing: Thinking Backward May Outpace Thinking Forward in Multi-choice Questions"_**, explores a counterintuitive approach to data augmentation: training LLMs on "reversed" sequences. It delves into the potential of **right-to-left (R2L)** language models, and their effectiveness in tackling some tasks such as **multiple-choice questions (MCQs)**. The paper can be found [here](https://arxiv.org/abs/2502.18435v2), The supporting code can be found in the GitHub repository [here](https://github.com/apple/ml-reversal-blessing?tab=readme-ov-file).
