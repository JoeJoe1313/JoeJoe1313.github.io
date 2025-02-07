---
Title: Fine-Tuning LLMs with LoRA and MLX-LM
Date: 2025-02-06 07:00
Category: Machine Learning
Tags: ai, ml, llm
Slug: 2025-02-06-fine-tuning-lora-mlx
Status: published
---

This blog post is going to be a tutorial on how to fine-tune a LLM with LoRA and the `mlx-lm` package.
Medium draft post can be found [here](https://medium.com/@levchevajoana/fine-tuning-llms-with-lora-and-mlx-lm-c0b143642deb) and Substack [here](https://joanalevtcheva.substack.com/p/780c0ba8-8dc3-461e-95cb-a65728f6c24b).

# Introduction

[MLX](https://opensource.apple.com/projects/mlx/) is an array framework tailored for efficient machine learning research on Apple silicon. Its biggest strength is that it leverages the unified memory architecture of Apple devices and offers a familiar, NumPy-like API. Apple has also developed a package for LLM text generation, fine-tuning, etc. called [MLX LM](https://github.com/ml-explore/mlx-examples/blob/main/llms/README.md).

Overall, `mlx-lm` supports many of Hugging Face format LLMs. With `mlx-lm` it is also very easy to directly load models from the Hugging Face [MLX Community](https://huggingface.co/mlx-community). This is a place for mlx model pre-converted weights that run on Apple Silicon, hosting many ready-to-use models with the framework. The framework also supports parameter efficient fine-tuning with [LoRA and QLoRA](https://github.com/ml-explore/mlx-examples/tree/main/lora). You can find more information about LoRA in the following [paper](https://arxiv.org/abs/2106.09685).

In this tutorial, with the help of the `mlx-lm` package, we are going to load the [Mistral-7B-Instruct-v0.3–4bit](https://medium.com/r/?url=https%3A%2F%2Fhuggingface.co%2Fmlx-community%2FMistral-7B-Instruct-v0.3-4bit) model from the MLX Community space, and attempt to fine-tune it with LoRA and the dataset [win-wang/Machine_Learning_QA_Collection](https://medium.com/r/?url=https%3A%2F%2Fhuggingface.co%2Fdatasets%2Fwin-wang%2FMachine_Learning_QA_Collection). Let's begin.

# Tutorial

{% notebook 2025-02-06-fine-tuning-lora-mlx/simple_fine_tune_lora_mlx.ipynb %}
