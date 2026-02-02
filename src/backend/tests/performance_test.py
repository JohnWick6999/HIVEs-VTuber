import time
import psutil
import os
import sys
from memory_profiler import memory_usage

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入要测试的模块
from config import config_manager
from ai_chat_system import AIChatSystem
from voice_api import VoiceAPISystem
from image_api import ImageAPISystem
from search_api import SearchAPISystem
from database import DatabaseManager
from obs_vts import OBSVTSSystem

class PerformanceTester:
    def __init__(self):
        self.results = []
        print("初始化性能测试工具...")
    
    def test_function(self, func_name, func, *args, **kwargs):
        """测试单个函数的性能"""
        start_time = time.time()
        start_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = str(e)
            success = False
        
        end_time = time.time()
        end_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        
        execution_time = (end_time - start_time) * 1000  # 转换为毫秒
        memory_used = end_memory - start_memory
        
        test_result = {
            "function": func_name,
            "execution_time_ms": execution_time,
            "memory_used_mb": memory_used,
            "success": success,
            "result": result
        }
        
        self.results.append(test_result)
        print(f"{func_name}: {execution_time:.2f}ms, {memory_used:.2f}MB, {'成功' if success else '失败'}")
        
        return test_result
    
    def test_config_manager(self):
        """测试配置管理器"""
        print("\n测试配置管理器...")
        self.test_function("config_manager.get_chat_api_config", config_manager.get_chat_api_config)
        self.test_function("config_manager.get_voice_api_config", config_manager.get_voice_api_config)
        self.test_function("config_manager.get_image_api_config", config_manager.get_image_api_config)
    
    def test_ai_chat_system(self):
        """测试AI聊天系统"""
        print("\n测试AI聊天系统...")
        chat_system = AIChatSystem()
        self.test_function("AIChatSystem初始化", AIChatSystem)
        self.test_function("AIChatSystem.generate_response", chat_system.generate_response, "你好")
    
    def test_voice_api(self):
        """测试语音API"""
        print("\n测试语音API...")
        voice_api = VoiceAPISystem()
        self.test_function("VoiceAPISystem初始化", VoiceAPISystem)
        self.test_function("VoiceAPISystem.text_to_speech", voice_api.text_to_speech, "测试语音合成", "test.mp3")
    
    def test_image_api(self):
        """测试图像API"""
        print("\n测试图像API...")
        image_api = ImageAPISystem()
        self.test_function("ImageAPISystem初始化", ImageAPISystem)
        # 创建一个简单的测试图像
        import cv2
        import numpy as np
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite("test_image.jpg", test_image)
        self.test_function("ImageAPISystem.recognize_image", image_api.recognize_image, "test_image.jpg")
        os.remove("test_image.jpg")
    
    def test_search_api(self):
        """测试搜索API"""
        print("\n测试搜索API...")
        search_api = SearchAPISystem()
        self.test_function("SearchAPISystem初始化", SearchAPISystem)
        self.test_function("SearchAPISystem.search", search_api.search, "Python programming")
    
    def test_database(self):
        """测试数据库"""
        print("\n测试数据库...")
        db = DatabaseManager()
        self.test_function("DatabaseManager初始化", DatabaseManager)
        self.test_function("DatabaseManager.save_chat_message", db.save_chat_message, "user", "测试消息")
        self.test_function("DatabaseManager.get_chat_history", db.get_chat_history)
    
    def test_obs_vts(self):
        """测试OBS和VTuberStudio集成"""
        print("\n测试OBS和VTuberStudio集成...")
        obs_vts = OBSVTSSystem()
        self.test_function("OBSVTSSystem初始化", OBSVTSSystem)
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始性能测试...\n")
        
        # 运行各个模块的测试
        self.test_config_manager()
        self.test_ai_chat_system()
        self.test_voice_api()
        self.test_image_api()
        self.test_search_api()
        self.test_database()
        self.test_obs_vts()
        
        # 打印测试结果汇总
        print("\n\n性能测试结果汇总:")
        print("-" * 80)
        print(f"{'函数':<40} {'执行时间(ms)':<15} {'内存使用(MB)':<15} {'状态':<10}")
        print("-" * 80)
        
        total_time = 0
        total_memory = 0
        success_count = 0
        
        for result in self.results:
            total_time += result["execution_time_ms"]
            total_memory += result["memory_used_mb"]
            if result["success"]:
                success_count += 1
            
            print(f"{result['function']:<40} {result['execution_time_ms']:.2f}ms {'{:.2f}MB'.format(result['memory_used_mb']):<15} {'成功' if result['success'] else '失败':<10}")
        
        print("-" * 80)
        print(f"{'总计':<40} {total_time:.2f}ms {'{:.2f}MB'.format(total_memory):<15} {'{}/{}'.format(success_count, len(self.results)):<10}")
        print("-" * 80)
        
        # 分析性能瓶颈
        print("\n性能瓶颈分析:")
        slowest_functions = sorted(self.results, key=lambda x: x["execution_time_ms"], reverse=True)[:3]
        print("最慢的3个函数:")
        for i, func in enumerate(slowest_functions, 1):
            print(f"{i}. {func['function']}: {func['execution_time_ms']:.2f}ms")
        
        most_memory_functions = sorted(self.results, key=lambda x: x["memory_used_mb"], reverse=True)[:3]
        print("\n内存使用最多的3个函数:")
        for i, func in enumerate(most_memory_functions, 1):
            print(f"{i}. {func['function']}: {func['memory_used_mb']:.2f}MB")

if __name__ == "__main__":
    # 安装必要的依赖
    try:
        import memory_profiler
    except ImportError:
        print("安装memory_profiler...")
        os.system("pip install memory_profiler psutil opencv-python")
        import memory_profiler
    
    tester = PerformanceTester()
    tester.run_all_tests()
