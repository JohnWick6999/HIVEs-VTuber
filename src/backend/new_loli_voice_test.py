#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新创建的萝莉音色
使用您昨天的设计理念重新创建的音色
"""

import dashscope
from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
import pyaudio
import base64
import queue
import threading
import time

def test_new_loli_voice():
    """测试新创建的萝莉音色"""
    print("🌙 测试全新萝莉音色")
    print("=" * 30)
    
    # 配置
    dashscope.api_key = "sk-a5e4d75ae5aa4961acc01d5a71f7b117"
    loli_voice_name = "qwen-tts-vc-new_loli_voice-voice-20260204010829410-44f8"
    
    print(f"🎯 使用音色: {loli_voice_name}")
    
    # 音频队列
    audio_queue = queue.Queue()
    is_finished = False
    
    class NewLoliCallback(QwenTtsRealtimeCallback):
        def on_open(self):
            print("🌙 全新萝莉音色启动")
        
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
                print(f"🎧 收到萝莉音频: {len(audio_data)} bytes")
        
        def on_close(self, code, msg):
            print("🌙 连接关闭")
    
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
        print("🎵 萝莉音频播放完成")
    
    # 启动播放线程
    player_thread = threading.Thread(target=audio_player, daemon=True)
    player_thread.start()
    
    # 创建TTS实例
    callback = NewLoliCallback()
    tts = QwenTtsRealtime(
        model='qwen3-tts-flash-realtime-2025-11-27',
        callback=callback,
        url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
    )
    
    # 连接和配置
    print("🔄 连接萝莉音色服务...")
    tts.connect()
    
    tts.update_session(
        voice=loli_voice_name,
        response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
        mode='server_commit',
        language_type='Chinese'
    )
    
    # 发送萝莉台词
    loli_lines = [
        "喵呜～人家是全新的小萝莉哦～",
        "哼！才不是特意为你准备的呢！",
        "要、要加油什么的...才不是关心你啦！"
    ]
    
    for i, line in enumerate(loli_lines, 1):
        print(f"🌙 [台词{i}]: {line}")
        tts.append_text(line)
        time.sleep(2)
    
    print("🌙 萝莉发言完毕")
    tts.finish()
    time.sleep(2)
    is_finished = True
    player_thread.join(timeout=5)
    
    print("✅ 全新萝莉音色测试完成")

if __name__ == "__main__":
    test_new_loli_voice()