#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试昨天凌晨创建的萝莉音色预设
直接使用您创建的自定义音色
"""

import sys
import os
from pathlib import Path

# 添加路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_yesterday_voice():
    """测试昨天创建的萝莉音色"""
    print("🌙 测试昨天凌晨创建的萝莉音色")
    print("=" * 40)
    
    # 直接使用您创建的音色名称
    loli_voice_name = "qwen-tts-vc-loli_voice-voice-20260203005435327-786e"
    print(f"🎯 使用音色: {loli_voice_name}")
    
    try:
        # 导入必要的库
        import dashscope
        from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
        import pyaudio
        import base64
        import queue
        import threading
        import time
        
        # 从配置文件读取API密钥
        config_path = Path("../data/config.json")
        if config_path.exists():
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            api_key = config_data.get('voice_api', {}).get('tts', {}).get('api_key')
        else:
            # 使用硬编码的API密钥（从之前的测试中获取）
            api_key = "sk-a5e4d75ae5aa4961acc01d5a71f7b117"
        
        if not api_key:
            print("❌ 未找到API密钥")
            return False
            
        dashscope.api_key = api_key
        print("✅ API密钥配置完成")
        
        # 音频处理
        audio_queue = queue.Queue()
        is_finished = False
        
        class LoliCallback(QwenTtsRealtimeCallback):
            def on_open(self):
                print("🌙 萝莉音色连接建立")
            
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
                print("🌙 萝莉音色连接关闭")
        
        def audio_player():
            """音频播放线程"""
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True
            )
            print("🎵 萝莉音频播放器就绪")
            
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
        
        # 创建TTS实例，使用您创建的自定义音色
        callback = LoliCallback()
        tts = QwenTtsRealtime(
            model='qwen3-tts-flash-realtime-2025-11-27',
            callback=callback,
            url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
        )
        
        print("🔄 连接萝莉音色服务...")
        tts.connect()
        
        # 使用您创建的自定义音色
        tts.update_session(
            voice=loli_voice_name,  # 使用您创建的音色
            response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
            mode='server_commit',
            language_type='Chinese'
        )
        
        print("🌙 发送萝莉台词...")
        loli_lines = [
            "喵呜～人家是昨天创建的小萝莉哦～",
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
        
        print("✅ 昨天的萝莉音色测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def list_custom_voices():
    """列出所有自定义音色"""
    print("📋 自定义音色列表")
    print("=" * 30)
    
    # 您创建的音色
    custom_voices = [
        {
            "name": "qwen-tts-vc-loli_voice-voice-20260203005435327-786e",
            "description": "昨天凌晨创建的萝莉音色",
            "created": "2026-02-03 00:54:35",
            "style": "甜美可爱萝莉音"
        }
    ]
    
    for i, voice in enumerate(custom_voices, 1):
        print(f"🎤 [{i}] {voice['name']}")
        print(f"   📝 描述: {voice['description']}")
        print(f"   📅 创建: {voice['created']}")
        print(f"   🎭 风格: {voice['style']}")
        print()

if __name__ == "__main__":
    print("🌙 昨天音色预设测试")
    print("=" * 25)
    
    # 显示自定义音色列表
    list_custom_voices()
    
    # 测试音色
    test_yesterday_voice()