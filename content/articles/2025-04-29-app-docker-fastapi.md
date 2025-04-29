---
Title: Build an Image Segmentation App with Docker, FastAPI, and GitHub Actions
Date: 2025-04-29 07:00
Category: Machine Learning
Tags: ai, ml, vlm, docker, fastapi, github-actions
Slug: 2025-04-29-app-docker-fastapi
Status: draft
---

In today's fast-paced machine learning landscape, deploying AI models efficiently is just as important as developing them. In this blog post, we are going to explore how to create an image segmentation application using Google's PaliGemma 2 Mix model, containerized with Docker, and served through a FastAPI backend. We are also going to set up a CI/CD pipeline using GitHub Actions to automate buidling the Docker image and pushing it to Docker Hub.

# Introduction

In this tutorial, we will build an image segmentation application that leverages the PaliGemma 2 Mix model for precise image segmentation. The application will be designed to take an image URL and a text prompt as input, perform segmentation, and return a base64-encoded mask along with bounding box coordinates.

# Architecture

<figure>
  <pre class="mermaid">
      graph LR
      User([User]) -->|Uploads Image| Client[Client Application]
      User -->|Provides Prompt| Client
      
      Client -->|HTTP POST Request| API[FastAPI Service]
      API -->|Process Image| PaliGemma[PaliGemma Model]
      PaliGemma -->|Generate Segmentation| VAE[VAE Model]
      VAE -->|Create Masks| API
      
      API -->|JSON Response| Client
      Client -->|Display Results| User
      
      style User fill:#f9d5e5,stroke:#d64161,stroke-width:2px
      style Client fill:#eeeeee,stroke:#333333
      style API fill:#b5e7a0,stroke:#86af49
      style PaliGemma fill:#b8e0d2,stroke:#6a9c89
      style VAE fill:#d0e1f9,stroke:#7fa6bc
  </pre>
  <figcaption style="text-align: center">Figure 1. User workflow</figcaption>
</figure>

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
    
    style Docker fill:#e7f4ff,stroke:#0078d7
    style main fill:#c2e0ff,stroke:#0078d7
    style segmentation fill:#c2e0ff,stroke:#0078d7
    style Client fill:#ffd7b5,stroke:#ff8c00
    style segment fill:#d5e8d4,stroke:#82b366
    style root fill:#d5e8d4,stroke:#82b366
  </pre>
  <figcaption style="text-align: center">Figure 2. App architecture</figcaption>
</figure>

<figure>
<pre class="mermaid">
    graph TD
    Client[Client] -->|HTTP Request with Image URL & Prompt| API[FastAPI Server]
    API -->|Process Request| Model[PaliGemma 2 Mix Model]
    Model -->|Generate Segmentation| API
    API -->|Return JSON with Mask & Coordinates| Client
    
    subgraph Docker Container
    API
    Model
    end;
</pre>
<figcaption style="text-align: center">Figure 3. System Architecture</figcaption>
</figure>

# Project Structure

```
project_folder/
├── app/
│   ├── main.py           # FastAPI application code
│   └── segmentation.py   # PaliGemma integration code
├── models/
│   └── vae-oid.npz       # Pre-trained model weights
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```
