#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
傲娇小公主音色测试
专门测试最夸张的傲娇音色效果
"""

import dashscope
from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
import pyaudio
import base64
import queue
import threading
import time

def test_princess_voice():
    """测试傲娇小公主音色"""
    print("👑 傲娇小公主音色测试")
    print("=" * 30)
    
    # 配置
    dashscope.api_key = "sk-a5e4d75ae5aa4961acc01d5a71f7b117"
    
    # 音频队列
    audio_queue = queue.Queue()
    is_finished = False
    
    class PrincessCallback(QwenTtsRealtimeCallback):
        def on_open(self):
            print("👑 傲娇小公主模式启动")
        
        def on_event(self, response):
            # 更安全的响应处理
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
                print(f"🎧 收到公主音频: {len(audio_data)} bytes")
        
        def on_close(self, code, msg):
            print("👸 连接关闭")
    
    def audio_player():
        """音频播放线程"""
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=24000,
            output=True
        )
        print("🎵 音频播放器就绪")
        
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
        print("🎵 公主音频播放完成")
    
    # 启动播放线程
    player_thread = threading.Thread(target=audio_player, daemon=True)
    player_thread.start()
    
    # 创建TTS实例
    callback = PrincessCallback()
    tts = QwenTtsRealtime(
        model='qwen3-tts-flash-realtime-2025-11-27',
        callback=callback,
        url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
    )
    
    # 连接和配置
    print("🔄 连接公主专线...")
    tts.connect()
    
    tts.update_session(
        voice='Cherry',
        response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
        mode='server_commit',
        language_type='Chinese',
        additional_params={
            'pitch': 1.5,    # 超高音调
            'rate': 0.7,     # 超慢语速
            'volume': 65,    # 稍大声
            'seed': 99999    # 公主专用种子
        }
    )
    
    # 发送傲娇台词
    princess_lines = [
        "哼！本 princess 才不屑和你说话呢！",
        "喂！不准用那种眼神看着本 princess 啦！",
        "讨、讨厌啦！才不是为了你才这么做的呢！"
    ]
    
    for i, line in enumerate(princess_lines, 1):
        print(f"👸 [台词{i}]: {line}")
        tts.append_text(line)
        time.sleep(2)  # 台词间隔
    
    # 完成处理
    print("👸 公主发言完毕")
    tts.finish()
    time.sleep(2)
    is_finished = True
    player_thread.join(timeout=5)
    
    print("✅ 傲娇小公主测试完成")

if __name__ == "__main__":
    test_princess_voice()