# -*- coding: utf-8 -*-
"""
AI导演工作室 - API Server
六阶段工作流: 剧本→角色设计→分镜→参考图→视频→后期
"""
import os
import sys
import json
import asyncio
import time
import uvicorn
import queue
import threading
import logging
from logging.handlers import QueueHandler, QueueListener

# ========== 并发日志配置 ==========
def setup_concurrent_logging():
    """配置并发安全的日志系统"""
    # 创建日志队列
    log_queue = queue.Queue(-1)

    # 控制台处理器（主线程输出）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] [%(threadName)-12s] %(levelname)-8s %(message)s',
        datefmt='%H:%M:%S'
    ))

    # 创建 QueueListener（主线程运行，安全输出）
    listener = QueueListener(log_queue, console_handler, respect_handler_level=True)
    listener.start()

    # 为所有现有 logger 添加 QueueHandler
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # 给 root logger 也添加 QueueHandler
    queue_handler = QueueHandler(log_queue)
    root_logger.addHandler(queue_handler)

    # 让所有模块的 logger 都使用 QueueHandler
    for name in logging.Logger.manager.loggerDict:
        logger = logging.getLogger(name)
        # 清除原有 handlers，添加 QueueHandler
        logger.handlers.clear()
        logger.addHandler(queue_handler)

    return listener

# 启动并发日志监听器
_log_listener = setup_concurrent_logging()
# =================================
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Optional, Dict, List

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings
from core.orchestrator import WorkflowEngine, WorkflowStage

app = FastAPI(title="AI导演工作室", version="2.0.0")
workflow_engine = WorkflowEngine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.CODE_DIR, exist_ok=True)
app.mount("/code", StaticFiles(directory=settings.CODE_DIR), name="code")


# ============================== 请求模型 ==============================

class ProjectStartRequest(BaseModel):
    idea: str
    style: Optional[str] = "anime"
    video_ratio: Optional[str] = "16:9"
    expand_idea: Optional[bool] = True  # 默认启用创意扩写
    llm_model: Optional[str] = None
    vlm_model: Optional[str] = None
    image_t2i_model: Optional[str] = None
    image_it2i_model: Optional[str] = None
    video_model: Optional[str] = None
    enable_concurrency: Optional[bool] = True
    web_search: Optional[bool] = False

class InterventionRequest(BaseModel):
    stage: str
    modifications: Dict[str, Any] = {}


# ============================== API ==============================

@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    return {"status": "ok", "timestamp": time.time()}


@app.post("/api/project/start")
async def start_project(req: ProjectStartRequest):
    session_id = str(int(time.time() * 1000))
    state = workflow_engine.get_or_create_state(session_id)
    state.started_at = __import__('datetime').datetime.now()
    state.status = "stage_completed"

    # 保存会话元数据（未传参数时使用 config.py 中的默认值）
    meta = {
        "idea": req.idea,
        "style": req.style or "anime",
        "video_ratio": req.video_ratio or "16:9",
        "expand_idea": req.expand_idea if req.expand_idea is not None else True,
        "llm_model": req.llm_model or settings.LLM_MODEL,
        "vlm_model": req.vlm_model or settings.VLM_MODEL,
        "image_t2i_model": req.image_t2i_model or settings.IMAGE_T2I_MODEL,
        "image_it2i_model": req.image_it2i_model or settings.IMAGE_IT2I_MODEL,
        "video_model": req.video_model or settings.VIDEO_MODEL,
        "enable_concurrency": req.enable_concurrency if req.enable_concurrency is not None else True,
        "web_search": req.web_search if req.web_search is not None else False,
    }
    state.meta = meta
    workflow_engine.save_session_to_disk(session_id, meta)

    return {
        "session_id": session_id,
        "status": state.status,
        "params": {
            "idea": req.idea,
            "style": req.style,
            "llm_model": req.llm_model,
            "vlm_model": req.vlm_model,
        }
    }


