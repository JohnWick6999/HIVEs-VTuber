#!/usr/bin/env python3
# 功能测试脚本，验证各个模块是否正常工作

import os
import sys
from config import config_manager
from ai_chat_system import AIChatSystem
from voice_api import VoiceAPISystem
from image_api import ImageAPISystem
from search_api import SearchAPISystem
from database import DatabaseManager
from obs_vts import OBSVTSSystem

class FunctionalityTester:
    def __init__(self):
        self.results = []
        print("初始化功能测试工具...")
    
    def test_feature(self, feature_name, test_func):
        """测试单个功能"""
        print(f"\n测试 {feature_name}...")
        try:
            result = test_func()
            self.results.append({"feature": feature_name, "status": "成功", "result": result})
            print(f"✅ {feature_name} 测试成功")
            return True
        except Exception as e:
            self.results.append({"feature": feature_name, "status": "失败", "error": str(e)})
            print(f"❌ {feature_name} 测试失败: {e}")
            return False
    
    def test_config_manager(self):
        """测试配置管理器"""
        def test_func():
            # 测试获取各种配置
            chat_config = config_manager.get_chat_api_config()
            voice_config = config_manager.get_voice_api_config()
            image_config = config_manager.get_image_api_config()
            search_config = config_manager.get_search_api_config()
            db_config = config_manager.get_database_config()
            obs_config = config_manager.get_obs_config()
            vts_config = config_manager.get_vtuber_studio_config()
            personality_config = config_manager.get_personality_config()
            return "所有配置获取成功"
        return self.test_feature("配置管理器", test_func)
    
    def test_ai_chat_system(self):
        """测试AI聊天系统"""
        def test_func():
            chat_system = AIChatSystem()
            response = chat_system.generate_response("你好")
            return f"生成回复: {response}"
        return self.test_feature("AI聊天系统", test_func)
    
    def test_voice_api(self):
        """测试语音API"""
        def test_func():
            voice_api = VoiceAPISystem()
            # 测试文本转语音
            result = voice_api.text_to_speech("测试语音合成", "test_voice.mp3")
            # 清理测试文件
            if os.path.exists("test_voice.mp3"):
                os.remove("test_voice.mp3")
            return f"语音合成结果: {result}"
        return self.test_feature("语音API", test_func)
    
    def test_image_api(self):
        """测试图像API"""
        def test_func():
            image_api = ImageAPISystem()
            # 创建测试图像
            import cv2
            import numpy as np
            test_image = np.zeros((100, 100, 3), dtype=np.uint8)
            cv2.imwrite("test_image.jpg", test_image)
            # 测试图像识别
            result = image_api.recognize_image("test_image.jpg")
            # 清理测试文件
            if os.path.exists("test_image.jpg"):
                os.remove("test_image.jpg")
            return f"图像识别结果: {result}"
        return self.test_feature("图像API", test_func)
    
    def test_search_api(self):
        """测试搜索API"""
        def test_func():
            search_api = SearchAPISystem()
            result = search_api.search("Python programming")
            return f"搜索结果: {result}"
        return self.test_feature("搜索API", test_func)
    
    def test_database(self):
        """测试数据库"""
        def test_func():
            db = DatabaseManager()
            # 测试保存消息
            save_result = db.save_chat_message("user", "测试消息")
            # 测试获取历史
            history = db.get_chat_history()
            # 测试获取角色信息
            character = db.get_character_info()
            return f"保存结果: {save_result}, 历史记录数: {len(history)}, 角色信息: {character}"
        return self.test_feature("数据库", test_func)
    
    def test_obs_vts(self):
        """测试OBS和VTuberStudio集成"""
        def test_func():
            obs_vts = OBSVTSSystem()
            # 测试获取状态
            obs_status = obs_vts.get_obs_status()
            vts_status = obs_vts.get_vts_status()
            return f"OBS状态: {obs_status}, VTuberStudio状态: {vts_status}"
        return self.test_feature("OBS和VTuberStudio集成", test_func)
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始功能测试...")
        
        # 运行各个测试
        self.test_config_manager()
        self.test_ai_chat_system()
        self.test_voice_api()
        self.test_image_api()
        self.test_search_api()
        self.test_database()
        self.test_obs_vts()
        
        # 输出测试结果汇总
        print("\n\n功能测试结果汇总:")
        print("-" * 80)
        print(f"{'功能':<30} {'状态':<10} {'结果/错误':<40}")
        print("-" * 80)
        
        success_count = 0
        total_count = len(self.results)
        
        for result in self.results:
            status = result["status"]
            if status == "成功":
                success_count += 1
                detail = result.get("result", "")
            else:
                detail = result.get("error", "")
            
            # 限制详情长度
            if len(detail) > 35:
                detail = detail[:35] + "..."
            
            print(f"{result['feature']:<30} {status:<10} {detail:<40}")
        
        print("-" * 80)
        print(f"{'总计':<30} {success_count}/{total_count} 成功")
        print("-" * 80)
        
        if success_count == total_count:
            print("🎉 所有功能测试成功！")
        else:
            print("⚠️  部分功能测试失败，需要检查修复。")

if __name__ == "__main__":
    tester = FunctionalityTester()
    tester.run_all_tests()
