#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全独立的音色测试脚本
绕过所有导入问题，直接测试实际音频播放
"""

import time
import base64
import threading
import queue

def test_actual_voice():
    """测试实际的音频播放"""
    print("🔊 实际音色测试开始")
    print("=" * 40)
    
    try:
        # 导入必要的库
        import dashscope
        from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
        import pyaudio
        
        # 配置API密钥
        dashscope.api_key = "sk-a5e4d75ae5aa4961acc01d5a71f7b117"
        
        print("✅ 依赖库导入成功")
        
        # 音频队列和播放器
        audio_queue = queue.Queue()
        is_finished = False
        
        class TestCallback(QwenTtsRealtimeCallback):
            def on_open(self):
                print("📡 WebSocket连接已建立")
            
            def on_close(self, code, msg):
                print(f"🔌 连接关闭: {msg}")
            
            def on_event(self, response):
                if isinstance(response, str):
                    try:
                        response = eval(response)
                    except:
                        return
                
                event_type = response.get('type')
                
                if event_type == 'response.audio.delta':
                    audio_b64 = response.get('delta')
                    if audio_b64:
                        audio_data = base64.b64decode(audio_b64)
                        audio_queue.put(audio_data)
                        print(f"🎧 收到音频数据: {len(audio_data)} bytes")
                
                elif event_type == 'session.created':
                    print("🔄 会话创建成功")
                
                elif event_type == 'session.updated':
                    print("🔄 会话配置完成")
        
        def audio_player_worker():
            """音频播放工作线程"""
            try:
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=24000,
                    output=True
                )
                
                print("🎵 音频播放器已启动")
                
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
            except Exception as e:
                print(f"❌ 音频播放错误: {e}")
        
        # 启动播放线程
        player_thread = threading.Thread(target=audio_player_worker, daemon=True)
        player_thread.start()
        
        # 创建TTS实例
        callback = TestCallback()
        tts = QwenTtsRealtime(
            model='qwen3-tts-flash-realtime-2025-11-27',
            callback=callback,
            url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
        )
        
        print("🔄 连接TTS服务...")
        tts.connect()
        
        # 配置会话参数（使用超级可爱的参数）
        print("🎯 应用超级可爱音色参数...")
        tts.update_session(
            voice='Cherry',
            response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
            mode='server_commit',
            language_type='Chinese',
            additional_params={
                'pitch': 1.6,    # 超高音调
                'rate': 0.6,     # 超慢语速
                'volume': 60,    # 适中音量
                'seed': 88888    # 固定种子
            }
        )
        
        # 发送测试文本
        test_text = "咿呀...人家、人家才不想理你呢..."
        print(f"💬 发送文本: {test_text}")
        tts.append_text(test_text)
        
        # 等待处理完成
        time.sleep(3)
        tts.finish()
        
        # 等待音频播放完成
        time.sleep(2)
        is_finished = True
        player_thread.join(timeout=5)
        
        print("✅ 音色测试完成")
        return True
        
    except ImportError as e:
        print(f"❌ 缺少必要库: {e}")
        print("请安装: pip install dashscope pyaudio")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def quick_voice_demo():
    """快速音色演示"""
    print("⚡ 快速音色演示")
    print("=" * 25)
    
    # 测试几种不同的可爱参数组合
    voice_configs = [
        {
            "name": "🍼 软萌小奶音",
            "params": {"pitch": 1.6, "rate": 0.6, "volume": 60},
            "text": "咿呀...人家才不想理你呢..."
        },
        {
            "name": "👑 傲娇小公主", 
            "params": {"pitch": 1.5, "rate": 0.7, "volume": 65},
            "text": "哼！本princess才不屑和你说话呢！"
        },
        {
            "name": "🦌 害羞小鹿",
            "params": {"pitch": 1.35, "rate": 0.75, "volume": 55},
            "text": "那、那个...请问可以陪我聊聊天吗？"
        }
    ]
    
    for i, config in enumerate(voice_configs, 1):
        print(f"\n🎤 [{i}] {config['name']}")
        print(f"   参数: 音调{config['params']['pitch']}x | 语速{config['params']['rate']}x")
        print(f"   台词: {config['text']}")
        
        # 这里应该调用实际的TTS，但由于环境限制，先展示配置
        print("   (此处应该播放音频，参数已配置)")
        time.sleep(1)
    
    print("\n💡 如需实际音频播放，请确保:")
    print("   1. 已安装 dashscope 和 pyaudio 库")
    print("   2. 网络连接正常")
    print("   3. API密钥有效")

if __name__ == "__main__":
    print("🎀 超级可爱音色实际测试")
    
    # 先尝试实际播放测试
    success = test_actual_voice()
    
    if not success:
        # 如果实际测试失败，至少展示配置
        print("\n📋 配置展示模式:")
        quick_voice_demo()