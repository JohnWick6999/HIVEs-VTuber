import socketio
import requests
import json
from typing import Optional, Dict, Any
from config import config_manager

class OBSVTSSystem:
    """OBS和VTuberStudio接入系统类"""
    
    def __init__(self):
        """初始化OBS和VTuberStudio接入系统"""
        self.obs_config = config_manager.get_obs_config()
        self.vts_config = config_manager.get_vtuber_studio_config()
        self.obs_connected = False
        self.vts_connected = False
        self.obs_socket = None
        self.vts_session = requests.Session()
    
    def connect_to_obs(self) -> bool:
        """连接到OBS"""
        if not self.obs_config.get("enabled", False):
            return False
        
        try:
            host = self.obs_config.get("host", "localhost")
            port = self.obs_config.get("port", 4444)
            password = self.obs_config.get("password", "")
            
            # 创建Socket.IO客户端
            self.obs_socket = socketio.Client()
            
            # 连接事件
            @self.obs_socket.event
            def connect():
                print("连接到OBS成功")
                self.obs_connected = True
            
            @self.obs_socket.event
            def disconnect():
                print("与OBS断开连接")
                self.obs_connected = False
            
            # 连接到OBS
            self.obs_socket.connect(f"ws://{host}:{port}", auth={"password": password})
            return True
        except Exception as e:
            print(f"连接OBS失败: {e}")
            self.obs_connected = False
            return False
    
    def disconnect_from_obs(self) -> None:
        """断开与OBS的连接"""
        if self.obs_socket:
            try:
                self.obs_socket.disconnect()
            except Exception as e:
                print(f"断开OBS连接失败: {e}")
            self.obs_connected = False
    
    def set_obs_scene(self, scene_name: str) -> bool:
        """设置OBS场景"""
        if not self.obs_connected:
            return False
        
        try:
            # 发送设置场景的请求
            self.obs_socket.emit("SetCurrentProgramScene", {
                "sceneName": scene_name
            })
            return True
        except Exception as e:
            print(f"设置OBS场景失败: {e}")
            return False
    
    def start_obs_recording(self) -> bool:
        """开始OBS录制"""
        if not self.obs_connected:
            return False
        
        try:
            # 发送开始录制的请求
            self.obs_socket.emit("StartRecord")
            return True
        except Exception as e:
            print(f"开始OBS录制失败: {e}")
            return False
    
    def stop_obs_recording(self) -> bool:
        """停止OBS录制"""
        if not self.obs_connected:
            return False
        
        try:
            # 发送停止录制的请求
            self.obs_socket.emit("StopRecord")
            return True
        except Exception as e:
            print(f"停止OBS录制失败: {e}")
            return False
    
    def start_obs_streaming(self) -> bool:
        """开始OBS推流"""
        if not self.obs_connected:
            return False
        
        try:
            # 发送开始推流的请求
            self.obs_socket.emit("StartStream")
            return True
        except Exception as e:
            print(f"开始OBS推流失败: {e}")
            return False
    
    def stop_obs_streaming(self) -> bool:
        """停止OBS推流"""
        if not self.obs_connected:
            return False
        
        try:
            # 发送停止推流的请求
            self.obs_socket.emit("StopStream")
            return True
        except Exception as e:
            print(f"停止OBS推流失败: {e}")
            return False
    
    def connect_to_vts(self) -> bool:
        """连接到VTuberStudio"""
        if not self.vts_config.get("enabled", False):
            return False
        
        try:
            host = self.vts_config.get("host", "localhost")
            port = self.vts_config.get("port", 8001)
            self.vts_base_url = f"http://{host}:{port}"
            
            # 测试连接
            response = self.vts_session.get(f"{self.vts_base_url}/API/Hello")
            if response.status_code == 200:
                print("连接到VTuberStudio成功")
                self.vts_connected = True
                return True
            else:
                print(f"连接VTuberStudio失败: {response.status_code}")
                self.vts_connected = False
                return False
        except Exception as e:
            print(f"连接VTuberStudio失败: {e}")
            self.vts_connected = False
            return False
    
    def trigger_vts_hotkey(self, hotkey_name: str) -> bool:
        """触发VTuberStudio热键"""
        if not self.vts_connected:
            return False
        
        try:
            response = self.vts_session.post(f"{self.vts_base_url}/API/HotkeyTrigger", json={
                "hotkeyID": hotkey_name
            })
            
            if response.status_code == 200:
                return True
            else:
                print(f"触发VTuberStudio热键失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"触发VTuberStudio热键失败: {e}")
            return False
    
    def set_vts_expression(self, expression_name: str) -> bool:
        """设置VTuberStudio表情"""
        if not self.vts_connected:
            return False
        
        try:
            response = self.vts_session.post(f"{self.vts_base_url}/API/ExpressionActivation", json={
                "expressionName": expression_name,
                "active": True
            })
            
            if response.status_code == 200:
                return True
            else:
                print(f"设置VTuberStudio表情失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"设置VTuberStudio表情失败: {e}")
            return False
    
    def get_obs_status(self) -> Dict[str, Any]:
        """获取OBS状态"""
        return {
            "connected": self.obs_connected,
            "enabled": self.obs_config.get("enabled", False)
        }
    
    def get_vts_status(self) -> Dict[str, Any]:
        """获取VTuberStudio状态"""
        return {
            "connected": self.vts_connected,
            "enabled": self.vts_config.get("enabled", False)
        }

# 创建全局OBS和VTuberStudio接入系统实例
obs_vts_system = OBSVTSSystem()
