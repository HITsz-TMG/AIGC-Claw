---
name: video-claw
description: AI 视频生成全流程：通过 6 个阶段（剧本→角色/场景设计→分镜→参考图→视频生成→后期剪辑）将用户想法转化为完整视频。支持临时工作台（单独调用 LLM、VLM、文生图、图生图、视频生成）和一次性短流程 Pipeline（文艺短视频、动作迁移、数字人口播）。触发词：视频生成、AI视频、AIGC、创作视频、制作视频、AI画图、文艺短视频、静态短视频、动作迁移、数字人口播。
license: MIT License
metadata:
  author: Lychee
  version: "1.0"
---

# Video-Claw Agent Skill

> **本地运行**：这是一个**本地部署**的视频生成项目，**前后端都运行在本机**：
> - 后端：`http://localhost:8000`
> - 前端：`http://localhost:3000`
> - 所有 API 调用都请求本地服务器，不要请求其他地址！
> - 确保在调用任何 API 之前，后端和前端服务都已经启动并运行正常！

> **核心理念**：Agent 应该像"持续陪伴的智能视频制作助理"，每完成一个用户可感知的重要任务，都应立即给用户一条简报，并等待用户确认。

> **核心原则**：每个阶段的产物都必须展示给用户，必须停下来等待用户确认后才能继续下一阶段。

> **防止遗忘**：在整个流程中，Agent 可能会忘记之前的用户输入或之前阶段的产物内容。**每当进入一个新的阶段时，Agent 都必须重新加载这篇SKILL文档，确保不会忘记任何细节**。

---

## 项目结构

```
video-claw/                    ← OpenClaw 调用的 skill 根目录
├── video-claw/                    ← 前后端项目代码
│   ├── backend/                  ← FastAPI 后端（端口 8000）
│   │   ├── api/                  ← API 路由、Schema 和服务
│   │   ├── models/               ← 模型注册、能力标签和模型调用客户端
│   │   ├── pipelines/            ← 一次性短流程 Pipeline
│   │   └── code/                 ← 数据与生成产物
│   │       ├── data/tasks/       ← Pipeline 任务元数据：<task_id>.json
│   │       └── result/
│   │           ├── image/        ← 主流程图片产物
│   │           ├── video/        ← 主流程视频产物
│   │           └── task/         ← Pipeline 产物：<task_id>/
│   └── frontend/                 ← Next.js 前端（端口 3000）
├── references/                   ← OpenClaw 调用时的参考文档
│   ├── init_project/             ← 项目初始化
│   ├── run_project/              ← 服务启动
│   ├── workflow/                 ← 六阶段工作流 API
│   ├── sandbox/                  ← 临时工作台 API
│   ├── pipelines/                ← 一次性短流程 Pipeline API
│   └── send_message/             ← 消息发送
└── SKILL.md                      ← skill 正文
```

> **产物存放目录**：`video-claw/backend/code/result/`
> - `script/` - 剧本产物
> - `image/` - 图片产物（角色、场景、参考图）
> - `video/` - 视频产物
> - `task/<task_id>/` - Pipeline 产物（文艺短视频、动作迁移、数字人口播）
>
> **Pipeline 元数据目录**：`video-claw/backend/code/data/tasks/<task_id>.json`

---

## 阶段与停点（含停点0，共7个停点）

| 停点 | 阶段 | phase 值 | 描述 | 操作 |
|------|------|----------|------|------|
| 0 | 剧情及视觉确认 | - | 确认项目创意、集数、文档以及风格比例 | 展示初版规划 → 用户确认 |
| 1 | AI模型参数配置 | - | 确认项目将调用的各种底层AI模型类型及其他控制参数 | 展示配置 → 用户确认 |
| 2 | 剧本生成 | script_generation | 确认全集剧本 | 展示每集剧情概要，发送阶段url → 用户确认 |
| 3 | 角色/场景设计 | - | 确认角色/场景图片 | 展示所有人物/场景图片，发送阶段url → 用户确认 |
| 4 | 分镜设计 | - | 确认分镜列表 | 发送分镜个数、每集时长、总时长信息 → 用户确认 |
| 5 | 参考图生成 | - | 确认参考图 | 发送阶段url → 用户确认 |
| 6 | 视频生成 | - | 确认视频片段 | 发送阶段url → 用户确认 |
| - | 后期剪辑 | post_production | 拼接视频并生成最终成片 | 无需确认，完成后发送阶段url和分集视频 |

