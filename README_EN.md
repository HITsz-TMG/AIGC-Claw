<p align="center">
  <img src="video-claw-pics/banner.png" width="100%" />
</p>

<h1 align="center">
  VideoClaw: AI Creative Video Production Agent
</h1>

<p align="center">
  <a href="./README.md">简体中文</a> | <b>English</b>
</p>

<h3 align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue.svg" alt="Version">
  <a href="https://github.com/HITsz-TMG/VideoClaw/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/HITsz-TMG/VideoClaw?style=flat-square" alt="License">
  </a>
  <a href="https://github.com/HITsz-TMG/VideoClaw/stargazers">
    <img src="https://img.shields.io/github/stars/HITsz-TMG/VideoClaw?style=flat-square&logo=github" alt="Stars">
  </a>
  <a href="https://github.com/HITsz-TMG/VideoClaw/fork">
    <img src="https://img.shields.io/github/forks/HITsz-TMG/VideoClaw?style=flat-square&logo=github" alt="Forks">
  </a>
  <img src="https://img.shields.io/badge/Python-3.9+-purple.svg" alt="Python">
  <a href="#method-3-openclaw-auto-setup">
    <img src="https://img.shields.io/badge/OpenClaw-Compatible-ff4444?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6IiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==" alt="OpenClaw Compatible">
  </a>
</h3>

<p align="center">
  <b><i><font size="5">Talk to <a href="https://github.com/openclaw/openclaw">OpenClaw</a> directly: "Generate a video about X" -> done.</font></i></b>
</p>

<div align="center">