def _inject_user_selections(state, stage: str, data: dict):
    """从已持久化的 artifacts 中读取用户选项，注入到 input_data。

    video_generation 需要:
    - selected_images: 用户选择的参考图版本（来自 reference_generation）
    - clips: 包含用户修改的 description（来自 video_generation）

    post_production 需要:
    - selected_clips: 用户选择的视频版本（来自 video_generation）
    """
    # 注入用户选择的参考图
    if stage == 'video_generation' and 'selected_images' not in data:
        ref_art = state.artifacts.get('reference_generation', {})
        if isinstance(ref_art, dict):
            scenes = ref_art.get('scenes', [])
            selected_images = {s['id']: s['selected'] for s in scenes
                              if isinstance(s, dict) and s.get('id') and s.get('selected')}
            if selected_images:
                data['selected_images'] = selected_images

    # 注入已有的 clips（包含用户修改的 description 和 duration）
    if stage == 'video_generation' and 'clips' not in data:
        vid_art = state.artifacts.get('video_generation', {})
        if isinstance(vid_art, dict):
            clips = vid_art.get('clips', [])
            if clips:
                data['clips'] = clips

    # 注入用户选择的视频
    if stage == 'post_production' and 'selected_clips' not in data:
        vid_art = state.artifacts.get('video_generation', {})
        if isinstance(vid_art, dict):
            clips = vid_art.get('clips', [])
            selected_clips = {c['id']: c['selected'] for c in clips
                             if isinstance(c, dict) and c.get('id') and c.get('selected')}
            if selected_clips:
                data['selected_clips'] = selected_clips


