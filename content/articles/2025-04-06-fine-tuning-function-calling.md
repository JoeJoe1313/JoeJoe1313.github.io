---
Title: Fine-Tuning a Model for Function-Calling with MLX-LM
Date: 2025-04-06 07:00
Category: Machine Learning
Tags: ai, ml, llm, mlx-lm, mlx
Slug: fine-tuning-function-calling
Status: published
---

In this post, we explore the process of fine-tuning a language model for function-calling using [MLX-LM](https://github.com/ml-explore/mlx-lm). Following the Hugging Face Agents course [notebook](https://huggingface.co/agents-course/notebooks/blob/main/bonus-unit1/bonus-unit1.ipynb), we’ll walk through the steps from setting up the environment to training the model with LoRA adapters. The goal is to empower the model with the ability to intelligently plan and generate function calls, making it a versatile tool for interactive applications. Medium post can be found [here](https://medium.com/@levchevajoana/fine-tuning-a-model-for-function-calling-with-mlx-lm-d00d587e2559)

## Introduction

Modern AI models can do much more than generate plain text — they can now integrate with external tools by “calling” functions based on user intent. In this tutorial, we demonstrate how to adapt a pre-trained model (in our case, the [gemma-2-2b-it-4bit](https://huggingface.co/mlx-community/gemma-2-2b-it-4bit) model from the [MLX Community](https://huggingface.co/mlx-community)) to handle function-calling by using the `mlx-lm` package. This involves creating a specialized chat template, preprocessing a dataset of function call interactions, and applying LoRA for efficient fine-tuning.

## Setting Up the Model and Tokenizer

We start by importing the necessary libraries and modules, including the MLX-LM package, dataset utilities, and LoRA functions.

```python
import json
import os
from enum import Enum
from typing import Dict, List, Tuple, Union

import mlx.optimizers as optim
from datasets import load_dataset
from mlx.utils import tree_flatten
from mlx_lm import generate, load
from mlx_lm.tuner import TrainingArgs, datasets, linear_to_lora_layers, train
```

After loading our model and tokenizer,

```python
model_path = "mlx-community/gemma-2-2b-it-4bit"
model, tokenizer = load(model_path)
```

we customize the tokenizer’s chat template to define the structure of our conversational interactions.

```python
tokenizer.chat_template = (
    "{{ bos_token }}"
    "{% if messages[0]['role'] == 'system' %}{{ raise_exception('System role not supported') }}{% endif %}"
    "{% for message in messages %}"
    "{{ '<start_of_turn>' + message['role'] + '\n' + message['content'] | trim + '<end_of_turn><eos>\n' }}"
    "{% endfor %}"
    "{% if add_generation_prompt %}{{'<start_of_turn>model\n'}}{% endif %}"
)
```

This template embeds special tokens (like `<bos>`, `<start_of_turn>`,` <think>`, and `<tool_call>`) that mark the different stages of the conversation - from the user’s prompt to the model’s internal reasoning and eventual function call.

## Dataset Preparation and Preprocessing

We use the dataset [Jofthomas/hermes-function-calling-thinking-V1](https://huggingface.co/datasets/Jofthomas/hermes-function-calling-thinking-V1) which contains conversations involving function calls.

```python
dataset_path = "Jofthomas/hermes-function-calling-thinking-V1"
```

Let’s load the dataset.

```python
dataset = load_dataset(dataset_path)
dataset
```

This outputs

```
DatasetDict({
    train: Dataset({
        features: ['conversations'],
        num_rows: 3570
    })
})
```

showing that the dataset originally includes a “conversations” column, and has 3570 rows. We rename this column to “messages” for consistency

```python
dataset = dataset.rename_column("conversations", "messages")
dataset
```

and then apply the following preprocessing function

```python
def preprocess(sample):
    messages = sample["messages"]
    first_message = messages[0]

    # Instead of adding a system message, we merge the content into the first user message
    if first_message["role"] == "system":
        system_message_content = first_message["content"]
        # Merge system content with the first user message
        messages[1]["content"] = (
            system_message_content
            + "Also, before making a call to a function take the time to plan the function to take. Make that thinking process between <think>{your thoughts}</think>\n\n"
            + messages[1]["content"]
        )
        # Remove the system message from the conversation
        messages.pop(0)

    return {"text": tokenizer.apply_chat_template(messages, tokenize=False)}
```

to the dataset

```python
dataset = dataset.map(preprocess, remove_columns="messages")
dataset = dataset["train"].train_test_split(0.1)
dataset
```

This function merges any system messages into the first user message, ensuring the context is maintained without extra role annotations. This outputs

```text
DatasetDict({
    train: Dataset({
        features: ['text'],
        num_rows: 3213
    })
    test: Dataset({
        features: ['text'],
        num_rows: 357
    })
})
```

showing that we have successfully separated our original dataset into a train set with 3213 records, and a test set with 357 records. Each sample is now a formatted text string ready for fine-tuning. Let’s see one train example

```text
<bos><start_of_turn>human
You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags.You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug into functions.Here are the available tools:<tools> [{'type': 'function', 'function': {'name': 'create_todo', 'description': 'Create a new todo item', 'parameters': {'type': 'object', 'properties': {'task': {'type': 'string', 'description': 'The task description'}, 'due_date': {'type': 'string', 'format': 'date', 'description': 'The due date of the task'}, 'priority': {'type': 'integer', 'description': 'The priority of the task (1-5)'}}, 'required': ['task', 'due_date']}}}, {'type': 'function', 'function': {'name': 'calculate_bmi', 'description': 'Calculate the Body Mass Index (BMI)', 'parameters': {'type': 'object', 'properties': {'weight': {'type': 'number', 'description': 'The weight in kilograms'}, 'height': {'type': 'number', 'description': 'The height in meters'}}, 'required': ['weight', 'height']}}}] </tools>Use the following pydantic model json schema for each tool call you will make: {'title': 'FunctionCall', 'type': 'object', 'properties': {'arguments': {'title': 'Arguments', 'type': 'object'}, 'name': {'title': 'Name', 'type': 'string'}}, 'required': ['arguments', 'name']}For each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:
<tool_call>
{tool_call}
</tool_call>Also, before making a call to a function take the time to plan the function to take. Make that thinking process between <think>{your thoughts}</think>

I need to create a new task.<end_of_turn><eos>
<start_of_turn>model
Sure, I can help with that. Could you please provide me with the task description, the due date, and the priority level?<end_of_turn><eos>
<start_of_turn>human
The task is to prepare a presentation for the annual meeting. The due date is 2022-09-15 and the priority level is 3.<end_of_turn><eos>
<start_of_turn>model
<think>Okay, so I need to figure out the reasoning that goes between the conversation and the next function call. Let me break this down step by step.

First, looking at the conversation, the user starts by saying, "I need to create a new task." The model responds by asking for the task description, due date, and priority level. The user then provides all the necessary details: the task is to prepare a presentation for the annual meeting, the due date is 2022-09-15, and the priority is 3.

Now, the model's next move should be to call the appropriate function. The available functions are 'create_todo' and 'calculate_bmi'. Since the user is talking about creating a new task, 'create_todo' is the relevant function here.

Examining the function's parameters, it requires 'task', 'due_date', and takes 'priority' as optional. The user provided all three, so we can include them in the arguments.

Therefore, the model will execute the 'create_todo' function with the provided task details. This makes sense because the conversation is about setting up a new task, and the function is designed for that exact purpose.
</think><tool_call>
{'name': 'create_todo', 'arguments': {'task': 'Prepare a presentation for the annual meeting', 'due_date': '2022-09-15', 'priority': 3}}
</tool_call><end_of_turn><eos>
<start_of_turn>tool
<tool_response>
{'status': 'success', 'message': 'Todo item successfully created', 'todo_id': '12345'}
</tool_response><end_of_turn><eos>
<start_of_turn>model
Your task has been successfully created. The ID for your new task is 12345.<end_of_turn><eos>
```

## Training Setup with LoRA Adapters

To efficiently fine-tune the model without retraining all of its parameters, we leverage LoRA. First, we create a directory to store adapter configurations and weights.

```python
adapter_path = "adapters_fc"
os.makedirs(adapter_path, exist_ok=True)
adapter_config_path = os.path.join(adapter_path, "adapter_config.json")
adapter_file_path = os.path.join(adapter_path, "adapters.safetensors")
```

Then we define our LoRA configuration, with parameters like number of layers 8, a rank of 16, scale of 64, a dropout of 0.05,

```python
lora_config = {
    "num_layers": 8,
    "lora_parameters": {
        "rank": 16,
        "scale": 64,
        "dropout": 0.05,
    },
}
```

and save it as a JSON file.

```python
with open(adapter_config_path, "w") as f:
    json.dump(lora_config, f, indent=4)
```

Next, we define the training arguments, specifically setting a single iteration,

```python
training_args = TrainingArgs(
    adapter_file=adapter_file_path,
    iters=1,
    steps_per_eval=50,
)
```

and freeze the original model parameters.

```python
_ = model.freeze()
```

Then, we convert selected linear layers to LoRA layers to make only a small subset of parameters trainable.

```python
linear_to_lora_layers(model, lora_config["num_layers"], lora_config["lora_parameters"])
```

In our example, this results in

```python
num_train_params = sum(v.size for _, v in tree_flatten(model.trainable_parameters()))
print(f"Number of trainable parameters: {num_train_params}")
```

983,040 trainable parameters. Finally, we should not forget to activate training mode while still preserving the frozen state of the main model parameters.

```python
_ = model.train()
```

## Fine-Tuning Process and Metrics

With our model and dataset ready, we configure a metrics tracker to log both training and validation losses,

```python
class Metrics:
    def __init__(self) -> None:
        self.train_losses: List[Tuple[int, float]] = []
        self.val_losses: List[Tuple[int, float]] = []

    def on_train_loss_report(self, info: Dict[str, Union[float, int]]) -> None:
        self.train_losses.append((info["iteration"], info["train_loss"]))

    def on_val_loss_report(self, info: Dict[str, Union[float, int]]) -> None:
        self.val_losses.append((info["iteration"], info["val_loss"]))
```

and create an instance of this class.

```python
metrics = Metrics()
```

We also create mlx-lm–suitable datasets by first defining the following configuration about our datasets,

```python
configs = {
    "mask_prompt": False,
    "prompt_feature": "prompt",
    "text_feature": "text",
    "completion_feature": "completion",
    "chat_feature": "messages",
}
```

and then create a train set with the help of the mlx-lm function `datasets.create_dataset` and passing the configuration from above.

```python
train_set = datasets.create_dataset(
    dataset["train"],
    tokenizer,
    configs
)
```

Similarly, we create our validation set.

```python
val_set = datasets.create_dataset(
    dataset["test"],
    tokenizer,
    configs
)
```

Finally, we start the fine-tuning process by calling the `train()` function.

```python
train(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    optimizer=optim.Adam(learning_rate=1e-5),
    train_dataset=train_set,
    val_dataset=val_set,
    training_callback=metrics,
)
```

The training logs report both training and validation losses, along with performance metrics like tokens processed per second and memory usage. After training, the adapter weights are saved and can later be reloaded to quickly deploy the fine-tuned model.

```
Starting training..., iters: 1
Iter 1: Val loss 1.821, Val took 128.584s
Iter 1: Train loss 1.861, Learning Rate 1.000e-05, It/sec 0.430, Tokens/sec 160.427, Trained Tokens 3735, Peak mem 20.665 GB
Saved final weights to adapters_fc/adapters.safetensors.
```

## Evaluating the Fine-Tuned Model

After training, we reload the model with the newly learned LoRA weights,

```python
model_lora, _ = load(model_path, adapter_path=adapter_path)
```

set our prompt to

```python
prompt="""<bos><start_of_turn>human
You are a function calling AI model. You are provided with function signatures within <tools></tools> XML tags.You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug into functions.Here are the available tools:<tools> [{'type': 'function', 'function': {'name': 'convert_currency', 'description': 'Convert from one currency to another', 'parameters': {'type': 'object', 'properties': {'amount': {'type': 'number', 'description': 'The amount to convert'}, 'from_currency': {'type': 'string', 'description': 'The currency to convert from'}, 'to_currency': {'type': 'string', 'description': 'The currency to convert to'}}, 'required': ['amount', 'from_currency', 'to_currency']}}}, {'type': 'function', 'function': {'name': 'calculate_distance', 'description': 'Calculate the distance between two locations', 'parameters': {'type': 'object', 'properties': {'start_location': {'type': 'string', 'description': 'The starting location'}, 'end_location': {'type': 'string', 'description': 'The ending location'}}, 'required': ['start_location', 'end_location']}}}] </tools>Use the following pydantic model json schema for each tool call you will make: {'title': 'FunctionCall', 'type': 'object', 'properties': {'arguments': {'title': 'Arguments', 'type': 'object'}, 'name': {'title': 'Name', 'type': 'string'}}, 'required': ['arguments', 'name']}For each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:
<tool_call>
{tool_call}
</tool_call>Also, before making a call to a function take the time to plan the function to take. Make that thinking process between <think>{your thoughts}</think>

Hi, I need to convert 500 USD to Euros. Can you help me with that?<end_of_turn><eos>
<start_of_turn>model
<think>"""
```

and generate a response

```python
generate(model_lora, tokenizer, prompt=prompt, verbose=True, max_tokens=1000)
```

which returns

```text
==========

To convert USD to Euros, I need to use the 'convert_currency' function from the provided tools.  I need to provide the amount to convert, the currency to convert from (USD), and the currency to convert to (Euros).  I should also make sure the amount is a number.
</think>

<tool_call>
{
  'name': 'convert_currency',
  'arguments': {
    'amount': 500,
    'from_currency': 'USD',
    'to_currency': 'EUR'
  }
}
</tool_call> 

==========
Prompt: 460 tokens, 862.170 tokens-per-sec
Generation: 135 tokens, 68.472 tokens-per-sec
Peak memory: 20.665 GB
```

The model first walks through a thought process before generating a function call to convert USD to Euros. This demonstrates the model’s improved ability to generate precise JSON function calls within `<tool_call>` XML tags.

## Conclusion

Fine-tuning a model for function-calling can significantly enhance its interactivity and real-world utility. By adapting the chat template, preprocessing the dataset, and applying LoRA adapters, we’ve demonstrated a streamlined approach to training a model that can generate executable function calls with clear reasoning. It is impressive that we achieved this by using only the `mlx-lm` package. Happy fine-tuning!
