import json
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any, Optional

# 导入模块
from config import config_manager
from ai_chat_system import ai_chat_system
from voice_api import voice_api_system
from image_api import image_api_system
from search_api import search_api_system
from database import database_manager
from obs_vts import obs_vts_system

# 创建FastAPI应用
app = FastAPI(
    title="AI Vtuber Tool API",
    description="AI主播工具的后端API服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

# 配置管理端点
@app.get("/api/config")
async def get_config():
    """获取配置"""
    return config_manager.config

@app.post("/api/config")
async def update_config(config: Dict[str, Any]):
    """更新配置"""
    try:
        config_manager.config = config
        config_manager.save_config()
        return {"message": "配置更新成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"配置更新失败: {str(e)}")

# 聊天API端点
@app.post("/api/chat")
async def chat(request: Dict[str, Any]):
    """聊天接口"""
    try:
        user_input = request.get("input", "")
        if not user_input:
            raise HTTPException(status_code=400, detail="输入不能为空")
        
        # 生成回复
        response = ai_chat_system.generate_response(user_input)
        
        # 保存到数据库
        database_manager.save_chat_message("user", user_input)
        database_manager.save_chat_message("assistant", response)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"聊天失败: {str(e)}")

# 语音API端点
@app.post("/api/tts")
async def text_to_speech(request: Dict[str, Any]):
    """文本转语音"""
    try:
        text = request.get("text", "")
        output_file = request.get("output_file", "output.wav")
        
        if not text:
            raise HTTPException(status_code=400, detail="文本不能为空")
        
        success = voice_api_system.text_to_speech(text, output_file)
        if success:
            return {"message": "TTS成功", "file": output_file}
        else:
            raise HTTPException(status_code=500, detail="TTS失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS失败: {str(e)}")

@app.post("/api/tts/realtime/start")
async def start_realtime_tts():
    """启动实时TTS流式播放"""
    try:
        # 这里可以集成实时TTS功能
        # 目前返回模拟成功
        return {"message": "实时TTS已启动", "status": "streaming"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动实时TTS失败: {str(e)}")

@app.post("/api/tts/realtime/send")
async def send_realtime_text(request: Dict[str, Any]):
    """发送实时文本进行语音播放"""
    try:
        text = request.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="文本不能为空")
        
        # 这里处理实时文本发送
        # 目前返回模拟成功
        return {"message": "文本已发送", "text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"发送实时文本失败: {str(e)}")

@app.post("/api/tts/realtime/stop")
async def stop_realtime_tts():
    """停止实时TTS流式播放"""
    try:
        # 这里处理停止实时TTS
        # 目前返回模拟成功
        return {"message": "实时TTS已停止", "status": "stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"停止实时TTS失败: {str(e)}")

@app.post("/api/asr")
async def speech_to_text(request: Dict[str, Any]):
    """语音转文本"""
    try:
        audio_file = request.get("audio_file", None)
        text = voice_api_system.speech_to_text(audio_file)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ASR失败: {str(e)}")

# 图片识别API端点
@app.post("/api/image/recognize")
async def recognize_image(request: Dict[str, Any]):
    """识别图片"""
    try:
        image_path = request.get("image_path", "")
        if not image_path:
            raise HTTPException(status_code=400, detail="图片路径不能为空")
        
        result = image_api_system.recognize_image(image_path)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图片识别失败: {str(e)}")

# 搜索API端点
@app.post("/api/search")
async def search(request: Dict[str, Any]):
    """网络搜索"""
    try:
        query = request.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="搜索查询不能为空")
        
        result = search_api_system.search(query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

# 数据库API端点
@app.get("/api/database/history")
async def get_chat_history(limit: int = 50):
    """获取聊天历史"""
    history = database_manager.get_chat_history(limit)
    return {"history": history}

@app.delete("/api/database/history")
async def clear_chat_history():
    """清空聊天历史"""
    success = database_manager.clear_chat_history()
    if success:
        return {"message": "聊天历史清空成功"}
    else:
        raise HTTPException(status_code=500, detail="聊天历史清空失败")

# OBS和VTuberStudio API端点
@app.post("/api/obs/connect")
async def connect_to_obs():
    """连接到OBS"""
    success = obs_vts_system.connect_to_obs()
    if success:
        return {"message": "连接OBS成功"}
    else:
        raise HTTPException(status_code=500, detail="连接OBS失败")

@app.post("/api/obs/disconnect")
async def disconnect_from_obs():
    """断开与OBS的连接"""
    obs_vts_system.disconnect_from_obs()
    return {"message": "断开OBS连接成功"}

@app.post("/api/obs/scene")
async def set_obs_scene(request: Dict[str, Any]):
    """设置OBS场景"""
    try:
        scene_name = request.get("scene_name", "")
        if not scene_name:
            raise HTTPException(status_code=400, detail="场景名称不能为空")
        
        success = obs_vts_system.set_obs_scene(scene_name)
        if success:
            return {"message": "设置OBS场景成功"}
        else:
            raise HTTPException(status_code=500, detail="设置OBS场景失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"设置OBS场景失败: {str(e)}")

@app.post("/api/obs/recording/start")
async def start_obs_recording():
    """开始OBS录制"""
    success = obs_vts_system.start_obs_recording()
    if success:
        return {"message": "开始OBS录制成功"}
    else:
        raise HTTPException(status_code=500, detail="开始OBS录制失败")

@app.post("/api/obs/recording/stop")
async def stop_obs_recording():
    """停止OBS录制"""
    success = obs_vts_system.stop_obs_recording()
    if success:
        return {"message": "停止OBS录制成功"}
    else:
        raise HTTPException(status_code=500, detail="停止OBS录制失败")

@app.post("/api/obs/streaming/start")
async def start_obs_streaming():
    """开始OBS推流"""
    success = obs_vts_system.start_obs_streaming()
    if success:
        return {"message": "开始OBS推流成功"}
    else:
        raise HTTPException(status_code=500, detail="开始OBS推流失败")

@app.post("/api/obs/streaming/stop")
async def stop_obs_streaming():
    """停止OBS推流"""
    success = obs_vts_system.stop_obs_streaming()
    if success:
        return {"message": "停止OBS推流成功"}
    else:
        raise HTTPException(status_code=500, detail="停止OBS推流失败")

@app.post("/api/vts/connect")
async def connect_to_vts():
    """连接到VTuberStudio"""
    success = obs_vts_system.connect_to_vts()
    if success:
        return {"message": "连接VTuberStudio成功"}
    else:
        raise HTTPException(status_code=500, detail="连接VTuberStudio失败")

@app.post("/api/vts/hotkey")
async def trigger_vts_hotkey(request: Dict[str, Any]):
    """触发VTuberStudio热键"""
    try:
        hotkey_name = request.get("hotkey_name", "")
        if not hotkey_name:
            raise HTTPException(status_code=400, detail="热键名称不能为空")
        
        success = obs_vts_system.trigger_vts_hotkey(hotkey_name)
        if success:
            return {"message": "触发VTuberStudio热键成功"}
        else:
            raise HTTPException(status_code=500, detail="触发VTuberStudio热键失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"触发VTuberStudio热键失败: {str(e)}")

@app.post("/api/vts/expression")
async def set_vts_expression(request: Dict[str, Any]):
    """设置VTuberStudio表情"""
    try:
        expression_name = request.get("expression_name", "")
        if not expression_name:
            raise HTTPException(status_code=400, detail="表情名称不能为空")
        
        success = obs_vts_system.set_vts_expression(expression_name)
        if success:
            return {"message": "设置VTuberStudio表情成功"}
        else:
            raise HTTPException(status_code=500, detail="设置VTuberStudio表情失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"设置VTuberStudio表情失败: {str(e)}")

# 获取状态端点
@app.get("/api/status")
async def get_status():
    """获取系统状态"""
    return {
        "obs": obs_vts_system.get_obs_status(),
        "vts": obs_vts_system.get_vts_status()
    }

if __name__ == "__main__":
    # 修改配置文件路径
    config_manager.config_file = "../../data/config.json"
    config_manager.config = config_manager._load_config()
    
    # 启动服务器
    uvicorn.run(app, host="0.0.0.0", port=8000)