> **注意**：原有的部分复杂剧本流程（扩写、模式选择等）由于系统优化已简化，目前直接输出最终的剧本列表，以分集（`episode_number`）为单位。

---

## 工作流程

### 1. 本地部署(仅初始化时执行)

当用户要求"初始化项目"、"配置项目"、"部署项目"时，需要先进行项目初始化：参考 [init_all.md](references/init_project/init_all.md) 执行完整初始化流程。

> **注意**：仅在用户首次下载项目或需要重新配置环境时使用。项目已初始化过则跳过此步骤，直接检查服务运行状态。

### 2. 检查本地服务

参考 [start_backend.md](references/run_project/start_backend.md) 和 [start_frontend.md](references/run_project/start_frontend.md) 检查服务是否运行。

> **⚠️ 强制要求**：如果服务未运行，必须先启动服务再继续！

### 2. 路由判断

| 用户说 | 处理 |
|--------|------|
| "生成图片" | 临时工作台 (sandbox) |
| "生成视频" | 必须先询问：长视频(六阶段工作流)、文艺短视频、动作迁移、数字人口播，还是临时工作台视频？ |
| "文艺短视频" / "静态短视频" / "图文短视频" / "旁白配图视频" | Pipeline：文艺短视频，参考 `references/pipelines/static_short_video.md` |
| "动作迁移" / "把动作迁到人物上" | Pipeline：动作迁移，参考 `references/pipelines/action_transfer.md` |
| "数字人口播" / "口播视频" / "商品口播" | Pipeline：数字人口播，参考 `references/pipelines/digital_human.md` |
| "分析图片" | 临时工作台 (sandbox) |
| "问 LLM 问题" | 临时工作台 (sandbox) |
| "照片转动漫" | 临时工作台 (sandbox) |

### 3. 执行流程

```
1. 检查后端运行状态 → 未运行则参考 start_backend.md 启动 → 等待3秒 → 再次检查
2. 检查前端运行状态 → 未运行则参考 start_frontend.md 启动 → 等待5秒 → 再次检查
3. 检查 API Key 配置 → 读取 `video-claw/backend/config.yaml`，确认所需 API Key 已配置
4. 参考 create_project.md，询问用户剧情与集数相关配置（停点0），确认无误后接着确认生成参数选项（停点1）。全部确认完毕后 → 创建项目
5. 参考 create_script.md 执行剧本生成 → 停点2
6. 参考 create_character.md 执行角色设计 → 停点3
7. 参考 create_storyboard.md 执行分镜设计 → 停点4
8. 参考 create_reference.md 执行参考图生成 → 停点5
9. 参考 create_video.md 执行视频生成 → 停点6
10. 参考 create_post.md 执行后期剪辑
11. 完成 → 发送最终视频给用户（若用户在看完成片后希望继续推进故事，参考 smart_continue.md 开始智能续写，然后继续执行新生成片段的后续流程）
```

> **注意**：一定要参考 `references/` 目录下的具体文档执行每一步操作，不要凭记忆或想当然去调用 API！

### 4. 执行一次性 Pipeline

当用户明确选择文艺短视频、动作迁移或数字人口播时，不走六阶段停点流程，而是创建 Pipeline 任务：

```
1. 检查后端运行状态
2. 检查前端运行状态
3. 检查 API Key 配置
4. 根据用户目标选择 pipeline 文档
5. 必要时上传媒体文件
6. POST /api/pipelines/{pipeline}/tasks 创建任务
7. 通过 /api/tasks/{task_id}/events 订阅进度
8. 任务完成后查询 /api/tasks/{task_id}
9. 发送 final 视频和必要中间产物给用户
```

> **Pipeline 特点**：一次输入、后台执行、中间无需人工介入；任务状态只显示进度和产物，不显示日志。

#### 检查 API Key 配置

在创建项目前，必须检查用户选择的模型对应的 API Key 是否已配置：

