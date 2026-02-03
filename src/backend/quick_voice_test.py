#!/usr/bin/env python3
# 快速测试严格按照原始预设创建的音色

import dashscope
from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
import pyaudio
import base64
import queue
import threading

def test_original_voice():
    """测试严格按照原始预设创建的音色"""
    # 配置
    dashscope.api_key = 'sk-a5e4d75ae5aa4961acc01d5a71f7b117'
    voice_name = 'qwen-tts-vc-loli_voice-voice-20260204011321205-6164'
    
    print(f'🧪 测试严格按照原始预设创建的音色: {voice_name}')
    
    # 音频队列
    audio_queue = queue.Queue()
    is_playing = True
    
    class TestCallback(QwenTtsRealtimeCallback):
        def on_open(self):
            print('🌙 连接已打开')
        
        def on_event(self, response):
            global is_playing
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
                print(f'🎧 接收到音频数据: {len(audio_data)} bytes')
            
            elif response_data.get('type') == 'session.finished':
                print('🔄 会话已完成')
                is_playing = False
        
        def on_close(self, code, msg):
            print(f'🌙 连接已关闭: {msg}')
            global is_playing
            is_playing = False

    def audio_player():
        try:
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True,
                frames_per_buffer=1024
            )
            
            while is_playing or not audio_queue.empty():
                try:
                    audio_data = audio_queue.get(timeout=0.1)
                    if audio_data:
                        stream.write(audio_data)
                except queue.Empty:
                    continue
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            print('🔊 音频播放完成')
            
        except Exception as e:
            print(f'🔊 播放错误: {e}')

    # 启动播放线程
    player_thread = threading.Thread(target=audio_player, daemon=True)
    player_thread.start()

    # 创建TTS实例
    callback = TestCallback()
    tts = QwenTtsRealtime(
        model='qwen3-tts-vd-realtime-2026-01-15',
        callback=callback,
        url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
    )

    print('🔄 连接到TTS服务...')
    tts.connect()

    # 配置会话
    tts.update_session(
        voice=voice_name,
        response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
        mode='server_commit'
    )

    # 发送测试文本
    test_text = '你好，我是可爱的萝莉，我的声音又甜又萌，希望大家喜欢我哦～喵呜～'
    print(f'📤 发送测试文本: {test_text}')
    tts.append_text(test_text)
    tts.finish()

    # 等待播放完成
    player_thread.join(timeout=30)
    print('✅ 测试完成!')

if __name__ == "__main__":
    test_original_voice()