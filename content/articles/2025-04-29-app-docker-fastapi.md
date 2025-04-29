---
Title: Build an Image Segmentation App with Docker, FastAPI, and GitHub Actions
Date: 2025-04-29 07:00
Category: Machine Learning
Tags: ai, ml, vlm, docker, fastapi, github-actions
Slug: 2025-04-29-app-docker-fastapi
Status: draft
---

In today's fast-paced machine learning landscape, deploying AI models efficiently is just as important as developing them. In this blog post, we are going to explore how to create an image segmentation application using Google's PaliGemma 2 Mix model, containerized with Docker, and served through a robust FastAPI backend. We are also going to set up a CI/CD pipeline using GitHub Actions to automate buidling the Docker image and pushing it to Docker Hub.

<figure>
  <img src="../images/2025-04-29-app-docker-fastapi/user_workflow.png" alt="Cow output" style="display: block; margin: 0 auto">
  <figcaption style="text-align: center">Figure 1. User workflow</figcaption>
</figure>

<figure>
  <img src="../images/2025-04-29-app-docker-fastapi/app_architecture.png" alt="Cow output" style="display: block; margin: 0 auto">
  <figcaption style="text-align: center">Figure 2. App architecture</figcaption>
</figure>
