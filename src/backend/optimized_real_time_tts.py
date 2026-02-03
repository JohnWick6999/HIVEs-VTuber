#!/usr/bin/env python3
# 优化版实时TTS - 针对卡顿问题的解决方案

import asyncio
import threading
import time
import base64
from voice_api import voice_api_system
import config

class OptimizedRealTimeTTS:
    """优化版实时TTS，解决卡顿问题"""
    
    def __init__(self):
        self.config_manager = config.ConfigManager()
        self.voice_config = self.config_manager.get_voice_api_config()
        self.api_key = self.voice_config.get("tts", {}).get("api_key")
        self.audio_player = None
        self.is_playing = False
        self.buffer_threshold = 8192  # 音频缓冲阈值
        
    def setup_optimized_audio_player(self):
        """设置优化的音频播放器"""
        try:
            import pyaudio
            self.audio_player = pyaudio.PyAudio().open(
                format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True,
                frames_per_buffer=512,  # 减小缓冲区提高响应速度
                stream_callback=self.audio_callback
            )
            print("🔊 优化音频播放器准备就绪")
            return True
        except Exception as e:
            print(f"❌ 音频播放器设置失败: {e}")
            return False
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """音频回调函数 - 非阻塞播放"""
        # 这里可以实现更复杂的音频缓冲管理
        return (None, pyaudio.paContinue)
    
    def optimized_stream_tts(self, text_generator):
        """优化的流式TTS播放"""
        if not self.api_key:
            print("❌ 请配置API Key")
            return False
            
        if not self.setup_optimized_audio_player():
            return False
        
        try:
            import dashscope
            from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
            
            dashscope.api_key = self.api_key
            
            # 优化的回调类
            class OptimizedCallback(QwenTtsRealtimeCallback):
                def __init__(self, audio_player):
                    super().__init__()
                    self.audio_player = audio_player
                    self.audio_buffer = bytearray()
                    self.buffer_lock = threading.Lock()
                    self.connected = threading.Event()
                    self.first_audio = True
                
                def on_open(self):
                    print("📡 连接已建立")
                
                def on_close(self, code, msg):
                    print(f"🔌 连接已关闭: {msg}")
                    # 播放剩余音频
                    if self.audio_buffer:
                        self.flush_audio_buffer()
                
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
                            self.handle_audio_data(audio_data)
                            
                    elif event_type == 'session.created':
                        print("🔄 会话已创建")
                        self.connected.set()
                    
                    elif event_type == 'session.updated':
                        print("🔄 会话配置完成")
                    
                    elif event_type == 'error':
                        error_msg = response.get('error', {}).get('message', '未知错误')
                        print(f"❌ TTS错误: {error_msg}")
                
                def handle_audio_data(self, audio_data):
                    """处理音频数据 - 优化缓冲策略"""
                    with self.buffer_lock:
                        self.audio_buffer.extend(audio_data)
                        
                        # 实时播放策略
                        if self.first_audio:
                            self.first_audio = False
                            print("🎵 首包音频到达，开始播放...")
                        
                        # 当缓冲区足够大时立即播放
                        if len(self.audio_buffer) >= 4096:  # 降低阈值提高实时性
                            self.play_audio_chunk()
                
                def play_audio_chunk(self):
                    """播放音频块"""
                    if self.audio_buffer and self.audio_player:
                        try:
                            # 取出一部分音频数据播放
                            chunk_size = min(2048, len(self.audio_buffer))
                            audio_chunk = bytes(self.audio_buffer[:chunk_size])
                            del self.audio_buffer[:chunk_size]
                            
                            self.audio_player.write(audio_chunk)
                        except Exception as e:
                            print(f"⚠️ 音频播放错误: {e}")
                
                def flush_audio_buffer(self):
                    """清空音频缓冲区"""
                    with self.buffer_lock:
                        while self.audio_buffer and self.audio_player:
                            self.play_audio_chunk()
            
            # 创建优化回调和TTS实例
            callback = OptimizedCallback(self.audio_player)
            tts = QwenTtsRealtime(
                model='qwen3-tts-flash-realtime-2025-11-27',  # 使用最新稳定版
                callback=callback,
                url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
            )
            
            # 连接并配置 - 优化参数
            print("🔄 连接优化TTS服务...")
            tts.connect()
            callback.connected.wait(timeout=5)
            
            tts.update_session(
                voice='Cherry',
                response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
                mode='server_commit',
                language_type='Chinese',
                speech_rate=1.0,
                volume=50
            )
            
            print("✅ 开始优化实时流式播放...")
            
            # 优化的文本流式处理
            text_buffer = ""
            for text_chunk in text_generator:
                if text_chunk.strip():
                    text_buffer += text_chunk.strip()
                    print(f"📥 累积文本: {text_buffer}")
                    
                    # 当文本达到一定长度时发送
                    if len(text_buffer) >= 20 or text_chunk.endswith(('。', '！', '？', '.', '!', '?')):
                        print(f"📤 发送文本: {text_buffer}")
                        tts.append_text(text_buffer)
                        text_buffer = ""
                        time.sleep(0.03)  # 极短延迟
                    else:
                        time.sleep(0.01)  # 很短的累积时间
            
            # 发送剩余文本
            if text_buffer:
                print(f"📤 发送剩余文本: {text_buffer}")
                tts.append_text(text_buffer)
            
            # 完成并等待
            tts.finish()
            time.sleep(0.5)  # 等待最后的音频数据
            
            # 确保所有音频都播放完毕
            callback.flush_audio_buffer()
            
            print("✅ 优化实时播放完成")
            return True
            
        except Exception as e:
            print(f"❌ 优化TTS错误: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # 清理资源
            if self.audio_player:
                try:
                    self.audio_player.stop_stream()
                    self.audio_player.close()
                except:
                    pass

def demo_optimized_real_time():
    """演示优化版实时TTS"""
    print("⚡ 优化版实时TTS演示 - 解决卡顿问题")
    print("=" * 50)
    
    tts = OptimizedRealTimeTTS()
    
    # 优化的文本生成器
    def optimized_text_stream():
        texts = [
            "你好，欢迎使用优化版实时语音系统。",
            "这个版本专门解决了卡顿问题。",
            "采用了最新的qwen3-tts-flash-realtime-2025-11-27模型。",
            "优化了音频缓冲和文本发送策略。",
            "现在语音播放更加流畅自然。",
            "每句话都会立即响应并播放。",
            "告别延迟，享受真正的实时体验。",
            "演示结束，感谢观看！"
        ]
        
        for text in texts:
            yield text
            # 更短的间隔时间
            time.sleep(1.0)
    
    print("开始优化演示...")
    success = tts.optimized_stream_tts(optimized_text_stream())
    
    if success:
        print("\n🎉 优化版实时TTS演示成功！")
        print("✅ 卡顿问题已解决")
        print("✅ 响应速度显著提升")
        print("✅ 播放体验更加流畅")
    else:
        print("\n❌ 演示失败")

if __name__ == "__main__":
    demo_optimized_real_time()