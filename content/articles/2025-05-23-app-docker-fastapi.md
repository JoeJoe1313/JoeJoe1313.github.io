---
Title: Image Segmentation with PaliGemma 2 mix, Transformers, Docker, FastAPI, and GitHub Actions
Date: 2025-05-23 07:00
Category: Machine Learning
Tags: ai, ml, vlm, docker, fastapi, github-actions
Slug: 2025-05-23-app-docker-fastapi
Status: published
---

In today’s fast-paced machine learning landscape, deploying AI models is just as important as developing them. In this blog post, we are going to walk through an image segmentation application using Google’s **PaliGemma 2 Mix** model and **transformers**, containerized with **Docker**, and served through a **FastAPI** backend. We are also going to discuss the CI/CD pipeline using **GitHub Actions** to automate building the Docker image and pushing it to Docker Hub. Let’s explore this service, why we chose these technologies, and how you can get started and use the service yourself!

The complete code is available on [GitHub](https://github.com/JoeJoe1313/PaliGemma-Image-Segmentation). Medium post can be found [here](https://medium.com/@levchevajoana/image-segmentation-with-paligemma-2-mix-transformers-docker-fastapi-and-github-actions-ff6d00253832).

# What is This Project All About?

At its core, this project provides a **FastAPI service** that allows you to perform image segmentation using natural language. You simply provide as input to the REST API:

- A **text prompt** describing what to segment
- An **image** via URL or file upload
- The specific **PaliGemma 2 model** to perform image segmentation

The service then returns:

- The base64 encoded **model input image**
- The base64 encoded segmentation **masks** clearly outlining the desired objects
- The **bounding box coordinates** for each segmented object

The **FastAPI** application is also containerized with **Docker** for consistent deployment across environments. A CI/CD pipeline with **GitHub Actions** is created for automated container builds and registry publishing to Docker Hub.

# Architectural Blueprint: How It All Works Together

Understanding the flow of data and the interaction of components is key. Let’s first take a look at our project structure:

```plaintext
project_folder/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI application and endpoints
│   └── segmentation.py    # Image segmentation logic
├── models/
│   ├── huggingface/       # Cache directory for Hugging Face models
│   └── vae-oid.npz        # VAE model for mask generation
├── .dockerignore
├── .github/
│   └── workflows/         # GitHub Actions for Docker build and push
│     └── docker-build.yml # Workflow to build and push Docker images
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## User & Developer Workflow

Our system is designed with both the end-user and the developer in mind.

<figure>
    <pre class="mermaid">
        graph LR
            User([User]) -->|Provides Image & Prompt| ClientApp[Client Application]
            ClientApp -->|POST Request| FastAPI_Service[FastAPI Service]
            FastAPI_Service -->|Process Input| PaliGemma_Model[PaliGemma Model]
            PaliGemma_Model -->|Generate Segmentation Tokens| VAE_Model[VAE Model]
            VAE_Model -->|Decode Masks| FastAPI_Service
            FastAPI_Service -->|JSON Response | ClientApp
            ClientApp -->|Display Results| User

            Developer([Developer]) -->|Push Code| GitHubRepo[GitHub Repository]
            GitHubRepo -->|Trigger| GitHubActions[GitHub Actions]
            GitHubActions -->|Build & Push Image| DockerRegistry[Docker Hub]
            DockerRegistry -->|Pull Image| DeploymentEnv[Deployment Environment]
            DeploymentEnv -.->|Runs| FastAPI_Service
</pre>
    <figcaption style="text-align: center">Figure 1. User & Developer Workflow</figcaption>
</figure>

**Figure 1** shows the workflow:

- A **User** interacts with a client application, providing an image and a text prompt, and optionally the specific PaliGemma 2 model.
- The **Client Application** sends an HTTP POST request to our **FastAPI Service**.
- The **FastAPI Service** preprocesses the input and feeds it to the **PaliGemma Model**.
- PaliGemma generates segmentation tokens, which are then passed to the **VAE Model**.
- The VAE Model decodes these into pixel-level masks and, along with bounding boxes, sends them back to the API.
The API returns a JSON response to the client.

To visualize the precise sequence of operations when a user requests an image segmentation, the following diagram details the interactions between the core components:

<figure>
    <pre class="mermaid">
        sequenceDiagram
            participant User
            participant Client
            participant FastAPI
            participant SegmentationPy as segmentation.py
            participant PaliGemma as PaliGemma Model
            participant VAE as VAE Model

            User->>+Client: Upload image & prompt
            Client->>+FastAPI: POST /segment
            FastAPI->>+SegmentationPy: call segment_image()
            SegmentationPy->>+PaliGemma: infer with PaliGemma
            PaliGemma-->>-SegmentationPy: (tokens/features)
            SegmentationPy->>+VAE: generate masks
            VAE-->>-SegmentationPy: (pixel masks)
            SegmentationPy-->>-FastAPI: return mask & coords
            FastAPI-->>-Client: JSON response
            Client-->>-User: display results
</pre>
    <figcaption style="text-align: center">Figure 2. Segmentation process</figcaption>
</figure>

This sequence highlights how FastAPI acts as the entry point, delegating the complex segmentation logic to the `segmentation.py` module, which in turn leverages the PaliGemma and VAE models to produce the desired output.

For **developers**, pushing code to GitHub triggers **GitHub Actions**, which automatically builds a Docker image and pushes it to a **Container Registry** (Docker Hub), ready for deployment.

## Inside the Application

Within the Docker container, the application is neatly structured:

<figure>
    <pre class="mermaid">
        graph TD
            subgraph "Docker Container"
                subgraph "app/"
                    main[main.py
                    FastAPI Application]
                    segmentation[segmentation.py
                    Image Segmentation Logic]
                    main -->|imports| segmentation
                end
                
                subgraph "External Dependencies"
                    NP[numpy]
                    TR[transformers]
                    PT[PyTorch]
                    JF[JAX/Flax]
                end
                
                subgraph "Models"
                    PaliGemma[PaliGemma 2 mix]
                    VAE[VAE Checkpoint]
                end
                
                segmentation -->|uses| TR
                segmentation -->|uses| PT
                segmentation -->|uses| JF
                segmentation -->|uses| NP
                
                main -->|loads| PaliGemma
                segmentation -->|loads| VAE
            end
            
            Client[Client Application] -->|HTTP Requests| main
            
            subgraph "API Endpoints"
                segment[POST /segment/]
                root[GET /]
            end
            
            main -->|defines| segment
            main -->|defines| root
            Client -->|calls| segment
            Client -->|calls| root

            style main fill:#c2e0ff,stroke:#0078d7
            style segmentation fill:#c2e0ff,stroke:#0078d7
            style Client fill:#ffd7b5,stroke:#ff8c00
            style segment fill:#d5e8d4,stroke:#82b366
            style root fill:#d5e8d4,stroke:#82b366
</pre>
    <figcaption style="text-align: center">Figure 3. Application Architecture</figcaption>
</figure>

- `app/main.py`: This is the heart of our API, built using FastAPI. It defines the API endpoints like `/` (for a welcome message) and `/segment` (for the actual segmentation).
- `app/segmentation.py`: This module contains all the core logic for image processing, interacting with the PaliGemma and VAE models, and generating the final masks and coordinates. It uses the libraries **JAX**, **Flax** and **Transformers** for efficient model execution and inference.

# Technology Stack Overview

Let’s first understand the key technologies used in the project.

## PaliGemma 2 mix

[PaliGemma 2 mix](https://developers.googleblog.com/en/introducing-paligemma-2-mix/) is a state-of-the-art vision-language model from Google that can comprehend both images and text. It represents a significant advancement in multimodal AI, allowing for natural language-guided image understanding. Once PaliGemma identifies the segments (as tokens), a Variational Autoencoder (VAE) model steps in. It decodes these segmentation tokens into the detailed, pixel-level masks that you see as the output. This particular service uses a VAE checkpoint specifically `vae-oid.npz` for this task. A comprehensive overview of the image segmentation process with Paligemma 2 mix can be found in one of my previous posts [here](https://joejoe1313.github.io/2025-04-15-paligemma-2-mix.html).

## FastAPI

[FastAPI](https://fastapi.tiangolo.com) is a web framework for building APIs with Python. We chose this framework for several compelling reasons:

- Automatic API documentation with **Swagger UI** and ReDoc
Data validation and serialization through **Pydantic** models
- Asynchronous request handling with support for `async`/`await` syntax
- Excellent performance comparable to Node.js and Go
- Built-in dependency injection system
- Security and authentication features out of the box
- WebSocket support and background tasks

In our project, `main.py` uses FastAPI to define the `/segment` endpoint which accepts form data including the prompt, and optionally an image URL or an uploaded image file, and the desired `model_id`.

## Transformers

**Transformers** is a library by **Hugging Face** that provides state-of-the-art pre-trained models for natural language processing and computer vision. For our project, it’s essential because:

- It provides easy access to the PaliGemma models
- Offers a unified API for loading and using different model architectures
- Handles model preprocessing and tokenization
- Supports efficient model inference
- Enables fine-tuning of models if needed

## JAX/Flax

JAX is a high-performance numerical computing library developed by Google. Flax is a neural network library built on top of JAX. Together, they provide:

- Accelerated computation on GPUs and TPUs
- Just-in-time compilation for optimized performance
- Automatic differentiation capabilities
- Functional programming approach to machine learning

In our app **JAX/Flax & Transformers** are used for scalable model execution and inference, JAX/Flax is used for the VAE model which decodes segmentation tokens into pixel-level masks.

## Docker & Docker Compose

### What is Docker?

Docker is a platform that uses OS-level virtualization to deliver software in packages called **containers**. A container is a standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries, and settings.

### Why Docker for This Project?

- **Consistency**: _“It works on my machine”_ is a phrase Docker aims to eliminate. By packaging the application, its dependencies (like specific versions of PyTorch, JAX, Transformers), we ensure it runs identically everywhere - from a developer’s laptop to a production server.
- **Isolation**: Containers run in isolation, preventing conflicts between different applications or dependencies on the same host system.
- **Simplified Deployment**: Docker abstracts away the underlying infrastructure. With a simple `docker-compose up` command, anyone can get the service running without manually installing Python, various libraries, or configuring complex environments.
- **Scalability**: Dockerized applications are inherently easier to scale. Orchestration tools like Kubernetes can manage multiple instances of our container to handle increased load.
- **Multi-Architecture Support**: Our Docker setup supports both `amd64` (common for desktops and servers) and `arm64` (increasingly used in cloud instances and devices like Raspberry Pi) architectures, broadening its usability.

### Key Docker Components Used:

- **`Dockerfile`**

This is the **recipe for building our Docker image**. It specifies the base image (e.g., a Python image), copies our application code (`app/` directory, `requirements.txt`, etc.) into the image, installs all necessary Python packages, and defines the command to run when the container starts (e.g., `uvicorn app.main:app`).

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MODEL_ID=google/paligemma2-3b-mix-448
ENV MODELS_DIR=/app/models

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- **`docker-compose.yml`**

While a `Dockerfile` builds a single image, Docker Compose is used to define and run multi-container Docker applications. In our case, it simplifies running our FastAPI service. It can also manage networks, volumes, and other aspects of the application stack. For this project, it handles setting up the service and importantly, the volume mounting for model persistence.

```yaml
services:
  paligemma-api:
    image: joejoe1313/paligemma-image-segmentation:latest
    ports:
      - "8000:8000"
    environment:
      - MODEL_ID=google/paligemma2-3b-mix-448
      - MODELS_DIR=/app/models
    secrets:
      - hf_token
    volumes:
      - $HOME/.cache/huggingface/hub:/app/models/huggingface
    restart: unless-stopped

secrets:
  hf_token:
    file: $HOME/.cache/huggingface/token
```

- **`.dockerignore`:**

Similar to `.gitignore`, this file lists files and directories that should not be copied into the Docker image during the build process (e.g., local virtual environments, `.git` directory). This keeps the image lean and build times faster.

### Smart Model Management with Volume Mounting

Models, especially large ones like PaliGemma, take time to download. We use Docker’s **volume mounting** feature to map a directory on the host machine to a directory inside the container. This means:

- Models are downloaded once and **persisted** on your host machine.
- They are **reused** across container restarts.
- They can be **shared** if you run multiple instances.
- Updating models becomes easier as you can manage them directly on your host.

The default mount point in our `docker-compose.yaml` file is `$HOME/.cache/huggingface/hub:/app/models/huggingface` which maps the local `$HOME/.cache/huggingface/hub` directory to `/app/models/huggingface` in the container.

## CI/CD with GitHub Actions

GitHub Actions provides automated workflows for continuous integration and continuous delivery (CI/CD). This is crucial for modern software development, thus we have implemented a CI/CD pipeline using **GitHub Actions**. We can see our workflow `.github/workflows/docker-build.yml` below:

```yaml
name: Docker Build and Push

on:
  push:
    branches: main
  pull_request:
    branches: main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          platforms: linux/amd64,linux/arm64
          tags: ${{ vars.DOCKERHUB_USERNAME }}/paligemma-image-segmentation:latest
```

**What does it do?**

- **Trigger**: Every time code is pushed to the `main` branch (or a pull request is made to `main`), the GitHub Actions workflow is automatically triggered.
- **Build**: The workflow checks out the code and builds a multi-architecture (`amd64`/`arm64`) Docker image using the `Dockerfile`.
- **Push**: The newly built image is then pushed to a container registry (like Docker Hub).
- **Tag**: The image is tagged with the unique commit SHA (for traceability) and also with `latest` (for convenience).

**Figure 4** below shows a high level overview of the workflow:

<figure>
    <pre class="mermaid">
        sequenceDiagram
            participant G as GitHub Repo
            participant A as GitHub Actions
            participant D as Docker Registry

            G->>A: on: push / pull_request to main
            activate A
            A-->>A: Login to Docker Registry
            A-->>A: Set up QEMU (for multi-arch)
            A-->>A: Set up Docker Buildx
            A-->>A: Build Docker image (multi-arch)
            A-->>D: Push image (tagged with SHA & latest)
            deactivate A
</pre>
    <figcaption style="text-align: center">Figure 4. GitHub Actions workflow</figcaption>
</figure>

**How to use it in your fork**

If you fork this repository, you can set up your own CI/CD pipeline by adding the following secrets to your GitHub repository settings:

- `DOCKERHUB_USERNAME`: Your Docker Hub username.
- `DOCKERHUB_TOKEN`: Your Docker Hub access token (not your password!).
- You should also update the image in docker-compose.yaml with your username: `{DOCKERHUB_USERNAME}/paligemma-image-segmentation:latest`

This automated pipeline ensures that a fresh, deployable image is always available.

# Getting Started: Installation and Setup

Ready to try it yourself? Here’s how:

## Prerequisites

- **Docker**: Ensure Docker Desktop or Docker Engine is installed and running.
- **Hugging Face Token**: To access gated models like PaliGemma, you’ll need a Hugging Face token. Make sure it’s stored at `$HOME/.cache/huggingface/token` on your host machine, or adjust the path accordingly. The application will use this token when downloading models.

## Setup with Docker Compose:

- Clone the repository:

```bash
git clone https://github.com/JoeJoe1313/PaliGemma-Image-Segmentation.git
cd PaliGemma-Image-Segmentation
```

- Ensure your **Hugging Face token** is in place as mentioned above. The `docker-compose.yml` is set up to mount your local Hugging Face cache, including the token.
- Run the application:

```bash
docker-compose up -d
```

> **Warning**: It’s generally good practice to avoid running Docker commands as a root user unless necessary. Docker Compose should typically be run by a `user` in the `docker group`.

This command will pull the pre-built Docker image and start the FastAPI service on `http://localhost:8000`. The `-dflag` runs it in detached mode.

## Choosing Your PaliGemma Model

You have two ways to specify which PaliGemma model variant to use:

- At **runtime via API**: Pass the `model_id` parameter in your POST request to the `/segment` endpoint.
- Via **Docker Environment Variable**: Set the `MODEL_ID` environment variable when starting the container.

> **Note**: If both are set, the `model_id` parameter in the API request takes precedence.

If a specified model isn’t found in the local cache (`/app/models/huggingface` inside the container, which maps to your `$HOME/.cache/huggingface/hub`), the application will attempt to download it from Hugging Face. **Figure 5** below shows a comprehensive overview of the possible steps.

<figure style="width: 70%; margin: auto;">
    <pre class="mermaid" style="max-width: 300px; margin: auto;">
        flowchart TD
            A[API Request] --> B{Check Local Cache}
            B -->|Found| H[Load from Local Cache]
            B -->|Not Found| C{Has HF Token?}
            
            %% Style definitions
            classDef process fill:#e0e0ff,stroke:#9999ff,color:black
            classDef decision1 fill:#ffe0b0,stroke:#ffbb66,color:black
            classDef decision2 fill:#d0f0d0,stroke:#aaddaa,color:black
            classDef cache fill:#d0e0ff,stroke:#aabbee,color:black
            
            %% Apply styles
            class A,D,F,I,E,Z process
            class B decision1
            class C decision2
            class G,H cache

            C -->|Yes| D[Authenticate with HF]
            C -->|No| E[Try Loading Public Model]
            D --> F[Download Model]
            F --> G[Save to Cache]
            E -->|Success| G
            E -->|Failure| Z[Auth Error]
            G --> H
            H --> I[Use Model]
</pre>
    <figcaption style="text-align: center">Figure 5. Model download scheme</figcaption>
</figure>

# Examples: Putting the API to the Test

Once the service is running (default: `http://localhost:8000`):

- **API Docs**: Visit `http://localhost:8000/docs` for interactive API documentation.

## Health Check (GET /)

Verify the API is up and running.

**Request:**

```python
import requests

response = requests.get("http://localhost:8000/")
print(response.json())
```

**Response:**

```json
{
    "message": "Welcome to the PaliGemma Segmentation API!"
}
```

## Segmenting an Image (POST /segment/)

Form Parameters:

- `prompt` (str, required): Text description of objects to segment (e.g., "segment the red car").
- `image_url` (str, optional): URL of the image to segment.
- `image_file` (UploadFile, optional): Uploaded image file to segment.
- `model_id` (str, optional): Specific PaliGemma model ID to use.

### Using an Image URL

<figure>
    <pre class="mermaid">
        sequenceDiagram
            participant C as Client
            participant S as /segment Endpoint
            C->>S: POST Request with JSON body: { "image_url": "your_image_url.jpg", "prompt": "object to segment" }
            S-->>S: Download Image
            S-->>S: Process with PaliGemma & VAE
            S-->>C: JSON Response: { "image": "base64_input_image", "masks": [ { "mask": "base64_mask_data", "coordinates": [x_min,y_min,x_max,y_max] } ] }
    </pre>
    <figcaption style="text-align: center">Figure 6. Segment request</figcaption>
</figure>

**Request:**

```python
import requests

data = {
    "prompt": "segment left wheel",
    "image_url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg"
}

response = requests.post("http://localhost:8000/segment", data=data)
print(response.json())
```

### Uploading an Image File

**Request:**

```python
import os
import requests

segm_url = "http://localhost:8000/segment"
image_path = "your_image.png"

with open(image_path, "rb") as image_file:
    data = {
        "prompt": "segment the main object" # Adjust prompt as needed
    }
    files = {
        "image_file": (os.path.basename(image_path), image_file, "image/png") # Or image/jpeg
    }

    response = requests.post(segm_url, files=files, data=data)
    print(response.json())
```

### Expected JSON Response Structure:

**Response:**

```python
{
  "image": "base64_encoded_model_input_image_data",
  "masks": [
    {
      "mask": "base64_encoded_mask_data_for_object_1",
      "coordinates": [x_min, y_min, x_max, y_max]
    }
    # ...more masks if multiple instances of the prompt are found
  ]
}
```

See [example.ipynb](https://github.com/JoeJoe1313/PaliGemma-Image-Segmentation/blob/main/example.ipynb) for a demonstration of the segmentation pipeline.

# Conclusion

In this guide, we explored an image segmentation API using PaliGemma 2 mix, FastAPI, Transformers, and Docker. This service enables users to segment objects in images using natural language prompts, opening up a wide range of applications in computer vision, image editing, and data analysis. The containerized application provides a flexible, scalable solution that can be easily deployed across various environments. The combination of FastAPI’s performance and Docker’s portability makes this architecture ideal for production ML applications.

_Happy coding!_
