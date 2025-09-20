---
Title: Chat with Qwen3 on your iPhone: A Step-by-Step Guide
Date: 2025-05-06 00:00
Category: Machine Learning
Tags: ai, ml, vlm, ios, swift, mlx-swift
Slug: chat-qwen3-ios
Status: published
---

Have you ever wanted to run a powerful large language model directly on your iPhone without sending your data to the cloud? Thanks to Apple’s [MLX Swift](https://github.com/ml-explore/mlx-swift) framework, you can now run the remarakably capable [Qwen3](https://qwenlm.github.io/blog/qwen3/) models right on your iPhone.

What makes this exciting is how capable these new models are even with as little as 4B parameters. Based on Qwen’s benchmark reports, Qwen3–4B can rival the performance of Qwen2.5–72B-Instruct, delivering impressive results with just a fraction of the parameters. This development means truly powerful AI can now fit in your pocket.

This blog post will guide you through the entire process from setting up your development environment to testing the model on your device. You can embrace true privacy, and take ownership of your AI experience. Your data stays on your device, where it belongs, and most importantly - you have access to this knowledge powerhouse even with no internet connection.

Medium post can be found [here](https://medium.com/@levchevajoana/chat-with-qwen3-on-your-iphone-a-step-by-step-guide-515bb957cd02).

# Main Steps

The whole process consists of three main steps:

- Enable Developer Mode on your iPhone
- Clone Apple’s MLX Swift Examples [repository](https://github.com/ml-explore/mlx-swift-examples)
- Configure and deploy the Xcode project to your device

# Enable Developer Mode on iPhone

In order to deploy custom apps to your iPhone, you need to enable **Developer Mode**. On your iPhone:

- Go to **Settings &#8594; Privacy & Security &#8594; Developer Mode**  
- Toggle Developer Mode to **On**
Restart your iPhone when prompted

> **NOTE:** It is important to note that your device’s security is reduced in Developer Mode.

# Apple’s MLX Swift Examples Repository

Now that your iPhone is ready for development, let’s get the necessary code. We are going to run the **MLXChatExample**, an example chat app supporting LLMs and VLMs for iOS and macOS, which can be found in the Applications folder in the [mlx-swift-examples](https://github.com/ml-explore/mlx-swift-examples) repository. So, the first step is to clone the repository:

```bash
git clone git@github.com:ml-explore/mlx-swift-examples.git
```

Then, navigate to the cloned directory:

```bash
cd mlx-swift-examples
```

And finally, open the Xcode project:

```bash
open mlx-swift-examples.xcodeproj
```

The above command should open the project directly in Xcode.

# Configure and Deploy the Xcode Project

With the project open in Xcode, you should connect your iPhone to the Mac, and then make a few adjustments.

## Configure the Project

We are interested in deploying the **MLXChatExample** app on your connected iPhone, so you should:

- Change your scheme to **MLXChatExample** by going to **Product &#8594; Scheme &#8594; Choose Scheme** (this opens a dropdown menu from the Xcode’s top bar, which can be selected directly from the bar as well)
- Set the destination to your connected iPhone by going to **Product &#8594; Destination &#8594; Choose Destination**

<figure>
  <img src="../images/2025-05-06-chat-qwen3-ios/config_scheme_dest.png" alt="Configure scheme and destination" class="zoomable" style="display: block; margin: 0 auto">
  <figcaption style="text-align: center">Figure 1. Configure scheme and destination</figcaption>
</figure>

## Add Developer Team

In order to build and run the app we have to assign a development team:

- Select the **mlx-swift-examples** project in the Project Navigator (on the left)
- Go to the **Signing & Capabilities** tab
- Choose your **Team** from the dropdown menu

<figure>
  <img src="../images/2025-05-06-chat-qwen3-ios/developer_team.png" alt="Developer team" class="zoomable" style="display: block; margin: 0 auto">
  <figcaption style="text-align: center">Figure 2. Add developer team</figcaption>
</figure>

# Deploy to Your iPhone

Now we are ready to deploy **MLXChatExample** to our actual device:

- Click the Run button (▶) on the left to run the project, or alternatively choose **Product &#8594; Run**
- You might be asked to authorize Xcode development on your device
- If successful, the app will be downloaded to your iPhone

## Trust Developer Certificate

If this is your first app from this developer team, you would get a message on your iPhone that the app is from an **Untrusted Developer** and you are not allowed to use it. We should allow applications from this developer, so on your iPhone:

- Go to **Settings &#8594; General &#8594; VPN & Device Management**
- Under **Developer App**, tap on your app
Select **Trust “[Developer Name]”** and confirm

## Using Qwen3 on Your iPhone

With that, we are ready to test the MLXChatExample app. Let’s open it:

<figure style="display: flex; justify-content: center; gap: 1rem; margin: 0;">
  <div>
    <img src="../images/2025-05-06-chat-qwen3-ios/3_1.png" alt="App launch 1" class="zoomable" />
  </div>
  <div>
    <img src="../images/2025-05-06-chat-qwen3-ios/3_2.png" alt="App launch 2" class="zoomable" />
  </div>
</figure>
<figcaption style="text-align: center; width: 100%; margin-top: 0.5rem;">
    Figure 3. Left: MLXChatExample app default screen | Right: models dropdown menu
</figcaption>

By default, the app loads with the **llama3.2:1b** model. You can select different models from the dropdown menu in the upper right corner, see **Figure 3**. Let’s choose **qwen3:4b**, which runs successfully on an iPhone 14 Pro, and type our first query.

If this is the first run for a given model, we have to wait for the model to download from Hugging Face to our cache. Below, in **Figure 4**, we can see our first query and how it triggers the model download (the arrow on top), and when clicking on the arrow we can see the download progress.

<figure style="display: flex; justify-content: center; gap: 1rem; margin: 0;">
  <div>
    <img src="../images/2025-05-06-chat-qwen3-ios/4_1.png" alt="Init query" class="zoomable" />
  </div>
  <div>
    <img src="../images/2025-05-06-chat-qwen3-ios/4_2.png" alt="Download model" class="zoomable" />
  </div>
</figure>
<figcaption style="text-align: center; width: 100%; margin-top: 0.5rem;">
    Figure 4. Left: first query for a model triggering model download | Right: model downloading progress
</figcaption>

The Qwen3 models can have thinking enabled and disabled. At the moment the app doesn’t support a toggle to manually switch between both modes. The default behaviour is to use thinking (the thought process output is encapsulated between the tags `<think></think>`), and in order to disable the thinking we have to add **/no_think** at the end of our prompt. In this case the think tags appear with nothing between them. Refer to **Figure 5** below.

<figure style="display: flex; justify-content: center; gap: 1rem; margin: 0;">
  <div>
    <img src="../images/2025-05-06-chat-qwen3-ios/5_1.png" alt="Gen 1" class="zoomable" />
  </div>
  <div>
    <img src="../images/2025-05-06-chat-qwen3-ios/5_2.png" alt="Gen 2" class="zoomable" />
  </div>
</figure>
<figcaption style="text-align: center; width: 100%; margin-top: 0.5rem;">
    Figure 5. Left: query with default thinking behaviour | Right: query with disabled thinking
</figcaption>

# The Benefits of On-Device AI

Running models like Qwen3 directly on your device offers several significant advantages:

- **Complete Privacy:** Your conversations never leave your device. No server logs, no data collection, just you and your AI.
- **Works Offline:** You have all the world’s knowledge in your pocket wherever you are, without depending on internet connection availability. Need AI assistance while traveling, hiking, or in areas with poor connectivity? Local models work anywhere, anytime.
- **No Subscription Fees:** Once you’ve set up the model, there are no ongoing costs.
- **No Rate Limits:** Chat as much as you want without hitting quotas.
- **Reduced Environmental Impact:** On-device inference eliminates the carbon footprint associated with massive data centers processing your requests.

# Conclusion

While cloud-based solutions may offer larger models with excellent performance, the gap is closing rapidly as efficiency improvements make smaller models surprisingly capable. The Qwen3 models are an excellent example for this, and are a “living” proof of the rapid advancements in the field of AI. The MLX Swift framework from Apple makes powerful machine learning accessible to everyday users on their personal devices. This shift from cloud-dependent to local-first AI is just beginning.

***Own your AI. Own your data. Go local.***
