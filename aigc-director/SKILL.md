---
name: aigc-director
description: AI 视频生成全流程：通过 6 个阶段（剧本→角色/场景设计→分镜→参考图→视频生成→后期剪辑）将用户想法转化为完整视频。支持临时工作台（单独调用 LLM、VLM、文生图、图生图、视频生成）。触发词：视频生成、AI视频、AIGC、创作视频、制作视频、AI画图。
license: MIT License
metadata:
  author: Lychee
  version: "1.0"
---

# AIGC-Director Agent Skill

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
aigc-director/                    ← OpenClaw 调用的 skill 根目录
├── aigc-claw/                    ← 前后端项目代码
│   ├── backend/                  ← FastAPI 后端（端口 8000）
│   │   └── code/result/          ← 模型生成产物存放目录
│   │            ├── script/      ← 剧本产物
│   │            ├── image/       ← 图片产物（角色、场景、参考图）
│   │            └── video/       ← 视频产物
│   └── frontend/                 ← Next.js 前端（端口 3000）
├── references/                   ← OpenClaw 调用时的参考文档
│   ├── init_project/             ← 项目初始化
│   ├── run_project/              ← 服务启动
│   ├── workflow/                 ← 六阶段工作流 API
│   ├── sandbox/                  ← 临时工作台 API
│   └── send_message/             ← 消息发送
└── SKILL.md                      ← skill 正文
```

> **产物存放目录**：`aigc-claw/backend/code/result/`
> - `script/` - 剧本产物
> - `image/` - 图片产物（角色、场景、参考图）
> - `video/` - 视频产物

---

## 阶段与停点（共9个）

| 停点 | 阶段 | phase 值 | 描述 | 操作 |
|------|------|----------|------|------|
| 1 | 项目配置 | - | 确认配置选项 | 展示配置 → 用户确认 |
| 2 | 剧本生成 | suggest_expand | 建议扩写 | 等待用户确认 |
| 3 | 剧本生成 | logline_selection | 选择情节 | 从3个候选中选择 |
| 4 | 剧本生成 | mode_selection | 选择模式 | 电影(4幕) / 微电影(1幕) |
| 5 | 剧本生成 | script_generation | 确认剧本 | 确认后继续 |
| 6 | 角色/场景设计 | - | 确认角色/场景图片 | 确认后继续 |
| 7 | 分镜设计 | - | 确认分镜列表 | 确认后继续 |
| 8 | 参考图生成 | - | 确认参考图 | 确认后继续 |
| 9 | 视频生成 | - | 确认视频片段 | 确认后继续 |

> **注意**：`suggest_expand` 和 `logline_selection` 可能根据输入质量被跳过。

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
| "生成视频" | 必须先询问：长视频(工作流) 还是 短视频(工作台)？ |
| "分析图片" | 临时工作台 (sandbox) |
| "问 LLM 问题" | 临时工作台 (sandbox) |
| "照片转动漫" | 临时工作台 (sandbox) |

### 3. 执行流程

```
1. 检查后端运行状态 → 未运行则参考 start_backend.md 启动 → 等待3秒 → 再次检查
2. 检查前端运行状态 → 未运行则参考 start_frontend.md 启动 → 等待5秒 → 再次检查
3. 检查 API Key 配置 → 读取 .env 文件，确认所需 API Key 已配置
4. 参考 create_project.md 询问用户项目配置 → 停点1（配置确认）→ 创建项目
5. 参考 create_script.md 执行剧本生成 → 停点2-5
6. 参考 create_character.md 执行角色设计 → 停点6
7. 参考 create_storyboard.md 执行分镜设计 → 停点7
8. 参考 create_reference.md 执行参考图生成 → 停点8
9. 参考 create_video.md 执行视频生成 → 停点9
10. 参考 create_post.md 执行后期剪辑
11. 完成 → 发送最终视频给用户
```

> **注意**：一定要参考 `references/` 目录下的具体文档执行每一步操作，不要凭记忆或想当然去调用 API！

#### 检查 API Key 配置

在创建项目前，必须检查用户选择的模型对应的 API Key 是否已配置：

```bash
# 读取 .env 文件检查配置
cat aigc-claw/backend/.env | grep -E "API_KEY|KEY"

# 必需的配置（根据选择的模型）
# LLM: DASHSCOPE_API_KEY / DEEPSEEK_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY
# 图片: ARK_API_KEY / DASHSCOPE_API_KEY
# 视频: DASHSCOPE_API_KEY / VOLC_ACCESS_KEY / KLING_ACCESS_KEY
```

如果 API Key 未配置，需要提醒用户：
1. 告知缺少哪个平台的 API Key
2. 提供获取方式
3. 配置位置（`aigc-claw/backend/.env` 文件）
4. 等待用户配置完成后才能继续

| 平台 | API Key 变量 | 获取链接 |
|------|--------------|----------|
| DeepSeek | `DEEPSEEK_API_KEY` | https://platform.deepseek.com/api_keys |
| 阿里云 DashScope | `DASHSCOPE_API_KEY` | https://bailian.console.aliyun.com/cn-beijing/?tab=home#/home |
| 字节火山方舟 | `ARK_API_KEY` 或 `VOLC_ACCESS_KEY`/`VOLC_SECRET_KEY` | https://www.volcengine.com/product/ark |
| 快手可灵 Kling | `KLING_ACCESS_KEY`/`KLING_SECRET_KEY` | https://klingai.com/cn/dev |

---

## 🚨 停点处理（强制规则）

**当查询状态为 `stage_completed` 或 `waiting_in_stage` 时，必须按以下步骤执行：**

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
收到 suggest_expand 停点 → 直接调用 intervene → 跳过用户确认
```

### ✅ 正确示例
```
1. 阶段内部停点触发（如 suggest_expand）
收到 suggest_expand 停点 
→ 获取 artifact 查看内容
→ 展示给用户："系统建议启用创意扩写模式..."
→ 询问："是否同意？"
→ 用户回复"同意" → 调用 intervene

2. 阶段完成停点触发
收到 stage_completed 停点
→ 获取 artifact 查看产物内容
→ 展示给用户："第一阶段已完成，生成了剧本内容..."
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
| idle | 新建会话 | 启动项目 |
| running | 执行中 | 轮询等待 |
| waiting_in_stage | 等待用户介入 | 调用 `intervene` |
| stage_completed | 阶段完成 | 调用 `continue` |
| session_completed | 全部完成 | 结束 |

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
| **send_message/** | 消息发送 | |
| [feishu.md](references/send_message/feishu.md) | 飞书发送媒体文件 | 用户通过飞书渠道发起对话，并且需要向用户发送图片/视频给用户时 |
| [wechat.md](references/send_message/wechat.md) | 微信发送媒体文件 | 用户通过微信渠道发起对话，并且需要向用户发送图片/视频给用户时 |
