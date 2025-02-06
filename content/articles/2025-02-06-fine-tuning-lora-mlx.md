---
Title: Fine-Tuning LLMs with LoRA and MLX-LM
Date: 2025-02-06 07:00
Category: Machine Learning
Tags: ai, ml
Slug: 2025-02-06-fine-tuning-lora-mlx
Status: published
---

This blog post is going to be a tutorial on how to fine-tune a LLM with LoRA and the `mlx-lm` package.
Medium draft post can be found [here](https://medium.com/@levchevajoana/fine-tuning-llms-with-lora-and-mlx-lm-c0b143642deb) and Substack [here](https://joanalevtcheva.substack.com/p/780c0ba8-8dc3-461e-95cb-a65728f6c24b).

# Introduction

MLX is an array framework tailored for efficient machine learning research on Apple silicon. Its biggest strength is that it leverages the unified memory architecture of Apple devices and offers a familiar, NumPy-like API. Apple has also developed a package for LLM text generation, fine-tuning, etc. called MLX LM.

Overall,mlx-lm supports many of Hugging Face format LLMs. With mlx-lm it is also very easy to directly load models from the Hugging Face MLX Community. This is a place for mlx model pre-converted weights that run on Apple Silicon, hosting many ready-to-use models with the framework. The framework also supports parameter efficient fine-tuning with LoRA and QLoRA. You can find more information about LoRA in the paper.

In this tutorial, with the help of the `mlx-lm` package, we are going to load the `Mistral-7B-Instruct-v0.3–4bit` model from the MLX Community space, and attempt to fine-tune it with LoRA and the dataset win-wang/Machine_Learning_QA_Collection. Let's begin.

# Tutorial

First, we have to load the needed packages.
import json
from pathlib import Path

```
import matplotlib.pyplot as plt
import mlx.optimizers as optim
from mlx.utils import tree_flatten
from mlx_lm import generate, load
from mlx_lm.tuner import TrainingArgs, linear_to_lora_layers, train

from mlx_utils import load_hf_dataset
```

Then, we should load the model and tokenizer.

```
model_path = "mlx-community/Mistral-7B-Instruct-v0.3-4bit"
model, tokenizer = load(model_path)
```

Let's see ...

```
prompt = "What is under-fitting and overfitting in machine learning?"
messages = [{"role": "user", "content": prompt}]
prompt = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
```

The output is

```
Under-fitting and overfitting are two common problems that can occur when training machine learning models.

1. Under-fitting: This occurs when a model is too simple to learn the underlying pattern in the data. In other words, the model is not complex enough to capture the relationship between the input and output variables. As a result, the model's performance on both the training and test data is poor. This can happen when the model has too few parameters, or when the model is not trained for long enough.

2. Overfitting: This occurs when a model is too complex and starts to fit the noise in the data instead of the underlying pattern. In other words, the model is learning the idiosyncrasies of the training data rather than the general pattern that applies to new, unseen data. As a result, the model performs well on the training data but poorly on the test data. This can happen when the model has too many parameters, or when the model is trained for too long.

The goal in machine learning is to find a balance between under-fitting and overfitting, where the model is complex enough to capture the underlying pattern in the data, but not so complex that it starts
```
