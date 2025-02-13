---
Title: Qwen2.5-vl with MLX-VLM
Date: 2025-02-13 07:00
Category: Machine Learning
Tags: ai, ml, vlm, mlx-vlm
Slug: 2025-02-13-qwen2_5-vl-mlx-lm
Status: draft
---

In this post, we are going to show a tutorial on using the Qwen2.5-VL model with MLX-VLM for visual understanding tasks. We are going to cover:

- Loading the model and image
- Generating a natural language description of an image
- Extracting spatial information (bounding boxes) for objects
- Visualizing the results

## Introduction

Qwen2.5-VL with MLX-LM is a state-of-the-art multimodal model that seamlessly integrates advanced vision and language processing capabilities. Designed to handle both images and videos, this model excels in generating detailed natural language descriptions and extracting spatial information from visual inputs. Leveraging cutting-edge transformer architectures, Qwen2.5-VL enables developers and researchers to build sophisticated applications in artificial intelligence, bridging the gap between visual perception and textual understanding.

## Loading Packages

We begin by importing the necessary libraries. The mlx_vlm package simplifies loading our Qwen2.5-VL model and handling image inputs. We also use libraries such as matplotlib for plotting and PIL for image processing.

```python
import json

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from mlx_vlm import apply_chat_template, generate, load
from mlx_vlm.utils import load_image
from PIL import Image
```

## Loading the Qwen2.5-VL Model and Processor

Next, we load the pre-trained Qwen2.5-VL model along with its processor using the provided model path. The processor helps in formatting the inputs (both text and image) in a way that the model can understand.

```python
model_path = "mlx-community/Qwen2.5-VL-3B-Instruct-bf16"
model, processor = load(model_path)
config = model.config
```

You’ll notice the loading process involves fetching several files. Once completed, the model is ready to process our inputs.

## Loading and Displaying the Image

For this tutorial, we use an image file (person_dog.jpg) which contains a person with a dog. We load the image using a helper function and then display its properties.

```python
image_path = "person_dog.jpg"
image = load_image(image_path)
print(image)  # Displays a PIL.Image.Image object

# Check image size
print(image.size)  # Example output: (467, 700)
```

At this point, if you’re using a Jupyter Notebook, simply typing image in a cell would render the image inline.

# Generating an Image Description

We now prepare a prompt to describe the image. The prompt is wrapped using the `apply_chat_template` function, which converts our query into the chat-based format expected by the model.

```python
prompt = "Describe the image."
formatted_prompt = apply_chat_template(
    processor, config, prompt, num_images=1
)
```

Next, we generate the output by feeding both the formatted prompt and image into the model:

```python
output = generate(model, processor, formatted_prompt, image, verbose=True)
```

**Sample Output:**

```
The image shows a person standing outdoors, holding a small, fluffy, light-colored dog. The person is wearing a dark gray hoodie with the word "ROX" on it and blue jeans. The background features a garden with various plants and a fence, and there are some fallen leaves on the ground. The setting appears to be a residential area with a garden.
```

This demonstrates how the model can effectively generate descriptive captions for images.

# Object Detection with Bounding Boxes