@app.post("/api/project/{session_id}/execute/{stage}")
async def execute_stage(session_id: str, stage: str, request: Request):
    state = workflow_engine.get_or_create_state(session_id)

    try:
        body = await request.json()
    except Exception:
        body = {}

    # 确保 body 中有 session_id（agent 需要）
    body["session_id"] = session_id

    # 注入会话级元数据（模型配置等），确保模型参数始终可用
    if state.meta:
        for k, v in state.meta.items():
            if v is not None and k not in body:  # 区分 None 和 False
                body[k] = v

    # 从已持久化的 artifacts 中注入用户选项（selected_images / selected_clips）
    _inject_user_selections(state, stage, body)

    workflow_engine.reset_stop_event(session_id)
    session_stop = workflow_engine.get_stop_event(session_id)
    stop_event = threading.Event()
    cancellation_check = lambda: stop_event.is_set() or session_stop.is_set()

    progress_events = queue.Queue()

    def progress_callback(phase, step, percent, data=None):
        event = {"phase": phase, "step": step, "percent": percent}
        if data:
            event["data"] = data
        progress_events.put(event)

    async def stream_execution():
        stage_enum = WorkflowStage(stage)

        try:
            task = asyncio.create_task(
                workflow_engine.execute_stage(
                    state, stage_enum, body,
                    cancellation_check=cancellation_check,
                    progress_callback=progress_callback
                )
            )

            while not task.done():
                while not progress_events.empty():
                    try:
                        p = progress_events.get_nowait()
                        evt = {
                            "type": "progress",
                            "message": f"{p['phase']}: {p['step']}",
                            "phase": p["phase"],
                            "step_desc": p["step"],
                            "percent": p["percent"],
                        }
                        if p.get("data"):
                            evt["data"] = p["data"]
                        yield json.dumps(evt) + "\n"
                        await asyncio.sleep(0)  # 强制立即发送 SSE 事件
                    except queue.Empty:
                        break

                if await request.is_disconnected():
                    stop_event.set()
                    yield json.dumps({"type": "error", "content": "Client disconnected"}) + "\n"
                    return

                yield json.dumps({"type": "heartbeat", "time": time.time()}) + "\n"
                await asyncio.sleep(0.1)  # 减少心跳间隔，加快事件处理

            # Drain any remaining progress events after task completion
            while not progress_events.empty():
                try:
                    p = progress_events.get_nowait()
                    evt = {
                        "type": "progress",
                        "message": f"{p['phase']}: {p['step']}",
                        "phase": p["phase"],
                        "step_desc": p["step"],
                        "percent": p["percent"],
                    }
                    if p.get("data"):
                        evt["data"] = p["data"]
                    yield json.dumps(evt) + "\n"
                    await asyncio.sleep(0)  # 强制立即发送 SSE 事件
                except queue.Empty:
                    break

            result = task.result()

            # 保存会话到磁盘
            workflow_engine.save_session_to_disk(session_id)

            requires_intervention = result.get("requires_intervention", False)
            # 生成 OpenCLAW 提示文本
            # 优先使用 agent 返回的 openclaw_hint
            openclaw_msg = result.get("openclaw_hint", "")
            if not openclaw_msg and requires_intervention:
                stage_name_map = {
                    "script_generation": "剧本生成",
                    "character_design": "角色/场景设计",
                    "storyboard": "分镜设计",
                    "reference_generation": "参考图生成",
                    "video_generation": "视频生成",
                    "post_production": "后期剪辑",
                }
                stage_name = stage_name_map.get(stage, stage)
                openclaw_msg = f"{stage_name}完成，需要用户确认。请展示给用户并等待用户确认后才能调用 /continue。"

            yield json.dumps({
                "type": "stage_complete",
                "stage": stage,
                "status": state.status,
                "requires_intervention": requires_intervention,
                # OpenCLAW 提示
                "openclaw": openclaw_msg,
                "payload_summary": result.get("payload"),
            }) + "\n"

        except Exception as e:
            # 即使出错也保存会话，保留已生成的部分结果
            try:
                workflow_engine.save_session_to_disk(session_id)
            except Exception:
                pass
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"

    return StreamingResponse(
        stream_execution(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.get("/api/project/{session_id}/status")
async def get_project_status(session_id: str):
    state = workflow_engine.get_state(session_id)
    if not state:
        raise HTTPException(404, "Session not found")
    return state.to_dict()


@app.get("/api/project/{session_id}/status/from_disk")
async def get_project_status_from_disk(session_id: str):
    """从 sessions json 文件读取状态，供前端轮询使用（即使后端重启也能获取状态）"""
    import os
    # backend/api_server.py -> backend/code/data/sessions
    session_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'code', 'data', 'sessions'
    )
    session_file = os.path.join(session_dir, f"{session_id}.json")
    if not os.path.exists(session_file):
        raise HTTPException(404, "Session not found")
    with open(session_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


@app.get("/api/project/{session_id}/artifact/{stage}")
async def get_artifact(session_id: str, stage: str):
    state = workflow_engine.get_state(session_id)
    if not state:
        raise HTTPException(404, "Session not found")
    artifact = state.artifacts.get(stage)

    if artifact is None:
        raise HTTPException(404, f"Artifact for stage '{stage}' not found")
    return {"stage": stage, "artifact": artifact}


@app.patch("/api/project/{session_id}/models")
async def update_models(session_id: str, request: Request):
    """更新会话的模型配置"""
    state = workflow_engine.get_state(session_id)
    if not state:
        raise HTTPException(404, "Session not found")
    body = await request.json()
    allowed_keys = ("llm_model", "vlm_model", "image_t2i_model", "image_it2i_model", "video_model", "video_ratio", "enable_concurrency")
    if not state.meta:
        state.meta = {}
    for k in allowed_keys:
        if k in body:
            state.meta[k] = body[k]
    workflow_engine.save_session_to_disk(session_id)
    return {"status": "ok"}


@app.patch("/api/project/{session_id}/artifact/{stage}")
async def update_artifact(session_id: str, stage: str, request: Request):
    """保存用户在某阶段的选择（如选定的图片/视频版本）

    数据存储策略：
    - 用户修改只保存到 sessions json（state.artifacts）
    - result/script json 只作为 LLM 初始生成，不接受用户修改
    """
    state = workflow_engine.get_state(session_id)
    if not state:
        raise HTTPException(404, "Session not found")
    body = await request.json()

    # 第三阶段分镜修改：同步更新 video_generation 的 clips duration
    if stage == "storyboard" and "shots" in body:
        shot_durations = {s['shot_id']: s.get('duration', 10) for s in body['shots'] if 'shot_id' in s}
        video_art = state.artifacts.get('video_generation', {})
        if isinstance(video_art, dict) and 'clips' in video_art:
            for clip in video_art['clips']:
                shot_id = clip.get('id')
                if shot_id in shot_durations:
                    clip['duration'] = shot_durations[shot_id]
                    logger.info(f"Synced duration {shot_durations[shot_id]}s to video_generation clip {shot_id}")
        # 移除 shots，避免合并到 storyboard artifact
        body = {k: v for k, v in body.items() if k != "shots"}

    # 第三阶段确认新分镜：清除 is_new 标记
    if stage == "storyboard" and "shots" in body:
        updated_shots = body.get('shots', [])
        # 清除所有 is_new 标记
        for shot in updated_shots:
            if 'is_new' in shot:
                shot['is_new'] = False
        logger.info(f"Confirmed new shots, cleared is_new flag for {len(updated_shots)} shots")

    # 第三阶段清除 new_shot_ids 标记
    if stage == "storyboard" and "new_shot_ids" in body and body.get('new_shot_ids') == []:
        # 清除 new_shot_ids 标记
        logger.info("Cleared new_shot_ids marker")

    # 第五阶段视频提示词修改：更新 video_generation 的 clips
    if stage == "reference_generation" and "shots" in body:
        shot_prompts = {s['shot_id']: s.get('video_prompt', s.get('visual_prompt', ''))
                        for s in body['shots'] if 'shot_id' in s}
        shot_durations = {s['shot_id']: s.get('duration', 10) for s in body['shots'] if 'shot_id' in s}
        video_art = state.artifacts.get('video_generation', {})
        if isinstance(video_art, dict) and 'clips' in video_art:
            for clip in video_art['clips']:
                shot_id = clip.get('id')
                if shot_id in shot_prompts:
                    clip['description'] = shot_prompts[shot_id]
                if shot_id in shot_durations:
                    clip['duration'] = shot_durations[shot_id]
        # 移除 shots，避免合并到 reference_generation artifact
        body = {k: v for k, v in body.items() if k != "shots"}

    # 第四阶段选择图片版本：需要更新 scenes 数组中的 selected
    if stage == "reference_generation" and body:
        ref_art = state.artifacts.get('reference_generation', {})
        if isinstance(ref_art, dict):
            scenes = ref_art.get('scenes', [])
            # 检查 body 是否是 {sceneId: path} 格式
            is_selection_format = any(
                isinstance(k, str) and not isinstance(v, (list, dict))
                for k, v in body.items()
            )
            if is_selection_format and scenes:
                # body 是 {sceneId: path} 格式，需要更新 scenes 数组
                for scene in scenes:
                    scene_id = scene.get('id')
                    if scene_id and scene_id in body:
                        scene['selected'] = body[scene_id]
                # 清空 body，避免覆盖 scenes
                body = {}

    # 第五阶段选择视频版本：需要更新 clips 数组中的 selected
    if stage == "video_generation" and body:
        vid_art = state.artifacts.get('video_generation', {})
        if isinstance(vid_art, dict):
            clips = vid_art.get('clips', [])
            # 检查 body 是否是 {clipId: path} 格式
            is_selection_format = any(
                isinstance(k, str) and not isinstance(v, (list, dict))
                for k, v in body.items()
            )
            if is_selection_format and clips:
                # body 是 {clipId: path} 格式，需要更新 clips 数组
                for clip in clips:
                    clip_id = clip.get('id')
                    if clip_id and clip_id in body:
                        clip['selected'] = body[clip_id]
                # 清空 body，避免覆盖 clips
                body = {}

    # 更新 state.artifacts 并保存到 sessions json
    current = state.artifacts.get(stage)
    if current is None:
        state.artifacts[stage] = body
    elif isinstance(current, dict):
        current.update(body)
    else:
        state.artifacts[stage] = body

    workflow_engine.save_session_to_disk(session_id)

    return {"status": "ok"}


@app.post("/api/project/{session_id}/intervene")
async def intervene(session_id: str, req: InterventionRequest, request: Request):
    state = workflow_engine.get_state(session_id)
    if not state:
        raise HTTPException(404, "Session not found")

    workflow_engine.reset_stop_event(session_id)
    session_stop = workflow_engine.get_stop_event(session_id)
    stop_event = threading.Event()
    cancellation_check = lambda: stop_event.is_set() or session_stop.is_set()

    progress_events = queue.Queue()

    def progress_callback(phase, step, percent, data=None):
        event = {"phase": phase, "step": step, "percent": percent}
        if data:
            event["data"] = data
        progress_events.put(event)

    async def stream_intervention():
        stage_enum = WorkflowStage(req.stage)
        try:
            current_artifact = state.artifacts.get(req.stage, {})
            input_data = current_artifact if isinstance(current_artifact, dict) else {}
            # 确保 input_data 中有 session_id（agent 需要）
            input_data["session_id"] = session_id
            # 注入会话级元数据（模型配置等），确保 intervene 时也能读到正确的模型
            if state.meta:
                for k, v in state.meta.items():
                    if v is not None and k not in input_data:
                        input_data[k] = v
            # 从已持久化的 artifacts 中注入用户选项
            _inject_user_selections(state, req.stage, input_data)
            input_data.update(req.modifications)

            task = asyncio.create_task(
                workflow_engine.execute_stage(
                    state, stage_enum, input_data,
                    cancellation_check=cancellation_check,
                    progress_callback=progress_callback,
                    intervention=req.modifications,
                )
            )

            while not task.done():
                while not progress_events.empty():
                    try:
                        p = progress_events.get_nowait()
                        evt = {
                            "type": "progress",
                            "message": f"{p['phase']}: {p['step']}",
                            "phase": p["phase"],
                            "step_desc": p["step"],
                            "percent": p["percent"],
                        }
                        if p.get("data"):
                            evt["data"] = p["data"]
                        yield json.dumps(evt) + "\n"
                        await asyncio.sleep(0)  # 强制立即发送 SSE 事件
                    except queue.Empty:
                        break

                if await request.is_disconnected():
                    stop_event.set()
                    yield json.dumps({"type": "error", "content": "Client disconnected"}) + "\n"
                    return

                yield json.dumps({"type": "heartbeat", "time": time.time()}) + "\n"
                await asyncio.sleep(0.1)  # 减少心跳间隔，加快事件处理

            # Drain remaining
            while not progress_events.empty():
                try:
                    p = progress_events.get_nowait()
                    evt = {
                        "type": "progress",
                        "message": f"{p['phase']}: {p['step']}",
                        "phase": p["phase"],
                        "step_desc": p["step"],
                        "percent": p["percent"],
                    }
                    if p.get("data"):
                        evt["data"] = p["data"]
                    yield json.dumps(evt) + "\n"
                except queue.Empty:
                    break

            result = task.result()
            workflow_engine.save_session_to_disk(session_id)

            requires_intervention = result.get("requires_intervention", False)
            # 生成 OpenCLAW 提示文本
            # 优先使用 agent 返回的 openclaw_hint
            openclaw_msg = result.get("openclaw_hint", "")
            if not openclaw_msg and requires_intervention:
                stage_name_map = {
                    "script_generation": "剧本生成",
                    "character_design": "角色/场景设计",
                    "storyboard": "分镜设计",
                    "reference_generation": "参考图生成",
                    "video_generation": "视频生成",
                    "post_production": "后期剪辑",
                }
                stage_name = stage_name_map.get(req.stage, req.stage)
                openclaw_msg = f"{stage_name}完成，需要用户确认。请展示给用户并等待用户确认后才能调用 /continue。"

            yield json.dumps({
                "type": "stage_complete",
                "stage": req.stage,
                "status": state.status,
                "requires_intervention": requires_intervention,
                # OpenCLAW 提示
                "openclaw": openclaw_msg,
            }) + "\n"

        except Exception as e:
            try:
                workflow_engine.save_session_to_disk(session_id)
            except Exception:
                pass
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"

    return StreamingResponse(
        stream_intervention(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@app.post("/api/project/{session_id}/continue")
async def continue_workflow(session_id: str):
    state = workflow_engine.get_state(session_id)
    if not state:
        raise HTTPException(404, "Session not found")
    return await workflow_engine.continue_workflow(session_id)


@app.post("/api/project/{session_id}/stop")
async def stop_project(session_id: str):
    workflow_engine.stop_session(session_id)
    return {"status": "stopped", "session_id": session_id}


@app.get("/api/sessions")
async def list_sessions():
    return {"sessions": workflow_engine.list_saved_sessions()}


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str, request: Request):
    """删除历史记录（需要管理员密码）"""
    try:
        body = await request.json()
    except Exception:
        body = {}
    password = body.get("password", "")
    if not settings.ADMIN_PASSWORD or password != settings.ADMIN_PASSWORD:
        raise HTTPException(403, "密码错误")
    deleted = workflow_engine.delete_session(session_id)
    if not deleted:
        raise HTTPException(404, "Session not found")
    return {"status": "deleted", "session_id": session_id}


@app.delete("/api/sessions")
async def cleanup_orphan_files(request: Request):
    """清理孤立的结果文件（需要管理员密码）"""
    try:
        body = await request.json()
    except Exception:
        body = {}
    password = body.get("password", "")
    if not settings.ADMIN_PASSWORD or password != settings.ADMIN_PASSWORD:
        raise HTTPException(403, "密码错误")

    # 获取所有 session ID
    session_ids = set()
    for f in os.listdir(workflow_engine._session_dir):
        if f.endswith('.json'):
            session_ids.add(f.replace('.json', ''))

    # 清理孤立文件
    cleaned = {"scripts": [], "images": [], "videos": []}
    result_base = settings.RESULT_DIR

    # 清理孤立剧本
    script_dir = os.path.join(result_base, 'script')
    for f in os.listdir(script_dir):
        if f.startswith('script_') and f.endswith('.json'):
            sid = f.replace('script_', '').replace('.json', '')
            if sid not in session_ids:
                os.remove(os.path.join(script_dir, f))
                cleaned["scripts"].append(sid)

    # 清理孤立图片
    image_dir = os.path.join(result_base, 'image')
    for d in os.listdir(image_dir):
        if d != 'test_avail' and d not in session_ids:
            import shutil
            shutil.rmtree(os.path.join(image_dir, d))
            cleaned["images"].append(d)

    # 清理孤立视频
    video_dir = os.path.join(result_base, 'video')
    for d in os.listdir(video_dir):
        if d != 'test_avail' and d not in session_ids:
            import shutil
            shutil.rmtree(os.path.join(video_dir, d))
            cleaned["videos"].append(d)

    return {"status": "cleaned", "cleaned": cleaned}


@app.get("/api/project/{session_id}/scene/{scene_number}/assets")
async def check_scene_assets(session_id: str, scene_number: int):
    """检查某场景是否有生成的参考图或视频"""
    import os
    from config import settings

    result_file = os.path.join(settings.RESULT_DIR, 'script', f'script_{session_id}.json')
    if not os.path.exists(result_file):
        return {"scene_number": scene_number, "reference_images": 0, "videos": 0}

    with open(result_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    storyboard = results.get(session_id, {}).get('storyboard', {})
    shots = storyboard.get('shots', [])

    # 筛选该场景的分镜
    scene_shots = [s for s in shots if s.get('scene_number') == scene_number]
    shot_ids = [s.get('shot_id') for s in scene_shots if s.get('shot_id')]

    # 检查参考图
    ref_artifact = results.get(session_id, {}).get('reference_generation', {})
    ref_scenes = ref_artifact.get('scenes', [])
    ref_image_count = 0
    for sc in ref_scenes:
        if sc.get('id') in shot_ids:
            selected = sc.get('selected')
            if selected and os.path.exists(os.path.join(settings.CODE_DIR, selected.lstrip('/'))):
                ref_image_count += 1
            versions = sc.get('versions', [])
            for v in versions:
                if v and os.path.exists(os.path.join(settings.CODE_DIR, v.lstrip('/'))):
                    ref_image_count += 1

    # 检查视频
    video_artifact = results.get(session_id, {}).get('video_generation', {})
    video_clips = video_artifact.get('clips', [])
    video_count = 0
    for vc in video_clips:
        if vc.get('id') in shot_ids:
            selected = vc.get('selected')
            if selected and os.path.exists(os.path.join(settings.CODE_DIR, selected.lstrip('/'))):
                video_count += 1

    return {
        "scene_number": scene_number,
        "reference_images": ref_image_count,
        "videos": video_count,
        "shot_count": len(scene_shots),
    }


@app.get("/api/stages")
async def list_stages():
    return {
        "stages": [
            {"id": "script_generation", "name": "剧本生成", "order": 1, "description": "将灵感���化为结构化剧本"},
            {"id": "character_design", "name": "角色/场景设计", "order": 2, "description": "生成角色设计图和场景背景"},
            {"id": "storyboard", "name": "分镜设计", "order": 3, "description": "设计镜头语言和分镜脚本"},
            {"id": "reference_generation", "name": "参考图生成", "order": 4, "description": "生成高精度参考图"},
            {"id": "video_generation", "name": "视频生成", "order": 5, "description": "将参考图/分镜图生成视频"},
            {"id": "post_production", "name": "后期剪辑", "order": 6, "description": "拼接视频片段为最终成片"},
        ]
    }


# ============================== 临时工作台 API ==============================

import json
import uuid
from datetime import datetime

# 临时工作台数据目录
SANDBOX_DIR = os.path.join(settings.CODE_DIR, "result", "sandbox")
SANDBOX_HISTORY_FILE = os.path.join(SANDBOX_DIR, "history.json")

# 确保目录存在
os.makedirs(SANDBOX_DIR, exist_ok=True)


def _load_history() -> List[dict]:
    """加载历史记录"""
    if os.path.exists(SANDBOX_HISTORY_FILE):
        try:
            with open(SANDBOX_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def _save_history(history: List[dict]):
    """保存历史记录"""
    with open(SANDBOX_HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def _normalize_path(path: str) -> str:
    """将绝对路径转换为相对路径格式 result/..."""
    if not path:
        return path
    # 如果已经是相对路径，直接返回
    if not path.startswith('/'):
        # 确保以 result/ 开头
        if not path.startswith('result/'):
            return f"result/{path}"
        return path
    # 绝对路径，提取相对于 CODE_DIR 的部分
    code_dir = settings.CODE_DIR
    if path.startswith(code_dir):
        relative = path[len(code_dir):].lstrip('/')
        # 直接返回 result/... 格式，因为 /code/ 会映射到 CODE_DIR
        return relative
    # 其他绝对路径，尝试提取文件名
    return path.split('/')[-1]


def _convert_output_paths(output_data: dict) -> dict:
    """转换 output 中的路径为相对路径格式"""
    if not output_data:
        return output_data
    converted = output_data.copy()
    # 转换 images
    if 'images' in converted and isinstance(converted['images'], list):
        converted['images'] = [_normalize_path(img) for img in converted['images']]
    # 转换 video_path
    if 'video_path' in converted and converted['video_path']:
        converted['video_path'] = _normalize_path(converted['video_path'])
    # 转换 input 中的 reference_image
    if 'reference_image' in converted.get('input', {}):
        input_copy = converted['input'].copy()
        input_copy['reference_image'] = _normalize_path(input_copy['reference_image'])
        converted['input'] = input_copy
    return converted


def _add_record(tool: str, model: str, input_data: dict, output_data: dict, files: List[str] = None) -> str:
    """添加历史记录"""
    record_id = str(uuid.uuid4().hex[:8])
    # 转换路径为相对路径格式
    output_data = _convert_output_paths(output_data)
    record = {
        "id": record_id,
        "tool": tool,
        "model": model,
        "input": input_data,
        "output": output_data,
        "files": files or [],
        "created_at": datetime.now().isoformat(),
    }
    history = _load_history()
    history.insert(0, record)  # 最新记录放在最前面
    _save_history(history)
    return record_id


def _delete_record_files(files: List[str]):
    """删除记录关联的文件"""
    for f in files:
        if f and os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass


# 请求模型
class SandboxLLMRequest(BaseModel):
    model: str
    prompt: str
    temperature: Optional[float] = 0.7
    web_search: Optional[bool] = False


class SandboxVLMRequest(BaseModel):
    model: str
    prompt: str
    images: List[str]  # 图片URL或base64


class SandboxT2IRequest(BaseModel):
    model: str
    prompt: str
    style: Optional[str] = "anime"
    ratio: Optional[str] = "16:9"


class SandboxI2IRequest(BaseModel):
    model: str
    prompt: str
    image: str  # 参考图片URL或base64


class SandboxVideoRequest(BaseModel):
    model: str
    prompt: str
    image: Optional[str] = None  # 参考图片


@app.get("/api/sandbox/history")
async def sandbox_get_history():
    """获取历史记录列表"""
    history = _load_history()
    # 返回完整信息（包括 output）
    return {
        "success": True,
        "records": [
            {
                "id": r["id"],
                "tool": r["tool"],
                "model": r["model"],
                "input": r["input"],
                "output": r.get("output"),
                "created_at": r["created_at"],
            }
            for r in history
        ]
    }


@app.get("/api/sandbox/history/{record_id}")
async def sandbox_get_record(record_id: str):
    """获取单条历史记录详情"""
    history = _load_history()
    for r in history:
        if r["id"] == record_id:
            return {"success": True, "record": r}
    return {"success": False, "error": "记录不存在"}


@app.delete("/api/sandbox/history/{record_id}")
async def sandbox_delete_record(record_id: str):
    """删除历史记录"""
    history = _load_history()
    record_to_delete = None
    new_history = []
    for r in history:
        if r["id"] == record_id:
            record_to_delete = r
        else:
            new_history.append(r)

    if record_to_delete is None:
        return {"success": False, "error": "记录不存在"}

    # 删除关联的文件
    _delete_record_files(record_to_delete.get("files", []))
    _save_history(new_history)
    return {"success": True}


@app.post("/api/sandbox/llm")
async def sandbox_llm(req: SandboxLLMRequest):
    """临时工作台 - LLM 文字生成"""
    from tool.llm_client import LLM
    client = LLM()
    try:
        result = client.query(req.prompt, model=req.model, web_search=req.web_search)
        # ��存到历史记录
        record_id = _add_record(
            tool="llm",
            model=req.model,
            input_data={"prompt": req.prompt, "web_search": req.web_search},
            output_data={"response": result}
        )
        return {"success": True, "result": result, "record_id": record_id}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/sandbox/vlm")
async def sandbox_vlm(req: SandboxVLMRequest):
    """临时工作台 - VLM 图片理解"""
    from tool.vlm_client import VLM
    client = VLM()
    try:
        result = client.query(req.prompt, image_paths=req.images, model=req.model)
        # 保存到历史记录
        record_id = _add_record(
            tool="vlm",
            model=req.model,
            input_data={"prompt": req.prompt, "images": req.images},
            output_data={"response": result}
        )
        return {"success": True, "result": result, "record_id": record_id}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/sandbox/t2i")
async def sandbox_t2i(req: SandboxT2IRequest):
    """临时工作台 - 文生图"""
    from tool.image_client import ImageClient
    import traceback
    client = ImageClient()
    try:
        print(f"[T2I] Generating image with model: {req.model}, prompt: {req.prompt[:50]}...")
        result = client.generate_image(req.prompt, model=req.model, image_paths=None)
        print(f"[T2I] Result: {result}")
        # result 是图片路径列表
        # 保存到历史记录
        record_id = _add_record(
            tool="t2i",
            model=req.model,
            input_data={"prompt": req.prompt, "style": req.style, "ratio": req.ratio},
            output_data={"images": result},
            files=result if isinstance(result, list) else []
        )
        return {"success": True, "result": result, "record_id": record_id}
    except Exception as e:
        error_detail = traceback.format_exc()
        print(f"[T2I] Error: {error_detail}")
        return {"success": False, "error": str(e)}


@app.post("/api/sandbox/i2i")
async def sandbox_i2i(req: SandboxI2IRequest):
    """临时工作台 - 图生图"""
    from tool.image_client import ImageClient
    client = ImageClient()
    try:
        result = client.generate_image(req.prompt, image_paths=[req.image], model=req.model)
        # 保存到历史记录
        record_id = _add_record(
            tool="i2i",
            model=req.model,
            input_data={"prompt": req.prompt, "reference_image": req.image},
            output_data={"images": result},
            files=result if isinstance(result, list) else []
        )
        return {"success": True, "result": result, "record_id": record_id}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/api/sandbox/video")
async def sandbox_video(req: SandboxVideoRequest):
    """临时工作台 - 视频生成"""
    from tool.video_client import VideoClient
    client = VideoClient()
    try:
        # 生成唯一的保存路径
        save_dir = os.path.join(SANDBOX_DIR, "videos")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"{uuid.uuid4().hex[:8]}.mp4")

        result = client.generate_video(
            prompt=req.prompt,
            image_path=req.image or "",
            save_path=save_path,
            model=req.model,
            duration=5,
            shot_type="multi"
        )
        # 保存到历史记录
        record_id = _add_record(
            tool="video",
            model=req.model,
            input_data={"prompt": req.prompt, "reference_image": req.image},
            output_data={"video": result, "video_path": save_path},
            files=[save_path]
        )
        return {"success": True, "result": result, "video_path": save_path, "record_id": record_id}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    # 强制监听 0.0.0.0，允许其他电脑访问
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
