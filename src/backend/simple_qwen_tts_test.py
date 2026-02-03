#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的通义千问实时TTS测试
"""

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat
import pyaudio
import queue
import threading
import time

# 配置API密钥
dashscope.api_key = "sk-a5e4d75ae5aa4961acc01d5a71f7b117"

class TTSResultCallback:
    """TTS结果回调类"""
    def __init__(self, audio_queue):
        self.audio_queue = audio_queue
    
    def on_open(self):
        """连接打开时调用"""
        print("WebSocket连接已打开")
    
    def on_complete(self):
        """合成完成时调用"""
        print("音频合成完成")
    
    def on_error(self, error):
        """发生错误时调用"""
        print(f"TTS错误: {error}")
    
    def on_close(self):
        """连接关闭时调用"""
        print("WebSocket连接已关闭")
    
    def on_event(self, message):
        """收到事件消息时调用"""
        if hasattr(message, 'data'):
            self.audio_queue.put(message.data)
            print(f"收到音频数据: {len(message.data)} bytes")

def simple_real_time_tts(text):
    """简化的实时TTS实现"""
    try:
        # 音频队列
        audio_queue = queue.Queue()
        is_finished = False
        
        # 创建回调对象
        callback = TTSResultCallback(audio_queue)
        
        def play_audio():
            """播放音频"""
            try:
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=22050,
                    output=True
                )
                
                while not is_finished or not audio_queue.empty():
                    try:
                        data = audio_queue.get(timeout=0.1)
                        if data:
                            stream.write(data)
                    except queue.Empty:
                        continue
                
                stream.stop_stream()
                stream.close()
                p.terminate()
                print("音频播放完成")
            except Exception as e:
                print(f"播放错误: {e}")
        
        # 启动播放线程
        play_thread = threading.Thread(target=play_audio, daemon=True)
        play_thread.start()
        
        # 创建合成器
        synthesizer = SpeechSynthesizer(
            model='qwen-tts-v1',
            voice='default',
            format=AudioFormat.PCM_22050HZ_MONO_16BIT,
            callback=callback
        )
        
        print("开始发送文本...")
        synthesizer.streaming_call(text)
        synthesizer.streaming_complete()
        
        # 等待完成
        is_finished = True
        play_thread.join(timeout=10)
        
        print("✅ 实时TTS完成")
        return True
        
    except Exception as e:
        print(f"❌ 实时TTS失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_text = "你好，这是一个实时语音测试"
    print(f"测试文本: {test_text}")
    simple_real_time_tts(test_text)