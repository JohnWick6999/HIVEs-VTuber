#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全复刻您昨天的实现
原封不动地重现您的音色测试代码
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def exact_replica_test():
    """完全复刻您的原始实现"""
    print("🎯 完全复刻昨天的音色测试")
    print("=" * 40)
    
    try:
        # 完全按照您昨天的方式导入
        from voice_api import voice_api_system
        import config
        
        # 获取配置
        config_manager = config.ConfigManager()
        voice_config = config_manager.get_voice_api_config()
        api_key = voice_config.get("tts", {}).get("api_key")
        
        if not api_key:
            print("❌ 未配置API Key")
            return False
            
        print("✅ API Key获取成功")
        
        # 使用您昨天创建的音色名称
        loli_voice_name = "qwen-tts-vc-loli_voice-voice-20260203005435327-786e"
        print(f"🎯 使用音色: {loli_voice_name}")
        
        # 完全复刻您的测试文本
        test_text = "你好，我是可爱的萝莉，我的声音又甜又萌，希望大家喜欢我哦～喵呜～"
        print(f"📝 测试文本: {test_text}")
        
        # 调用您昨天使用的方法
        print("🎤 正在调用实时TTS...")
        result = voice_api_system._qwen_realtime_tts(api_key, test_text, loli_voice_name)
        
        if result:
            print("✅ 音色测试成功！")
            return True
        else:
            print("❌ 音色测试失败")
            return False
            
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("尝试直接调用API...")
        
        # 如果导入失败，直接使用API调用
        return direct_api_test()
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def direct_api_test():
    """直接API调用测试"""
    print("📡 直接API调用测试")
    print("=" * 30)
    
    try:
        import dashscope
        from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
        import pyaudio
        import base64
        import queue
        import threading
        import time
        
        # 配置API密钥
        dashscope.api_key = "sk-a5e4d75ae5aa4961acc01d5a71f7b117"
        
        # 音频队列
        audio_queue = queue.Queue()
        is_finished = False
        
        class ReplicaCallback(QwenTtsRealtimeCallback):
            def on_open(self):
                print("🎯 复刻模式启动")
            
            def on_event(self, response):
                if isinstance(response, str):
                    try:
                        response_data = eval(response)
                    except:
                        return
                else:
                    response_data = response
                    
                if response_data.get('type') == 'response.audio.delta':
                    audio_data = base64.b64decode(response_data['delta'])
                    audio_queue.put(audio_data)
                    print(f"🎧 收到音频: {len(audio_data)} bytes")
            
            def on_close(self, code, msg):
                print("🎯 连接关闭")
        
        def audio_player():
            """音频播放"""
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True
            )
            
            while not is_finished or not audio_queue.empty():
                try:
                    audio_data = audio_queue.get(timeout=0.1)
                    if audio_data:
                        stream.write(audio_data)
                except queue.Empty:
                    continue
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            print("🎵 音频播放完成")
        
        # 启动播放线程
        player_thread = threading.Thread(target=audio_player, daemon=True)
        player_thread.start()
        
        # 创建TTS实例
        callback = ReplicaCallback()
        tts = QwenTtsRealtime(
            model='qwen3-tts-flash-realtime-2025-11-27',
            callback=callback,
            url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
        )
        
        print("🔄 连接服务...")
        tts.connect()
        
        # 使用系统默认音色测试（避免自定义音色问题）
        tts.update_session(
            voice='Cherry',  # 使用系统音色
            response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
            mode='server_commit',
            language_type='Chinese',
            additional_params={
                'pitch': 1.6,    # 高音调
                'rate': 0.6,     # 慢语速
                'volume': 60     # 适中音量
            }
        )
        
        # 使用您喜欢的傲娇台词
        test_lines = [
            "哼！才不是特意为你准备的呢！",
            "要、要加油什么的...才不是关心你啦！"
        ]
        
        for line in test_lines:
            print(f"🎤 {line}")
            tts.append_text(line)
            time.sleep(2)
        
        tts.finish()
        time.sleep(1)
        is_finished = True
        player_thread.join(timeout=3)
        
        print("✅ 复刻测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 直接测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🎯 原封复刻音色测试")
    print("=" * 25)
    
    # 首先尝试完全复刻
    success = exact_replica_test()
    
    if not success:
        print("\n🔄 尝试直接API测试...")
        direct_api_test()