```bash
# 读取 config.yaml 检查配置
sed -n '1,120p' video-claw/backend/config.yaml

# 必需的配置（根据选择的模型）
# LLM: models.llm.api_key 或 api_providers.deepseek/openai/gemini/dashscope.api_key
# 图片: api_providers.ark.api_key 或 api_providers.dashscope.api_key
# 视频: api_providers.dashscope.api_key / api_providers.ark.api_key / api_providers.kling.access_key + secret_key
```

如果 API Key 未配置，需要提醒用户：
1. 告知缺少哪个平台的 API Key
2. 提供获取方式
3. 配置位置（`video-claw/backend/config.yaml` 文件，或前端侧边栏底部「设置」页面）
4. 等待用户配置完成后才能继续

| 平台 | config.yaml 字段 | 获取链接 |
|------|--------------|----------|
| DeepSeek | `api_providers.deepseek.api_key` | https://platform.deepseek.com/api_keys |
| MiniMax | `api_providers.minimax.api_key` | https://platform.minimax.io |
| 阿里云 DashScope | `api_providers.dashscope.api_key` 或 `models.llm.api_key` | https://bailian.console.aliyun.com/cn-beijing/?tab=home#/home |
| 字节火山方舟 | `api_providers.ark.api_key` | https://www.volcengine.com/product/ark |
| 快手可灵 Kling | `api_providers.kling.access_key` / `api_providers.kling.secret_key` | https://klingai.com/cn/dev |

---

## 🚨 停点处理（强制规则）

**当查询状态为 `completed` 或 `waiting` 时，必须按以下步骤执行：**

### 步骤1：获取产物
```bash
curl "http://localhost:8000/api/project/{session_id}/artifact/{stage}"
```

### 步骤2：展示给用户
将 artifact 中的内容（选项列表、建议、产物摘要）**完整展示**给用户

### 步骤3：询问决策
明确告诉用户：
- 选项有哪些
- 每个选项的含义
- 需要用户选择什么

### 步骤4：等待用户回复
**禁止**在用户回复前自行调用 `intervene` 或 `continue`！

### 步骤5：用户确认后执行
根据用户的选择，调用相应的 API

---

### ❌ 错误示例（我刚才犯的错）
```
收到确认剧情停点 → 直接调用 intervene → 跳过用户确认
```

### ✅ 正确示例
```
1. 阶段中间遇到不确定内容
收到 waiting 停点
→ 获取 artifact 查看内容
→ 展示给用户选项
→ 询问："是否同意修改？"
→ 用户回复"同意" → 调用 intervene

2. 阶段完成停点触发
收到 completed 停点
→ 获取 artifact 查看产物内容
→ 展示给用户："第一阶段已完成，生成了剧本内容（x集）..."
→ 询问："是否继续下一阶段？"
→ 用户回复"继续" → 调用 continue
```

**每个停点必须**：
1. 展示产物或选项给用户
2. 询问确认
3. 用户确认后才能继续

---

## 状态判断

| status | 含义 | 操作 |
|--------|------|------|
| pending | 新建会话 | 启动项目 |
| running | 执行中 | 轮询等待 |
| waiting | 等待用户介入 | 调用 `intervene` |
| completed | 阶段完成 | 调用 `continue` |
| completed | 全部完成 | 结束 |

> **注意**：只有 status 变化时才需要干预，不要反复调用 artifact API 去"确认"！

---

## 消息发送渠道

根据向用户发送消息的渠道（飞书/微信），读取 `references/send_message/` 下的对应参考文档，获取注意事项和发送方法：
- [feishu.md](references/send_message/feishu.md) - 飞书发送消息
- [wechat.md](references/send_message/wechat.md) - 微信发送消息

---

## 任务简报格式

每个阶段完成后，发送简报必须包含：
1. 刚完成什么
2. 下一步做什么
3. 需要用户决策的内容
4. **Web 界面链接**：`http://[本地IP]:3000/?session={session_id}&stage={stage}`（注意，这里使用本地 IPv4 地址，不要用 localhost！）
5. 产物图片/视频（直接发送文件，禁止只发路径）

### Web 界面链接格式

