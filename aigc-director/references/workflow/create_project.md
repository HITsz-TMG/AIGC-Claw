# 创建项目

创建一个新的视频生成项目。

## 请求与响应

### 请求

```bash
curl -X POST "http://localhost:8000/api/project/start" \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "故事内容",
    "style": "anime",
    "video_ratio": "16:9",
    "llm_model": "qwen3.5-plus",
    "vlm_model": "qwen-vl-plus",
    "image_t2i_model": "doubao-seedream-5-0",
    "image_it2i_model": "doubao-seedream-5-0",
    "video_model": "wan2.6-i2v-flash",
    "enable_concurrency": true,
    "web_search": false
  }'
```

### 响应

```json
{
  "session_id": "xxx",
  "status": "idle",
  "current_stage": "init"
}
```

---

## 参数说明

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| idea | ✅ | 故事创意/灵感 | - |
| style | ✅ | 视频风格 | realistic |
| video_ratio | | 视频比例 | 16:9 |
| llm_model | | 剧本生成模型 | qwen3.5-plus |
| vlm_model | | VLM 评估模型 | qwen-vl-plus |
| image_t2i_model | | 文生图模型 | doubao-seedream-5-0 |
| image_it2i_model | | 图生图模型 | doubao-seedream-5-0 |
| video_model | | 视频生成模型 | wan2.6-i2v-flash |
| enable_concurrency | | 开启并发生成 | true |
| web_search | | 联网搜索 | false |

### 可用风格

`anime`, `realistic`, `comic-book`, `3d-disney`, `watercolor`, `oil-painting`, `cyberpunk`, `chinese-ink`

### 可选视频比例

6:9, 9:16, 1:1, 4:3, 3:4

### 可用模型

| 模块 | 模型 |
|------|------|
| LLM | qwen3.5-plus, deepseek-chat, gpt-4o, gemini-2.5-flash |
| VLM | qwen-vl-plus, gemini-2.5-flash-image |
| T2I | doubao-seedream-5-0, wan2.6-t2i, jimeng_t2i_v40 |
| I2I | doubao-seedream-5-0, wan2.6-image |
| Video | wan2.6-i2v-flash, kling-v3, jimeng_ti2v_v30_pro |

---

## 询问用户示例

在创建项目前，请向用户展示以下选项并让用户选择：

表格形式：
| 配置项 | 选项 | 默认值（推荐） |
|--------|------|---------------|
| **视频风格 (style)** | anime, realistic, comic-book, 3d-disney, watercolor, oil-painting, cyberpunk, chinese-ink | realistic |
| **视频比例 (video_ratio)** | 16:9（横屏）, 9:16（竖屏）, 1:1（方形）, 4:3, 3:4 | 16:9 |
| **LLM 模型** | qwen3.5-plus, deepseek-chat, gpt-4o, gemini-2.5-flash | qwen3.5-plus |
| **VLM 模型** | qwen-vl-plus, gemini-2.5-flash-image | qwen-vl-plus |
| **T2I 模型** | doubao-seedream-5-0, wan2.6-t2i, jimeng_t2i_v40 | doubao-seedream-5-0 |
| **I2I 模型** | doubao-seedream-5-0, wan2.6-image | doubao-seedream-5-0 |
| **Video 模型** | wan2.6-i2v-flash, kling-v3, jimeng_ti2v_v30_pro | wan2.6-i2v-flash |
| **联网搜索** | true, false | false |
| **并发生成** | true, false | true |

编号列表形式：
1. 故事创意 (idea): [用户的创意内容]
2. 视频风格 (style): realistic（默认值）
   - 可选：anime, realistic, comic-book, 3d-disney, watercolor, oil-painting, cyberpunk, chinese-ink
3. 视频比例 (video_ratio): 16:9（默认值）
   - 可选：16:9, 9:16, 1:1, 4:3, 3:4
4. LLM 模型: qwen3.5-plus（默认值）
   - 可选：qwen3.5-plus, deepseek-chat, gpt-4o, gemini-2.5-flash
5. VLM 模型: qwen-vl-plus（默认值）
   - 可选：qwen-vl-plus, gemini-2.5-flash-image
6. T2I 模型: doubao-seedream-5-0（默认值）
   - 可选：doubao-seedream-5-0, wan2.6-t2i, jimeng_t2i_v40
