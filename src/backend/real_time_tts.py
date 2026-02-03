#!/usr/bin/env python3
# 实时语音生成系统 - Real-time TTS Streaming

import asyncio
import threading
import queue
import time
import os
from voice_api import voice_api_system
import config

class RealTimeTTSStreamer:
    """实时TTS流式播放系统"""
    
    def __init__(self):
        """初始化实时TTS系统"""
        self.config_manager = config.ConfigManager()
        self.voice_config = self.config_manager.get_voice_api_config()
        self.api_key = self.voice_config.get("tts", {}).get("api_key")
        
        # 音频播放相关
        self.audio_player = None
        self.is_playing = False
        self.text_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        
        # 线程控制
        self.playback_thread = None
        self.tts_thread = None
        self.running = False
        
    def initialize_audio_player(self):
        """初始化音频播放器"""
        try:
            import pyaudio
            self.audio_player = pyaudio.PyAudio().open(
                format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True,
                frames_per_buffer=1024
            )
            print("✅ 音频播放器初始化成功")
            return True
        except Exception as e:
            print(f"❌ 音频播放器初始化失败: {e}")
            return False
    
    def play_audio_chunk(self, audio_data):
        """播放音频数据块"""
        if self.audio_player and audio_data:
            try:
                self.audio_player.write(audio_data)
                if not self.is_playing:
                    self.is_playing = True
                    print("🔊 开始实时音频播放...")
            except Exception as e:
                print(f"⚠️ 音频播放错误: {e}")
    
    def audio_playback_worker(self):
        """音频播放工作线程"""
        print("🎧 音频播放线程启动")
        while self.running:
            try:
                # 从音频队列获取数据
                audio_chunk = self.audio_queue.get(timeout=0.1)
                if audio_chunk is None:  # 结束信号
                    break
                self.play_audio_chunk(audio_chunk)
                self.audio_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ 音频播放线程错误: {e}")
                break
        print("🎧 音频播放线程结束")
    
    def tts_worker(self):
        """TTS文本处理工作线程"""
        print("🤖 TTS处理线程启动")
        while self.running:
            try:
                # 从文本队列获取文本
                text_chunk = self.text_queue.get(timeout=0.1)
                if text_chunk is None:  # 结束信号
                    break
                
                print(f"📥 处理文本: {text_chunk}")
                
                # 调用实时TTS生成音频
                success = self.generate_audio_chunk(text_chunk)
                if not success:
                    print(f"❌ TTS生成失败: {text_chunk}")
                
                self.text_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ TTS处理线程错误: {e}")
                break
        print("🤖 TTS处理线程结束")
    
    def generate_audio_chunk(self, text):
        """生成单个文本块的音频"""
        if not self.api_key:
            print("❌ 未配置API Key")
            return False
        
        try:
            import base64
            import dashscope
            from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
            
            dashscope.api_key = self.api_key
            
            # 回调类用于实时接收音频数据
            class StreamCallback(QwenTtsRealtimeCallback):
                def __init__(self, audio_queue):
                    super().__init__()
                    self.audio_queue = audio_queue
                    self.session_ready = threading.Event()
                
                def on_open(self) -> None:
                    print("📞 实时TTS连接已打开")
                
                def on_close(self, close_status_code, close_msg) -> None:
                    print(f"📞 实时TTS连接已关闭: {close_msg}")
                
                def on_event(self, response) -> None:
                    try:
                        if isinstance(response, str):
                            import json
                            response = json.loads(response)
                        
                        event_type = response.get('type')
                        
                        if event_type == 'session.created':
                            print("🔄 实时会话已创建")
                            self.session_ready.set()
                        
                        elif event_type == 'session.updated':
                            print("🔄 实时会话配置已更新")
                        
                        elif event_type == 'response.audio.delta':
                            # 实时接收音频数据
                            audio_b64 = response.get('delta')
                            if audio_b64:
                                audio_data = base64.b64decode(audio_b64)
                                self.audio_queue.put(audio_data)
                        
                        elif event_type == 'session.finished':
                            print("🔄 实时会话已结束")
                            
                        elif event_type == 'error':
                            error_msg = response.get('error', {}).get('message', '未知错误')
                            print(f"❌ 实时TTS错误: {error_msg}")
                            
                    except Exception as e:
                        print(f"❌ 处理实时TTS事件失败: {e}")
            
            # 创建回调实例
            callback = StreamCallback(self.audio_queue)
            
            # 创建实时TTS实例
            tts = QwenTtsRealtime(
                model='qwen3-tts-flash-realtime',
                callback=callback,
                url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
            )
            
            # 连接并配置
            tts.connect()
            callback.session_ready.wait(timeout=5)  # 等待会话准备就绪
            
            tts.update_session(
                voice='Cherry',
                response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
                mode='server_commit',
                language_type="Chinese"
            )
            
            # 发送文本
            tts.append_text(text)
            time.sleep(0.1)  # 给服务器处理时间
            tts.finish()
            
            # 等待一小段时间确保音频传输完成
            time.sleep(0.5)
            
            return True
            
        except Exception as e:
            print(f"❌ 实时TTS生成失败: {e}")
            return False
    
    def start_streaming(self):
        """启动实时流式播放"""
        if not self.api_key:
            print("❌ 请先配置通义千问API Key")
            return False
        
        print("🚀 启动实时TTS流式播放系统...")
        
        # 初始化音频播放器
        if not self.initialize_audio_player():
            return False
        
        # 启动各工作线程
        self.running = True
        
        # 启动音频播放线程
        self.playback_thread = threading.Thread(target=self.audio_playback_worker, daemon=True)
        self.playback_thread.start()
        
        # 启动TTS处理线程
        self.tts_thread = threading.Thread(target=self.tts_worker, daemon=True)
        self.tts_thread.start()
        
        print("✅ 实时TTS系统启动成功")
        print("💡 使用 add_text() 方法添加要播放的文本")
        print("💡 使用 stop_streaming() 方法停止系统")
        
        return True
    
    def add_text(self, text):
        """添加文本到播放队列"""
        if not self.running:
            print("❌ 系统未运行，请先调用 start_streaming()")
            return False
        
        if text.strip():
            self.text_queue.put(text.strip())
            print(f"✅ 已添加文本到队列: {text.strip()}")
            return True
        return False
    
    def stop_streaming(self):
        """停止实时流式播放"""
        print("🛑 停止实时TTS流式播放系统...")
        
        self.running = False
        
        # 发送结束信号
        if self.text_queue:
            self.text_queue.put(None)
        if self.audio_queue:
            self.audio_queue.put(None)
        
        # 等待线程结束
        if self.tts_thread and self.tts_thread.is_alive():
            self.tts_thread.join(timeout=2)
        if self.playback_thread and self.playback_thread.is_alive():
            self.playback_thread.join(timeout=2)
        
        # 关闭音频播放器
        if self.audio_player:
            try:
                self.audio_player.stop_stream()
                self.audio_player.close()
                print("🔇 音频播放器已关闭")
            except:
                pass
        
        print("✅ 实时TTS系统已停止")

# 全局实例
real_time_tts = RealTimeTTSStreamer()

def demo_real_time_tts():
    """演示实时TTS功能"""
    print("🎙️ 实时TTS演示")
    print("=" * 50)
    
    # 启动实时系统
    if not real_time_tts.start_streaming():
        return
    
    try:
        # 演示文本
        demo_texts = [
            "你好，我是你的AI虚拟主播。",
            "现在开始实时语音播放演示。",
            "这段话会被实时转换为语音并播放出来。",
            "你可以看到文本是如何被流式处理的。",
            "实时TTS技术让语音更加自然流畅。",
            "感谢观看这次演示，再见！"
        ]
        
        print("\n开始播放演示文本...")
        
        # 逐个添加文本
        for i, text in enumerate(demo_texts):
            print(f"\n[{i+1}/{len(demo_texts)}] 添加文本: {text}")
            real_time_tts.add_text(text)
            time.sleep(2)  # 间隔2秒添加下一个文本
        
        # 等待所有文本处理完成
        print("\n⏳ 等待所有文本处理完成...")
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断演示")
    finally:
        real_time_tts.stop_streaming()
        print("🔚 演示结束")

if __name__ == "__main__":
    demo_real_time_tts()