```python
# 获取本地 IPv4 地址
import socket
local_ip = socket.gethostbyname(socket.gethostname())

# 构造前端 URL
frontend_url = f"http://{local_ip}:3000/?session={session_id}&stage={stage}"

# 发送给用户
send_to_user(f"📊 查看详情：{frontend_url}")
```

> **重要**：必须使用本地 IPv4 地址（如 `192.168.1.x`），不要使用 `localhost` 或 `127.0.0.1`，否则用户无法从其他设备访问！

---

## 详细参考

根据用户的需求和当前阶段，参考 `references/` 目录下的具体文档执行相应操作：

### references 目录

| 文件 | 用途 | 查看时机 |
|------|------|----------|
| **init_project/** | 项目初始化 | 用户首次下载或要求"初始化项目"时 |
| [init_all.md](references/init_project/init_all.md) | 完整初始化流程 | 用户要求初始化部署时 |
| [init_backend.md](references/init_project/init_backend.md) | 后端初始化 | 首次配置后端环境时 |
| [init_frontend.md](references/init_project/init_frontend.md) | 前端初始化 | 首次配置前端环境时 |
| **run_project/** | 项目启动 | |
| [start_backend.md](references/run_project/start_backend.md) | 启动后端服务 | 服务未运行时 |
| [start_frontend.md](references/run_project/start_frontend.md) | 启动前端服务 | 服务未运行时 |
| **workflow/** | 六阶段工作流 | |
| [create_project.md](references/workflow/create_project.md) | 创建新项目 API | 开始新视频项目时 |
| [create_script.md](references/workflow/create_script.md) | 剧本生成 API | 执行第一阶段时 |
| [create_character.md](references/workflow/create_character.md) | 角色/场景设计 API | 执行第二阶段时 |
| [create_storyboard.md](references/workflow/create_storyboard.md) | 分镜设计 API/剧情续写 API | 执行第三阶段时/用户提出续写剧情时 |
| [create_reference.md](references/workflow/create_reference.md) | 参考图生成 API | 执行第四阶段时 |
| [create_video.md](references/workflow/create_video.md) | 视频生成 API | 执行第五阶段时 |
| [create_post.md](references/workflow/create_post.md) | 后期剪辑 API | 执行第六阶段时 |
| [modify_character.md](references/workflow/modify_character.md) | 修改角色提示词 | 用户要求修改角色时 |
| [modify_storyboard.md](references/workflow/modify_storyboard.md) | 修改/续写分镜 | 用户要求修改/续写分镜时 |
| [modify_reference.md](references/workflow/modify_reference.md) | 修改参考图提示词 | 用户要求修改参考图时 |
| [modify_video.md](references/workflow/modify_video.md) | 修改视频提示词 | 用户要求修改视频时 |
| **sandbox/** | 临时工作台 | |
| [generate_image_t2i.md](references/sandbox/generate_image_t2i.md) | 文生图 API | 用户要求生成图片时 |
| [generate_image_it2i.md](references/sandbox/generate_image_it2i.md) | 图生图/风格转换 API | 用户要求转换图片风格时 |
| [generate_video.md](references/sandbox/generate_video.md) | 短视频生成 API | 用户要求生成15秒内视频时 |
| **pipelines/** | 一次性短流程 Pipeline | |
| [overview.md](references/pipelines/overview.md) | Pipeline 总览、任务状态、模型能力筛选 | 用户选择任一 Pipeline 时先读 |
| [static_short_video.md](references/pipelines/static_short_video.md) | 文艺短视频 Pipeline | 用户要求文艺短视频/静态短视频/旁白配图短视频时 |
| [action_transfer.md](references/pipelines/action_transfer.md) | 动作迁移 Pipeline | 用户要求动作迁移时 |
| [digital_human.md](references/pipelines/digital_human.md) | 数字人口播 Pipeline | 用户要求数字人口播/口播视频时 |
| **send_message/** | 消息发送 | |
| [feishu.md](references/send_message/feishu.md) | 飞书发送媒体文件 | 用户通过飞书渠道发起对话，并且需要向用户发送图片/视频给用户时 |
| [wechat.md](references/send_message/wechat.md) | 微信发送媒体文件 | 用户通过微信渠道发起对话，并且需要向用户发送图片/视频给用户时 |