7. I2I 模型: doubao-seedream-5-0（默认值）
   - 可选：doubao-seedream-5-0, wan2.6-image
8. Video 模型: wan2.6-i2v-flash（默认值）
   - 可选：wan2.6-i2v-flash, kling-v3, jimeng_ti2v_v30_pro
9. 联网搜索: false（默认值）
   - 可选：true, false
10. 并发生成: true（默认值）
   - 可选：true, false

> **注意**：
> - **所有参数必须都展示给用户**
> - 根据用户消息渠道选择格式：
>   - 飞书：使用 Markdown 表格
>   - 微信：使用编号列表（微信不支持 Markdown 表格）

---

## 停点1：项目配置确认

在调用 API 创建项目之前，必须展示当前配置并询问用户：

### 展示当前配置

根据用户提供的idea和选择（用户未提及的选项使用默认值），生成配置确认表格：

| 配置项 | 当前值 |
|--------|--------|
| 故事创意 (idea) | [用户的创意内容] |
| 视频风格 (style) | realistic（默认值）或其他用户选择 |
| 视频比例 (video_ratio) | 16:9（默认值）或其他用户选择 |
| LLM 模型 | qwen3.5-plus（默认值）或其他用户选择 |
| VLM 模型 | qwen-vl-plus（默认值）或其他用户选择 |
| T2I 模型 | doubao-seedream-5-0（默认值）或其他用户选择 |
| I2I 模型 | doubao-seedream-5-0（默认值）或其他用户选择 |
| Video 模型 | wan2.6-i2v-flash（默认值）或其他用户选择 |
| 联网搜索 | false（默认值）|
| 并发生成 | true（默认值）|

### 询问用户

> 当前配置如上，请问是否有需要修改的？
> - 如需修改，请告知具体要修改的项目和新值
> - 如无需修改，请回复"确认"或"确定"

### 循环确认

- 如果用户提出修改 → 记录修改项 → 重新展示更新后的配置 → 再次询问确认
- 直到用户确认无需修改 → 才能调用 API 创建项目

---

## 注意事项

1. **必须询问用户**：在创建项目前，一定要询问用户项目的配置，用户没有提及的选项则使用默认值
2. **检查 API Key**：在创建项目前，必须检查用户选择的模型对应的 API Key 是否已配置

### API Key 检查步骤

```bash
# 1. 读取 .env 文件
cat aigc-claw/backend/.env

# 2. 根据用户选择的模型检查对应 API Key
#    - LLM 模型：检查 DASHSCOPE_API_KEY / DEEPSEEK_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY
#    - 图片模型：检查 ARK_API_KEY / DASHSCOPE_API_KEY / VOLC_ACCESS_KEY/VOLC_SECRET_KEY
#    - 视频模型：检查 DASHSCOPE_API_KEY / VOLC_ACCESS_KEY/VOLC_SECRET_KEY / KLING_ACCESS_KEY/KLING_SECRET_KEY

# 3. 如果缺少 API Key，提醒用户配置
```

### 缺少 API Key 时的处理

如果检测到缺少必要的 API Key，需要告知用户：
1. 缺少哪个平台的 API Key
2. 如何获取（官方链接）
3. 配置位置（`aigc-claw/backend/.env` 文件）
4. 等待用户配置完成后才能继续创建项目

| 平台 | API Key 变量 | 获取链接 |
|------|--------------|----------|
| DeepSeek | `DEEPSEEK_API_KEY` | https://platform.deepseek.com/api_keys |
| 阿里云 DashScope | `DASHSCOPE_API_KEY` | https://bailian.console.aliyun.com/cn-beijing/?tab=home#/home |
| 字节火山方舟 | `ARK_API_KEY` 或 `VOLC_ACCESS_KEY`/`VOLC_SECRET_KEY` | https://www.volcengine.com/product/ark |
| 快手可灵 Kling | `KLING_ACCESS_KEY`/`KLING_SECRET_KEY` | https://klingai.com/cn/dev |

---

## 常见问题

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `curl: (7) Failed to connect` | 后端未运行 | 启动后端服务 |
| `500 Internal Server Error` | API Key 缺失或配置错误 | 检查 `backend/.env` 文件 |
| `404 Not Found` | API 路径错误 | 确认 URL 为 `http://localhost:8000/api/project/start` |