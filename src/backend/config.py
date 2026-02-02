import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    """配置管理类"""
    
    def __init__(self, config_file: str = "../../data/config.json"):
        """初始化配置管理器"""
        self.config_file = config_file
        # 确保配置文件目录存在
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                # 加载失败时返回默认配置
                return self._get_default_config()
        else:
            # 返回默认配置
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "chat_api": {
                "api_key": "",
                "base_url": "",
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 1024
            },
            "voice_api": {
                "tts": {
                    "api_key": "",
                    "base_url": "",
                    "voice": "default"
                },
                "asr": {
                    "api_key": "",
                    "base_url": ""
                }
            },
            "image_api": {
                "api_key": "",
                "base_url": ""
            },
            "search_api": {
                "api_key": "",
                "base_url": ""
            },
            "database": {
                "enabled": False,
                "db_path": "chat_history.db"
            },
            "obs": {
                "enabled": False,
                "host": "localhost",
                "port": 4444,
                "password": ""
            },
            "vtuber_studio": {
                "enabled": False,
                "host": "localhost",
                "port": 8001
            },
            "personality": {
                "name": "AI Vtuber",
                "description": "一个友好的AI虚拟主播",
                "greeting": "你好！我是你的AI虚拟主播，很高兴认识你！",
                "tone": "活泼、友好、幽默"
            }
        }
    
    def save_config(self) -> None:
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get_chat_api_config(self) -> Dict[str, Any]:
        """获取ChatAPI配置"""
        return self.config.get("chat_api", {})
    
    def get_voice_api_config(self) -> Dict[str, Any]:
        """获取语音API配置"""
        return self.config.get("voice_api", {})
    
    def get_image_api_config(self) -> Dict[str, Any]:
        """获取图片识别API配置"""
        return self.config.get("image_api", {})
    
    def get_search_api_config(self) -> Dict[str, Any]:
        """获取搜索API配置"""
        return self.config.get("search_api", {})
    
    def get_database_config(self) -> Dict[str, Any]:
        """获取数据库配置"""
        return self.config.get("database", {})
    
    def get_obs_config(self) -> Dict[str, Any]:
        """获取OBS配置"""
        return self.config.get("obs", {})
    
    def get_vtuber_studio_config(self) -> Dict[str, Any]:
        """获取VTuberStudio配置"""
        return self.config.get("vtuber_studio", {})
    
    def get_personality_config(self) -> Dict[str, Any]:
        """获取人格配置"""
        return self.config.get("personality", {})
    
    def update_config(self, section: str, key: str, value: Any) -> None:
        """更新配置"""
        if section in self.config:
            if isinstance(self.config[section], dict):
                self.config[section][key] = value
            else:
                self.config[section] = value
        else:
            self.config[section] = {key: value}
        self.save_config()

# 创建全局配置实例
config_manager = ConfigManager()