📺 [**Bilibili**](https://space.bilibili.com/2031891503?spm_id_from=333.1007.0.0)  ▶️ [**YouTube**](https://www.youtube.com/@imryanxu)  📖 [**Integration Guide**](#method-3-openclaw-auto-setup)  🦀 [**ClawHub**](https://clawhub.ai/hit-cxf/video-claw)

<a href="https://trendshift.io/repositories/24295" target="_blank"><img src="https://trendshift.io/api/badge/repositories/24295" alt="HITsz-TMG%2FVideo-Claw | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

</div>


# 💥 News

- `2026/3/27`: 🎬 VideoClaw was officially released, supporting full workflow automation from idea to video generation, with user intervention and adjustment available at any time.
- `2026/4/9`: ♾️ VideoClaw was optimized for short dramas, adding infinite continuation and customizable plots.
- `2026/4/29`: 🧩 Added three features: commentary-style short videos, action transfer, and digital human talking videos.
- `2026/5/8`: ⚙️ Added WebUI configuration for APIs and default models, with one-click installation support.
- `2026/5/13`: 🎞️ Integrated Pixelle-Video HTML templates into commentary-style short videos.


# 📖 Overview

<p align="center">
  <img src="video-claw-pics/workflow.png" width="100%" />
</p>

VideoClaw is an AI director system for creative video production. **You only need to provide an idea, a story outline, or even a vague concept. The system will break it down into an executable filmmaking workflow, continuously producing intermediate assets that can be reviewed, confirmed, revised, and delivered, until a complete final video is generated.**

It is not a one-shot text-to-video tool. It is a full production line covering **script planning -> character and scene design -> storyboard planning -> reference image generation -> video generation -> post-production editing**. Instead of giving you a black-box result, VideoClaw behaves like a collaborative AI directing team: each stage informs the next, and every key node is visible, editable, and extensible.

# 📺 Demos

## 🎬 VideoClaw

<details>
<summary><b>Click to view WebUI UI design</b></summary>

| Stage | Demo | Description |
|---|---|---|
| Home | <img src="video-claw-pics/workflow_demo/homepage.png" width="800" /> | Displays the system overview, supports viewing historical projects, creating new projects, and global configuration (API keys and default model settings). This is the starting point of the creation workflow. |
| Script Planning | <img src="video-claw-pics/workflow_demo/stage-1.png" width="800" /> | Enter a creative title and project synopsis, and the system automatically generates a structured multi-scene script (including narration and dialogue), with support for intelligent continuation of subsequent plots. |
| Character/Scene Design | <img src="video-claw-pics/workflow_demo/stage-2.png" width="800" /> | Automatically extracts core characteristics of characters and scenes from the script, generating stylistically consistent reference concept art as the visual basis for later storyboard generation. |
| Storyboard Planning | <img src="video-claw-pics/workflow_demo/stage-3.png" width="800" /> | Breaks each script scene into continuous visual storyboards, specifying camera perspective, action descriptions, and reference content in detail to ensure narrative coherence. |
| Reference Image Generation | <img src="video-claw-pics/workflow_demo/stage-4.png" width="800" /> | Generates high-quality, high-precision reference base images for each storyboard scene, controlling lighting details and composition as key visual references for video generation. |
| Video Generation | <img src="video-claw-pics/workflow_demo/stage-5.png" width="800" /> | Calls mainstream high-performance video generation models (such as Wan and Kling) to convert storyboard images into dynamic clips. |
| Final Editing | <img src="video-claw-pics/workflow_demo/stage-6.png" width="800" /> | Aggregates all generated video clips and exports a publishable final video with one click. |

</details>

### 📱 Series 1: A Programmer Uses OpenClaw to Acquire His Former Company After Being Laid Off (Realistic Short Drama)
> 8 episodes in total, an underdog story with twists and reversal. The first 6 episodes were generated initially, followed by 2 continued episodes.

<table>
  <tr>
    <td align="center" valign="top" width="25%">
      <a href="https://github.com/user-attachments/assets/1d095b82-3a72-4acc-9ca1-3ff4a6189232">
        <img src="https://github.com/user-attachments/assets/47b1621e-5c5a-4cb1-9c51-dcf723ac5fda" width="100%" alt="Play Episode 1">
      </a>
      <br><b>▶️ Episode 1</b><br>Laid Off
    </td>
    <td align="center" valign="top" width="25%">
      <a href="https://github.com/user-attachments/assets/489c5343-6345-4bce-81dc-bf6012b9c1cf">
        <img src="https://github.com/user-attachments/assets/b0dd3781-b767-45c2-9fe2-3dc7421fbf80" width="100%" alt="Play Episode 2">
      </a>
      <br><b>▶️ Episode 2</b><br>Late-Night Departure, First Breakthrough
    </td>
    <td align="center" valign="top" width="25%">
      <a href="https://github.com/user-attachments/assets/359809cf-678b-429c-bafa-55ff50fd3277">
        <img src="https://github.com/user-attachments/assets/fcfd191c-61f9-484f-a036-ce717620c827" width="100%" alt="Play Episode 3">
      </a>
      <br><b>▶️ Episode 3</b><br>AI Funding, Old Employer in Crisis
    </td>
    <td align="center" valign="top" width="25%">
      <a href="https://github.com/user-attachments/assets/5561a04a-5ab3-4099-bc63-2fdbcc48f8e9">
        <img src="https://github.com/user-attachments/assets/14a535da-b0eb-4b4b-8039-517bac692696" width="100%" alt="Play Episode 4">
      </a>
      <br><b>▶️ Episode 4</b><br>Acquiring Xingyao
    </td>
  </tr>
  <tr>
    <td align="center" valign="top">
      <a href="https://github.com/user-attachments/assets/ae4c3618-1990-4ff5-ad85-e09f23b08f7d">
        <img src="https://github.com/user-attachments/assets/e2d7fbae-d945-461f-be2f-5eb781337cac" width="100%" alt="Play Episode 5">
      </a>
      <br><b>▶️ Episode 5</b><br>Acquisition, Liquidation, New Life
    </td>
    <td align="center" valign="top">
      <a href="https://github.com/user-attachments/assets/4ddbb725-34d8-478b-97bc-5d7143f73101">
        <img src="https://github.com/user-attachments/assets/02a8f7d4-04c9-460e-9ba1-07d594ffcd24" width="100%" alt="Play Episode 6">
      </a>
      <br><b>▶️ Episode 6</b><br>New Life, Looking Back
    </td>
    <td align="center" valign="top">
      <a href="https://github.com/user-attachments/assets/1c1e5970-aaea-44ba-b041-5d551905bfde">
        <img src="https://github.com/user-attachments/assets/053be420-20e8-423e-8379-f1d1554546c5" width="100%" alt="Play Episode 7">
      </a>
      <br><b>▶️ Episode 7</b><br>Technology Backfires
    </td>
    <td align="center" valign="top">
      <a href="https://github.com/user-attachments/assets/e56e6784-6e49-4891-b0bc-a32308dd2145">
        <img src="https://github.com/user-attachments/assets/19a50fcd-0a5a-4649-bb63-c7867e945d46" width="100%" alt="Play Episode 8">
      </a>
      <br><b>▶️ Episode 8</b><br>Upholding Ethics, Getting Through Together
    </td>
  </tr>
</table>

<br>

### 🖥️ Series 2: The Village Teacher (Sci-Fi Comic Drama)
> 5 episodes in total, a tribute to the inheritance of civilization.

<table>
  <tr>
    <td align="center" valign="top" width="50%">
      <a href="https://github.com/user-attachments/assets/1ffe7b06-73e9-44cd-ad3f-afced5239f97">
        <img src="https://github.com/user-attachments/assets/e1328cf7-23fe-48d8-9ae6-a7beeae6dda9" width="100%" alt="Play Episode 1">
      </a>
      <br><b>▶️ Episode 1</b><br>The Last Lesson
    </td>
    <td align="center" valign="top" width="50%">
      <a href="https://github.com/user-attachments/assets/7547e5d3-872c-4344-8727-ee2be109797d">
        <img src="https://github.com/user-attachments/assets/65bc3866-6405-4033-97b2-54de42a61402" width="100%" alt="Play Episode 2">
      </a>
      <br><b>▶️ Episode 2</b><br>The Cleansing Plan
    </td>
  </tr>
  <tr>
    <td align="center" valign="top">
      <a href="https://github.com/user-attachments/assets/affed408-4df7-4ce7-9681-8f4ed45a6fcf">
        <img src="https://github.com/user-attachments/assets/81acd075-e4f1-4621-b2dc-b2d87ed83b81" width="100%" alt="Play Episode 3">
      </a>
      <br><b>▶️ Episode 3</b><br>A Dying Entrustment
    </td>
    <td align="center" valign="top">
      <a href="https://github.com/user-attachments/assets/dc7a85a8-6912-4443-a995-3d8f3ca30bc8">
        <img src="https://github.com/user-attachments/assets/738c539e-8f90-47f5-9983-f3ac35d3d385" width="100%" alt="Play Episode 4">
      </a>
      <br><b>▶️ Episode 4</b><br>Questions of Life and Death
    </td>
  </tr>
  <tr>
    <td align="center" valign="top">
      <a href="https://github.com/user-attachments/assets/1fb889c5-0e2b-40fa-a438-7399322ada47">
        <img src="https://github.com/user-attachments/assets/ce4a1ac4-7308-43ba-a803-fc77b9b9561e" width="100%" alt="Play Episode 5">
      </a>
      <br><b>▶️ Episode 5</b><br>Light of Civilization
    </td>
    <td align="center" valign="top">
      <!-- Empty cell to keep table layout aligned -->
    </td>
  </tr>
</table>

<br>

### 🎞️ More Demos
<details>
<summary><b>More Micro-Drama Clips</b></summary>

<table>
  <tr>
    <td align="center" valign="top" width="33%">
      <video src="https://github.com/user-attachments/assets/63c2f33c-da50-44f0-8c26-a65611479d6a" controls width="100%" preload="none"></video>
      <br><b>London Mystery</b>
    </td>
    <td align="center" valign="top" width="33%">
      <video src="https://github.com/user-attachments/assets/d7c65cad-05b9-46c8-ab0e-96e39909f978" controls width="100%" preload="none"></video>
      <br><b>A Dog's Purpose</b>
    </td>
    <td align="center" valign="top" width="33%">
      <video src="https://github.com/user-attachments/assets/ec67546e-2d3d-4b34-b1ad-7d860a9bc1aa" controls width="100%" preload="none"></video>
      <br><b>Drone Delivers Lychees</b>
    </td>
  </tr>
</table>

</details>

<br>

<details>
<summary><b>WeChat Interaction</b></summary>
<div align="center">

| | | | |
|:---:|:---:|:---:|:---:|
| ![WeChat 1](video-claw-pics/wechat_demo/wechat_1.jpg) | ![WeChat 2](video-claw-pics/wechat_demo/wechat_2.jpg) | ![WeChat 3](video-claw-pics/wechat_demo/wechat_3.jpg) | ![WeChat 4](video-claw-pics/wechat_demo/wechat_4.jpg) |

</div>
</details>

<br>

<details>
<summary><b>Feishu Interaction</b></summary>
<div align="center">

| | | | |
|:---:|:---:|:---:|:---:|
| ![Feishu 1](video-claw-pics/feishu_demo/feishu_1.jpg) | ![Feishu 2](video-claw-pics/feishu_demo/feishu_2.jpg) | ![Feishu 3](video-claw-pics/feishu_demo/feishu_3.jpg) | ![Feishu 4](video-claw-pics/feishu_demo/feishu_4.jpg) |

</div>
</details>

<!-- 
## 🧩 Quick Creation

<details>
<summary><b>Click to view WebUI UI design</b></summary>

| Pipeline | Demo | Frontend Entry | Description |
|---|---|---|---|
| Artistic Short Video | <img src="video-claw-pics/pipeline_demo/standard.png" width="600" /> | Sidebar: "Artistic Short Video" | Supports both "Image Montage / Dynamic Video" and "Creative Inspiration / Full Script" modes. The system splits narration by periods, generates an image and voiceover for each segment, then either composes image-based clips or calls an image-to-video model for dynamic segments. Optional title and subtitles are supported. |
| Action Transfer | <img src="video-claw-pics/pipeline_demo/action_transfer.png" width="600" /> | Sidebar: "Action Transfer" | Takes a reference image, an action video, and a prompt, then calls a video model with action-transfer capability to generate the result video. |
| Digital Human Talking Video | <img src="video-claw-pics/pipeline_demo/digital_human.png" width="600" /> | Sidebar: "Digital Human Talking Video" | Takes a character image and talking script, generates sentence-level speech and digital human video clips, uses the previous clip's tail frame to continue multi-clip generation, and replaces the final video audio with the generated speech. |

</details>

### Artistic Short Video

<div align="center">
<table align="center" border="0" cellspacing="0" cellpadding="0" style="border:none; border-collapse:collapse; margin:0 auto;">
  <tr>
    <td align="center" valign="top" width="25%" style="border:none;"></td>
    <td align="center" valign="top" width="25%" style="border:none;">
      <video src="https://github.com/user-attachments/assets/7a674bb7-6ee9-4b83-bfd3-0d880127b632" controls width="100%" preload="none"></video>
      <br><b>▶️ Mountain and River Dreams</b>
    </td>
    <td align="center" valign="top" width="25%" style="border:none;">
      <video src="https://github.com/user-attachments/assets/a62c8184-322d-4c06-b16f-19660766e816" controls width="100%" preload="none"></video>
      <br><b>▶️ The Vastness of Life</b>
    </td>
    <td align="center" valign="top" width="25%" style="border:none;"></td>
  </tr>
</table>
</div>

<br>
 -->

# ✨ Features

| Capability | Description |
|---|---|
| 🎬 **End-to-end generation from idea to final cut** | Connects scripts, characters, storyboards, reference images, video clips, and post-production into one complete workflow, upgrading scattered generation abilities into a full video production pipeline. |
| 🖼️ **Storyboard-driven controllable creation** | Uses structured scripts, storyboard planning, and reference image generation to make character consistency, shot expression, and visual style more stable and controllable. |
| ✍️ **Editable, continuable, and regenerable** | Supports intelligent continuation of plots and storyboards, while also allowing character, reference image, and video stages to be edited and regenerated without starting from scratch. |
| 🧩 **Lightweight Pipeline tasks** | Supports three one-shot tasks: commentary-style short videos, action transfer, and digital human talking videos. They are suitable for batch generation of image/text or dynamic short videos, action-transfer videos, and talking-head videos. |
| 📲 **Local deployment, multi-platform collaboration, and asset retention** | Supports Web UI, WeChat / Feishu collaboration, OpenClaw Skill integration, and full-chain retention of scripts, images, video clips, and final outputs. |

---

# 🚀 Quick Start

## Method 1: One-Click Installation (Recommended)

**Linux / MacOS**:

```bash
# 1. Clone the repository
git clone https://github.com/HITsz-TMG/VideoClaw.git
cd VideoClaw

# 2. Enter the app directory and run the installer
cd video-claw/video-claw
chmod +x install.sh
./install.sh

# 3. back to root dir
cd ../..
```

**Windows**:

```bat
# 1. Clone the repository
git clone https://github.com/HITsz-TMG/VideoClaw.git
cd VideoClaw

# 2. Enter the app directory and run the installer
cd video-claw\video-claw
install.bat

# 3. back to root dir
cd ../..
```

The installer checks Python, Node.js, npm, and ffmpeg, installs backend and frontend dependencies, copies `backend/config.yaml.example` to `backend/config.yaml`, and builds the frontend. After installation, fill in model service API keys in `backend/config.yaml` and confirm the main-workflow default models under `models`. You can also start the frontend and edit these settings from the "Settings" page at the bottom of the sidebar. Then start the services:

```bash
# Start backend
cd video-claw/video-claw/backend
uv run python api_server.py

# Start frontend in a new terminal
cd video-claw/video-claw/frontend
npm start
```

By default, the backend runs at `http://localhost:8000`, and the frontend runs at `http://localhost:3000`.

If you only want to install dependencies and skip the frontend build temporarily, run:

```bash
AIGC_DIRECTOR_SKIP_FRONTEND_BUILD=1 ./install.sh
```

## Method 2: Manual Installation

```bash
# 1. Clone the repository
git clone https://github.com/HITsz-TMG/Video-Claw.git
cd Video-Claw

# 2. Configure and start the backend
cd video-claw/video-claw/backend

# Install backend dependencies
uv sync

# Configure backend YAML
cp config.yaml.example config.yaml
# Edit config.yaml, fill in API keys, and confirm main-workflow default models
# You can also use the frontend Settings page after startup

# Start backend
uv run python api_server.py
# Service runs at http://localhost:8000
```

```bash
# 3. Configure and start the frontend in a new terminal
cd video-claw/video-claw/frontend
npm install
npm run build
npm start
# Visit http://localhost:3000
```

If `uv` is not installed, you can also create a Python virtual environment manually and install backend dependencies with `pip install -r requirements.txt`.

## Method 3: OpenClaw Auto Setup

Send this message to OpenClaw:

```text
Please clone this git repository: https://github.com/HITsz-TMG/Video-Claw.git
Then recursively copy the video-claw folder inside Video-Claw to .openclaw/workspace/skills and use it as an AIGC-related skill.
```

When using it, it is recommended to explicitly say "use video-claw":

```text
Use video-claw to generate a video with the content "A Dog's Purpose".
```

## Method 4: Install via ClawHub

Make sure `clawhub-cli` is installed locally.

Open a terminal and run the following command. Choose `yes` for every prompt.

```bash
clawhub install video-claw
```

After installation, ClawHub will copy `video-claw` into `workspace/skills` or your specified skills directory.

Then you can follow Method 1 for one-click installation or Method 2 for manual setup, or let OpenClaw build and run the project for you.

The first time you use `video-claw`, if the project has not been built manually, OpenClaw will automatically build and start both the backend and frontend. This may take some time because setup involves dependency installation and compilation.

---

# 🔧 Configuration

<details>
<summary><b>Click to expand full requirements and configuration</b></summary>

## Requirements

- **Python**: 3.9+
- **Node.js**: 18+
- **npm**: 9+

## Backend Configuration

Backend configuration is stored in `video-claw/backend/config.yaml` using a lowercase hierarchical YAML structure. You can edit this file directly, or open the frontend "Settings" page from the bottom of the sidebar.

- `api_providers` stores API keys, base URLs, and proxy toggles for each model provider.
- `models` stores default models for the **main workflow** home page. When creating a project, the frontend reads these defaults first and sends the concrete model parameters to the backend. The backend no longer silently chooses fallback models for the main workflow; missing model parameters will return an error.
- Pipelines (Artistic Short Video, Action Transfer, and Digital Human Talking Video) do not use these main-workflow defaults. Choose their models separately on each Pipeline page.

## Frontend Settings Page

After starting both the backend and frontend, open the "Settings" page from the bottom of the left sidebar. You do not have to edit YAML manually for common configuration:

- Fill in or update API Key / Access Key / Secret Key values for OpenAI, Gemini, DeepSeek, DashScope, Volcengine ARK, Kling, and other configured providers.
- Edit each provider's `base_url`, `enable_proxy`, and the shared proxy address `api_providers.common.proxy`.
- Select main-workflow default models, including `llm`, `vlm`, `image_t2i`, `image_it2i`, `video`, `video_ratio`, and `eval`.
- Saving writes the values back to `backend/config.yaml`. API keys, proxy settings, and default models are read by newly created projects; service startup fields such as `server.host` and `server.port` require restarting the backend to fully take effect.

```yaml
project_name: Video-Claw

server:
  host: 127.0.0.1
  port: 8000
  debug: false

api_providers:
  common:
    print_model_input: false
    proxy: ''
  openai:
    api_key: your_openai_key
    base_url: https://api.openai.com/v1
    enable_proxy: false
  gemini:
    api_key: your_gemini_key
    base_url: https://generativelanguage.googleapis.com/v1beta
    enable_proxy: false
  deepseek:
    api_key: your_deepseek_key
    base_url: https://api.deepseek.com/v1
    enable_proxy: false
  minimax:
    api_key: your_minimax_key
    base_url: https://api.minimax.io/v1
    enable_proxy: false
  dashscope:
    api_key: your_dashscope_key
    base_url: https://dashscope.aliyuncs.com/api/v1
    enable_proxy: false
  ark:
    api_key: your_ark_key
    base_url: https://ark.cn-beijing.volces.com/api/v3
    enable_proxy: false
  kling:
    access_key: your_kling_access_key
    secret_key: your_kling_secret_key
    enable_proxy: false

models:
  llm: qwen3.5-plus
  vlm: qwen3.5-plus
  image_t2i: doubao-seedream-5-0-260128
  image_it2i: doubao-seedream-5-0-260128
  video: wan2.7-i2v
  video_ratio: '16:9'
  eval: qwen3.5-plus
```

<!-- `api_providers.common.proxy` is the only proxy address. Each provider decides whether to use it via `enable_proxy`, which is disabled by default, so different model calls in the same process do not pollute each other. Changes to service startup fields such as `server.host` and `server.port` require restarting the backend to fully take effect. API keys, proxy settings, and main-workflow defaults under `models` are read by new project creation and model calls. -->

## API Keys and Model Providers

| Provider | Config fields | Common use |
|:---:|:---|:---|
| **OpenAI** | `api_providers.openai.api_key` / `base_url` | GPT text/vision models and OpenAI image models |
| **Gemini** | `api_providers.gemini.api_key` / `base_url` | Gemini text and vision models |
| **DeepSeek** | `api_providers.deepseek.api_key` / `base_url` | DeepSeek text models |
| **MiniMax** | `api_providers.minimax.api_key` / `base_url` | MiniMax text models |
| **DashScope** | `api_providers.dashscope.api_key` / `base_url` | Qwen, Wan image/video models, and related Alibaba Cloud services |
| **Volcengine ARK** | `api_providers.ark.api_key` / `base_url` | Seedream image models and Seedance video models |
| **Kling** | `api_providers.kling.access_key` / `secret_key` / `base_url` | Kling video generation |

You only need to fill in the provider keys required by the models you choose. For example, if the main workflow uses a `doubao-seedream-*` image model, configure `ark.api_key`; if it uses a `wan*` video model, configure `dashscope.api_key`. If you choose different models on a Pipeline page, make sure the corresponding provider key is also configured.

## Available Models

| Type | Models |
|:---:|:---|
| **LLM** | qwen3.6-max-preview, qwen3-max, deepseek-chat, deepseek-reasoner, deepseek-v4-flash, deepseek-v4-pro, MiniMax-M3, MiniMax-M2.7, gpt-4o, gpt-5, gpt-5.4, gemini-2.5-flash, gemini-2.0-flash, kimi-k2.6 |
| **VLM** | qwen3.6-plus, qwen3.6-flash, kimi-k2.6, gpt-5.4, gemini-2.5-flash-image, gemini-2.0-flash |
| **Text-to-Image** | wan2.7-image, wan2.7-image-pro, wan2.6-t2i, doubao-seedream-5.0/4.5/4.0, gpt-image-2 |
| **Image-to-Image** | wan2.7-image, wan2.7-image-pro, doubao-seedream-5.0/4.5/4.0, gpt-image-2 |
| **Video Generation** | wan2.7-i2v, wan2.6-i2v-flash, doubao-seedance-2.0 (Normal/Fast), kling-v3/v2.6/v2.5 |

Model information is defined in `video-claw/video-claw/backend/models/config_model.py`. The frontend and Pipeline APIs filter models by capability tags, such as text generation, image generation, image-to-video, action transfer, and TTS.

</details>


# Artifacts and Storage

All tasks metadata and generated artifacts are stored under `video-claw/video-claw/backend/code/`.

<details>
<summary><b>Click to expand Storage Structure and Identifiers</b></summary>

## 📁 Storage Structure

```text
video-claw/video-claw/backend/code/
├── data/
│   ├── tasks/                  # Pipeline task metadata (JSON)
│   └── sessions/               # AIGC-Claw session metadata (JSON)
└── result/
    ├── task/                   # Pipeline generated artifacts (by Task ID)
    │   └── <task_id>/          # e.g., 20260514_204946_961f95d9
    │       ├── audio_xx.mp3    # Audio segments
    │       ├── video_xx.mp4    # Video segments
    │       ├── storyboard.json # Storyboard data
    │       └── final.mp4       # Final combined video
    ├── image/                  # AIGC-Claw generated images
    │   └── <session_id>/       # By Session ID
    │       ├── Assets/         # Character and setting assets
    │       │   ├── characters/ # Character reference images
    │       │   └── settings/   # Setting reference images
    │       └── Scenes/         # Generated storyboard reference images
    ├── video/                  # AIGC-Claw generated videos
    │   └── <session_id>/       # By Session ID
    └── script/                 # AIGC-Claw generated script/storyboard data
```

## 🆔 Identifiers

- **Task ID**: Format: `YYYYMMDD_HHMMSS_RandomHash` (e.g., `20260514_204946_961f95d9`), used to uniquely identify a Pipeline task.
- **Session ID**: Millisecond-level timestamp (e.g., `1778810088325`), used to associate interaction context and generated images in the main workflow.

</details>

# 🙏 Acknowledgments

The idea and design of Video-Claw were inspired by [Pixelle-Video](https://github.com/AIDC-AI/Pixelle-Video), [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw), [huobao-drama](https://github.com/chatfire-AI/huobao-drama), [Flova](https://www.flova.ai), and [libtv-skills](https://github.com/libtv-labs/libtv-skills).


# 📚 Related Work

| Framework | Paper Information |
|:---:|---|
| <img src="./FilmAgent-pics/framework.png" width="420" alt="FilmAgent framework"/> | **[SIGGRAPH Asia 2024] FilmAgent: Automating Virtual Film Production Through a Multi-Agent Collaborative Framework**<br>*Zhenran Xu, Jifang Wang, Longyue Wang, Zhouyi Li, Senbao Shi, Baotian Hu, Min Zhang*<br>[[Paper](https://doi.org/10.1145/3681758.3698014)] [[GitHub](https://github.com/HITsz-TMG/Video-Claw/blob/main/FilmAgent.md)] |
| <img src="https://github.com/HITsz-TMG/Anim-Director/blob/main/Anim-Director/assets/visualeg.png" width="420" alt="Anim-Director result"/> | **[SIGGRAPH Asia 2024] Anim-Director: A Large Multimodal Model Powered Agent for Controllable Animation Video Generation**<br>*Yunxin Li, Haoyuan Shi, Baotian Hu, Longyue Wang, Jiashun Zhu, Jinyi Xu, Zhen Zhao, Min Zhang*<br>[[Paper](https://doi.org/10.1145/3680528.3687688)] [[GitHub](https://github.com/HITsz-TMG/Anim-Director/tree/main/Anim-Director)] |
| <img src="https://raw.githubusercontent.com/HITsz-TMG/Anim-Director/main/AniMaker/assets/pipeline.png" width="420" alt="AniMaker pipeline"/> | **[SIGGRAPH Asia 2025] AniMaker: Multi-Agent Animated Storytelling with MCTS-Driven Clip Generation**<br>*Haoyuan Shi, Yunxin Li, Xinyu Chen, Longyue Wang, Baotian Hu, Min Zhang*<br>[[Paper](https://doi.org/10.1145/3757377.3764009)] [[GitHub](https://github.com/HITsz-TMG/Anim-Director/tree/main/AniMaker)] |


<p align="center">
  <sub>Built with 🦞 by the Lychee Agent team</sub>
</p>
