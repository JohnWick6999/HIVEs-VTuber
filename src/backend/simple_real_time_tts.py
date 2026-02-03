#!/usr/bin/env python3
# 简化的实时语音生成接口

import threading
import queue
import time
import base64
from voice_api import voice_api_system
import config

class SimpleRealTimeTTS:
    """简化的实时TTS接口"""
    
    def __init__(self):
        self.config_manager = config.ConfigManager()
        self.voice_config = self.config_manager.get_voice_api_config()
        self.api_key = self.voice_config.get("tts", {}).get("api_key")
        self.audio_player = None
        self.is_playing = False
        
    def setup_audio_player(self):
        """设置音频播放器"""
        try:
            import pyaudio
            self.audio_player = pyaudio.PyAudio().open(
                format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True
            )
            print("🔊 音频播放器准备就绪")
            return True
        except Exception as e:
            print(f"❌ 音频播放器设置失败: {e}")
            return False
    
    def play_audio_data(self, audio_data):
        """播放音频数据"""
        if self.audio_player and audio_data:
            try:
                self.audio_player.write(audio_data)
                if not self.is_playing:
                    self.is_playing = True
                    print("🎵 开始播放音频...")
            except Exception as e:
                print(f"⚠️ 音频播放错误: {e}")
    
    def stream_tts(self, text_generator):
        """流式TTS播放 - 接收文本生成器"""
        if not self.api_key:
            print("❌ 请配置API Key")
            return False
            
        if not self.setup_audio_player():
            return False
        
        try:
            import dashscope
            from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
            
            dashscope.api_key = self.api_key
            
            # 实时回调类
            class RealTimeCallback(QwenTtsRealtimeCallback):
                def __init__(self, audio_player_func):
                    super().__init__()
                    self.play_audio = audio_player_func
                    self.connected = threading.Event()
                
                def on_open(self):
                    print("📡 连接已建立")
                
                def on_close(self, code, msg):
                    print(f"🔌 连接已关闭: {msg}")
                
                def on_event(self, response):
                    if isinstance(response, str):
                        response = eval(response)  # 简单解析
                    
                    if response.get('type') == 'response.audio.delta':
                        audio_b64 = response.get('delta')
                        if audio_b64:
                            audio_data = base64.b64decode(audio_b64)
                            self.play_audio(audio_data)
                    elif response.get('type') == 'session.created':
                        self.connected.set()
            
            # 创建回调和TTS实例
            callback = RealTimeCallback(self.play_audio_data)
            tts = QwenTtsRealtime(
                model='qwen3-tts-flash-realtime-2025-11-27',  # 使用官方推荐的最新稳定版
                callback=callback,
                url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
            )
            
            # 连接并配置
            print("🔄 连接TTS服务...")
            tts.connect()
            callback.connected.wait(timeout=5)
            
            tts.update_session(
                voice='Cherry',
                response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
                mode='server_commit'
            )
            
            print("✅ 开始实时流式播放...")
            
            # 流式处理文本 - 优化发送策略
            for text_chunk in text_generator:
                if text_chunk.strip():
                    print(f"📥 发送: {text_chunk}")
                    tts.append_text(text_chunk)
                    # 减少等待时间，提高实时性
                    time.sleep(0.05)  # 50ms延迟
            
            # 完成并等待
            tts.finish()
            time.sleep(1)
            
            print("✅ 实时播放完成")
            return True
            
        except Exception as e:
            print(f"❌ 实时TTS错误: {e}")
            return False
        finally:
            # 清理资源
            if self.audio_player:
                try:
                    self.audio_player.close()
                except:
                    pass

# 使用示例
def demo_simple_real_time():
    """简单演示"""
    tts = SimpleRealTimeTTS()
    
    # 文本生成器示例
    def text_stream():
        texts = [
            "你好，我是AI虚拟主播。",
            "现在进行实时语音演示。",
            "每句话都会立即转换为语音播放。",
            "这就是真正的实时TTS效果。",
            "演示结束，谢谢观看！"
        ]
        for text in texts:
            yield text
            time.sleep(1.5)  # 模拟思考间隔
    
    print("🎙️ 简单实时TTS演示")
    print("=" * 30)
    tts.stream_tts(text_stream())

if __name__ == "__main__":
    demo_simple_real_time()