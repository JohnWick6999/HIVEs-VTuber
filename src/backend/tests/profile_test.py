# 简单的性能测试脚本，用于cProfile分析

from ai_chat_system import AIChatSystem
from voice_api import VoiceAPISystem
from image_api import ImageAPISystem
from search_api import SearchAPISystem
from database import DatabaseManager
from obs_vts import OBSVTSSystem
from config import config_manager

# 测试配置管理器
def test_config():
    print("测试配置管理器...")
    config_manager.get_chat_api_config()
    config_manager.get_voice_api_config()
    config_manager.get_image_api_config()
    config_manager.get_search_api_config()
    config_manager.get_database_config()
    config_manager.get_obs_config()
    config_manager.get_vtuber_studio_config()
    config_manager.get_personality_config()

# 测试AI聊天系统
def test_ai_chat():
    print("测试AI聊天系统...")
    chat_system = AIChatSystem()
    chat_system.generate_response("你好")

# 测试语音API
def test_voice():
    print("测试语音API...")
    voice_api = VoiceAPISystem()
    voice_api.text_to_speech("测试语音合成", "test.mp3")

# 测试图像API
def test_image():
    print("测试图像API...")
    image_api = ImageAPISystem()
    # 创建一个简单的测试图像
    import cv2
    import numpy as np
    import os
    test_image = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite("test_image.jpg", test_image)
    image_api.recognize_image("test_image.jpg")
    os.remove("test_image.jpg")

# 测试搜索API
def test_search():
    print("测试搜索API...")
    search_api = SearchAPISystem()
    search_api.search("Python programming")

# 测试数据库
def test_database():
    print("测试数据库...")
    db = DatabaseManager()
    db.save_chat_message("user", "测试消息")
    db.get_chat_history()

# 测试OBS和VTuberStudio集成
def test_obs_vts():
    print("测试OBS和VTuberStudio集成...")
    obs_vts = OBSVTSSystem()

# 主测试函数
def main():
    print("开始性能测试...")
    test_config()
    test_ai_chat()
    test_voice()
    test_image()
    test_search()
    test_database()
    test_obs_vts()
    print("性能测试完成...")

if __name__ == "__main__":
    main()
