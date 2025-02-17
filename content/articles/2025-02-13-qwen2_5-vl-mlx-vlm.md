---
Title: Qwen2.5-vl with MLX-VLM
Date: 2025-02-13 07:00
Category: Machine Learning
Tags: ai, ml, vlm, mlx-vlm, mlx
Slug: 2025-02-13-qwen2_5-vl-mlx-vlm
Status: published
---

In this post, we are going to show a tutorial on using the [Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL) model with [MLX-VLM](https://github.com/Blaizzy/mlx-vlm) for visual understanding tasks. We are going to cover:

- Loading the model and image
- Generating a natural language description of an image
- Perform object detection in different scenarios with outputing their bounding boxes in JSON format
- Visualizing the results

Medium post can be found [here](https://medium.com/@levchevajoana/qwen2-5-vl-with-mlx-vlm-c4329b40ab87) and Substack [here](https://substack.com/home/post/p-157062287).

# Introduction

[Qwen2.5-VL](https://github.com/QwenLM/Qwen2.5-VL) is the latest flagship vision-language model from the Qwen series, representing a significant advancement over its predecessor, [Qwen2-VL](https://arxiv.org/abs/2409.12191). This model is designed to enhance visual understanding and interaction capabilities across various domains. Key features of Qwen2.5-VL include:

- **Enhanced Visual Recognition:** The model excels at identifying a wide range of objects, including plants, animals, landmarks, and products. It also proficiently analyzes texts, charts, icons, graphics, and layouts within images.
- **Agentic Abilities:** Qwen2.5-VL functions as a visual agent capable of reasoning and dynamically directing tools, enabling operations on devices like computers and mobile phones.
- **Advanced Video Comprehension:** The model can understand lengthy videos exceeding one hour and can pinpoint specific events by identifying relevant video segments.
- **Accurate Visual Localization:** It can precisely locate objects within images by generating bounding boxes or points and provides structured JSON outputs detailing absolute coordinates and attributes.
- **Structured Data Output:** Qwen2.5-VL supports the generation of structured outputs from data such as scanned invoices, forms, and tables, benefiting applications in finance and commerce.

Performance evaluations indicate that the flagship model, Qwen2.5-VL-72B-Instruct, delivers competitive results across various benchmarks, including college-level problem-solving, mathematics, document comprehension, general question answering, and video understanding. Notably, it demonstrates significant strengths in interpreting documents and diagrams and operates effectively as a visual agent without the need for task-specific fine-tuning.

For developers and users interested in exploring Qwen2.5-VL, both base and instruct models are available in 3B, 7B, and 72B parameter sizes on platforms like Hugging Face. Additionally, the model can be used through [Qwen Chat](https://chat.qwenlm.ai).

# Tutorial

## Loading Packages

We begin by importing the necessary libraries. We are going to use the `mlx_vlm` package to load and operate with our Qwen2.5-VL model. We also use libraries such as matplotlib for plotting and PIL for image processing.

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

Next, we load the pre-trained [Qwen2.5-VL-3B-Instruct-bf16](https://huggingface.co/mlx-community/Qwen2.5-VL-3B-Instruct-bf16) model from the Hugging Face [MLX Community](https://huggingface.co/mlx-community) along with its processor using the provided model path. The processor formats and preprocesses both text and image inputs to ensure they are compatible with the model’s architecture.

```python
model_path = "mlx-community/Qwen2.5-VL-3B-Instruct-bf16"
model, processor = load(model_path)
config = model.config
```

You’ll notice the loading process involves fetching several files if the model hasn’t been downloaded previously. Once completed, the model is ready to process our inputs.

## Loading and Displaying the Image

For this tutorial, we use an image file (`person_dog.jpg`) which contains a person with a dog. We load the image using a helper function and then display its size.

```python
image_path = "person_dog.jpg"
image = load_image(image_path)
print(image)
print(image.size)  # Example output: (467, 700)
```

The input image is shown below.

![Input](../images/2025-02-13-qwen2_5-vl-mlx-vlm/input.png){ style="display: block; margin: 0 auto"}

## Generating an Image Description

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

## Object Detection with Bounding Boxes

In addition to descriptions, the Qwen2.5-VL model can help us obtain spatial details such as bounding box coordinates for detected objects. We prepare a prompt asking the model to outline each object’s position in JSON format. We include the system prompt *“You are a helpful assistant"*, the user prompt describing the task *“Outline the position of each object and output all the bbox coordinates in JSON format.”*, and the path to the input image.

```python
system_prompt="You are a helpful assistant"
prompt="Outline the position of ecah object and output all the bbox coordinates in JSON format."
messages = [
    {
      "role": "system",
      "content": system_prompt
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": prompt
        },
        {
          "type": "image",
          "image": image_path,
        }
      ]
    }
  ]
prompt = apply_chat_template(processor, config, messages, tokenize=False)
```

We then generate the spatial output:

```python
output = generate(
    model,
    processor,
    prompt,
    image,
    verbose=True
)
```

**Sample JSON Output:**

`````markdown
```json
[
  {
    "bbox_2d": [170, 105, 429, 699],
    "label": "person holding dog"
  },
  {
    "bbox_2d": [180, 158, 318, 504],
    "label": "dog"
  }
]
```
`````

This output provides the absolute coordinates of the bounding boxes around the detected objects along with the corresponding label. We should note that the absolute coordinates are with respect to:

- The beginning of the coordinate system which is top left.
- The image size corresponding to the possibly resized image after it’s processed via the `processor`. We can determine the new size by checking the `image_grid_thw` value in

```python
processor.image_processor(image)
```

and the `patch_size` value from `processor`. Then we simply multiply the height and width values of `image_grid_thw` with the `ptach_size`, which by default is $14$. Thus, the adjusted bounding box coordinates can be determined by scaling with the original image size divided by the image size after it’s processed by the `processor`. The code can be seen in the next section in the function `normalize_bbox(processor, image, x_min, y_min, x_max, y_max)`.

**Observations:**

1. Most of the time the model produces an identical format of the JSON, with the same key-value pairs. If the user prompt didn’t include the word bbox before the word coordinates, the model sometimes produced slightly different key names and/or structure.

2. I achieved accurate and identical JSON outputs when using [mlx-community/Qwen2.5-VL-3B-Instruct-8bit](https://huggingface.co/mlx-community/Qwen2.5-VL-3B-Instruct-8bit) and [mlx-community/Qwen2.5-VL-3B-Instruct-bf16](https://huggingface.co/mlx-community/Qwen2.5-VL-3B-Instruct-bf16). In contrast, when I experimented with [mlx-community/Qwen2.5-VL-7B-Instruct-6bit](https://huggingface.co/mlx-community/Qwen2.5-VL-7B-Instruct-6bit) and [mlx-community/Qwen2.5-VL-7B-Instruct-8bit](https://huggingface.co/mlx-community/Qwen2.5-VL-7B-Instruct-8bit) the generated bounding box coordinates seemed to be shifted along the $y$-axis, but otherwise matched the dimensions of the bounding boxes generated with 3B models.

## Visualizing the Bounding Boxes

To better understand the spatial outputs, we can visualize these bounding boxes on the image. Below are helper functions that:

- Parse the JSON output

```python
def parse_bbox(bbox_str):
    return json.loads(bbox_str.replace("```json", "").replace("```", ""))
```

- Normalize bounding box coordinates to match the image dimensions

```python
def normalize_bbox(processor, image, x_min, y_min, x_max, y_max):
    width, height = image.size
    _, input_height, input_width = (
        processor.image_processor(image)["image_grid_thw"][0] * 14
    )

    x_min_norm = int(x_min / input_width * width)
    y_min_norm = int(y_min / input_height * height)
    x_max_norm = int(x_max / input_width * width)
    y_max_norm = int(y_max / input_height * height)

    return x_min_norm, y_min_norm, x_max_norm, y_max_norm
```

- Plot the image with rectangles and labels

```python
def plot_image_with_bboxes(processor, image, bboxes):
    image = Image.open(image) if isinstance(image, str) else image
    _, ax = plt.subplots(1)
    ax.imshow(image)

    if isinstance(bboxes, list) and all(isinstance(bbox, dict) for bbox in bboxes):
        colors = plt.cm.rainbow(np.linspace(0, 1, len(bboxes)))

        for i, (bbox, color) in enumerate(zip(bboxes, colors)):
            label = bbox.get("label", None)
            x_min, y_min, x_max, y_max = bbox.get("bbox_2d", None)

            x_min_norm, y_min_norm, x_max_norm, y_max_norm = normalize_bbox(
                processor, image, x_min, y_min, x_max, y_max
            )
            width = x_max_norm - x_min_norm
            height = y_max_norm - y_min_norm

            rect = patches.Rectangle(
                (x_min_norm, y_min_norm),
                width,
                height,
                linewidth=2,
                edgecolor=color,
                facecolor="none",
            )
            ax.add_patch(rect)
            ax.text(
                x_min_norm,
                y_min_norm,
                label,
                color=color,
                fontweight="bold",
                bbox=dict(facecolor="white", edgecolor=color, alpha=0.8),
            )

    plt.axis("off")
    plt.tight_layout()
```

Running the functions below

```python
objects_data = parse_bbox(output)
plot_image_with_bboxes(processor, image, bboxes=objects_data)
```

display the original image with bounding boxes drawn around the person and the dog, along with their respective labels.

![Output](../images/2025-02-13-qwen2_5-vl-mlx-vlm/output.png){ style="display: block; margin: 0 auto"}

This example shows that even the 3B model can accurately detect objects based on a general prompt to detect all objects in the image.

## More Spatial Understanding Examples

We can demonstrate a few other model outputs, corresponding to different spatial understanding tasks.

### Detect a specific object using descriptions

**Prompt:** *“Outline the position of the dog and output all the bbox coordinates in JSON format.”*

**Output:**

![Output](../images/2025-02-13-qwen2_5-vl-mlx-vlm/output_1.png){ style="display: block; margin: 0 auto"}

**Observation:** The dog was accurately detected.

The next examples are taken from the original Qwen2.5-VL [cookbook](https://github.com/QwenLM/Qwen2.5-VL/blob/main/cookbooks/spatial_understanding.ipynb) in which they use the model `Qwen2.5-VL-7B-Instruct`.

### Reasoning capability

**Prompt:** *“Locate the shadow of the paper fox, report the bbox coordinates in JSON format.”*

**Note:** The original image size as in the cookbook example was reduced so it can be better processed by the 3B model.

**Output:**

![Output](../images/2025-02-13-qwen2_5-vl-mlx-vlm/output_2.png){ style="display: block; margin: 0 auto"}

**Observation:** The shadow of the paper fox was accurately detected.

### Understand relationships across different instances

**Prompt:** *“Locate the person who acts bravely, report the bbox coordinates in JSON format.”*

**Output:**

![Output](../images/2025-02-13-qwen2_5-vl-mlx-vlm/output_3.png){ style="display: block; margin: 0 auto"}

**Observation:** The person who acts bravely was accurately detected.

### Find a special instance with unique characteristic

**Prompt:** *“If the sun is very glaring, which item in this image should I use? Please locate it in the image with its bbox coordinates and its name and output in JSON format.”*

**Output:**

![Output](../images/2025-02-13-qwen2_5-vl-mlx-vlm/output_4.png){ style="display: block; margin: 0 auto"}

**Observation:** The image input in the cookbook has a transparent background. I tested the model with a present background and the produced results were not very logical. The above result is of the original image without background. Moreover, their output is `glasses`, in contrast to our 3B output `umbrella`, but our output is still logical.

---

In the end of their cookbook they mention that the above examples were based on the default system prompt. The system prompt can be changed so that we can obtain other output format like plain text. The supported Qwen2.5-VL formats are:

- bbox-format: JSON

```python
{"bbox_2d": [x1, y1, x2, y2], "label": "object name/description"}
```

- bbox-format: plain text

```
x1,y1,x2,y2 object_name/description
```

- point-format: XML

```xml
<points x y>object_name/description</points>
```

- point-format: JSON

```python
{"point_2d": [x, y], "label": "object name/description"}
```

They also give an example of how to change the system prompt so it ouputs plain text:

*“As an AI assistant, you specialize in accurate image object detection, delivering coordinates in plain text format ‘x1,y1,x2,y2 object’.”*

## Conclusion

In this tutorial, we explored the capabilities of Qwen2.5-VL by using MLX-VLM for various visual understanding tasks. We demonstrated how to load the model and images, generate natural language descriptions, and perform object detection with bounding boxes in different spatial understanding scenarios. Our experiments show that even the 3B model provides accurate object localization and structured JSON outputs, and suggests to be indeed a very powerful vision-language model.
