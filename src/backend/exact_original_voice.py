#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
严格按照用户原始预设创建音色
完全复制test_loli_voice.py中的参数和逻辑
"""

import base64
import pathlib
import requests
import json
import time
from datetime import datetime

def create_exact_original_voice():
    """严格按照原始预设创建音色"""
    print("🎯 严格按照原始预设创建音色")
    print("=" * 50)
    
    # 使用您原始代码中的确切参数
    api_key = "sk-a5e4d75ae5aa4961acc01d5a71f7b117"
    audio_file = "../../data/voice/e3fd62b8656da51a240754cb3919d3ea.mp3"
    preferred_name = "loli_voice"
    
    # 检查音频文件
    if not pathlib.Path(audio_file).exists():
        print(f"❌ 音频文件不存在: {audio_file}")
        return None
    
    print(f"✅ 音频文件: {audio_file}")
    print(f"文件大小: {pathlib.Path(audio_file).stat().st_size / (1024*1024):.2f} MB")
    
    # 读取并编码音频文件
    try:
        audio_data = pathlib.Path(audio_file).read_bytes()
        b64_audio = base64.b64encode(audio_data).decode()
        print("✅ 音频文件读取并编码成功")
    except Exception as e:
        print(f"❌ 音频文件处理失败: {e}")
        return None
    
    # 构建请求载荷 - 完全按照您的原始代码
    payload = {
        "model": "qwen-voice-enrollment",
        "input": {
            "action": "create",
            "target_model": "qwen3-tts-vd-realtime-2026-01-15",  # 您的原始target_model
            "preferred_name": preferred_name,
            "preview_text": "大家好，我是可爱的萝莉，我的声音又甜又萌，希望大家喜欢我哦～",  # 您的原始preview_text
            "voice_prompt": "年轻可爱的萝莉音，声音甜美清脆，音调偏高，带有少女感，说话带有一点奶声奶气的感觉，适合动画角色配音。",  # 您的原始voice_prompt
            "audio": {"data": f"data:audio/mpeg;base64,{b64_audio}"}
        }
    }
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # API端点 - 您的原始URL
    url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
    
    print("\n📤 发送创建请求...")
    print(f"Model: {payload['model']}")
    print(f"Target Model: {payload['input']['target_model']}")
    print(f"Preferred Name: {payload['input']['preferred_name']}")
    print(f"Preview Text: {payload['input']['preview_text']}")
    print(f"Voice Prompt: {payload['input']['voice_prompt']}")
    print(f"URL: {url}")
    
    try:
        # 发送请求
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120  # 增加超时时间
        )
        
        print(f"\n📥 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 请求成功!")
            print(f"响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if "output" in result and "voice" in result["output"]:
                voice_name = result["output"]["voice"]
                print(f"\n🎉 成功创建音色!")
                print(f"🎤 音色名称: {voice_name}")
                
                # 保存创建信息
                creation_info = {
                    "timestamp": datetime.now().isoformat(),
                    "voice_name": voice_name,
                    "target_model": payload["input"]["target_model"],
                    "preferred_name": payload["input"]["preferred_name"],
                    "preview_text": payload["input"]["preview_text"],
                    "voice_prompt": payload["input"]["voice_prompt"],
                    "audio_file": audio_file,
                    "full_response": result
                }
                
                info_file = f"exact_original_voice_{int(time.time())}.json"
                with open(info_file, 'w', encoding='utf-8') as f:
                    json.dump(creation_info, f, ensure_ascii=False, indent=2)
                
                print(f"💾 创建信息已保存到: {info_file}")
                
                return voice_name
            else:
                print("❌ 响应中没有找到voice字段")
                print(f"完整响应: {result}")
                return None
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误内容: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_created_voice(voice_name):
    """测试刚创建的音色"""
    if not voice_name:
        print("❌ 没有可测试的音色")
        return False
    
    print(f"\n🧪 测试创建的音色: {voice_name}")
    print("=" * 40)
    
    try:
        import dashscope
        from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
        import pyaudio
        import queue
        import threading
        
        # 配置API密钥
        dashscope.api_key = "sk-a5e4d75ae5aa4961acc01d5a71f7b117"
        
        # 测试文本 - 使用您的原始测试文本
        test_text = "你好，我是可爱的萝莉，我的声音又甜又萌，希望大家喜欢我哦～喵呜～"
        print(f"📝 测试文本: {test_text}")
        
        # 音频队列
        audio_queue = queue.Queue()
        is_playing = True
        
        class TestCallback(QwenTtsRealtimeCallback):
            def on_open(self):
                print("🌙 连接已打开")
            
            def on_event(self, response):
                if isinstance(response, str):
                    try:
                        response_data = json.loads(response)
                    except:
                        return
                else:
                    response_data = response
                
                if response_data.get('type') == 'response.audio.delta':
                    audio_data = base64.b64decode(response_data['delta'])
                    audio_queue.put(audio_data)
                    print(f"🎧 接收到音频数据: {len(audio_data)} bytes")
                
                elif response_data.get('type') == 'session.finished':
                    print("🔄 会话已完成")
                    global is_playing
                    is_playing = False
            
            def on_close(self, code, msg):
                print(f"🌙 连接已关闭: {msg}")
                global is_playing
                is_playing = False
        
        def audio_player():
            """音频播放线程"""
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
                print("🔊 音频播放完成")
                
            except Exception as e:
                print(f"🔊 播放错误: {e}")
        
        # 启动播放线程
        player_thread = threading.Thread(target=audio_player, daemon=True)
        player_thread.start()
        
        # 创建TTS实例
        callback = TestCallback()
        tts = QwenTtsRealtime(
            model='qwen3-tts-vd-realtime-2026-01-15',  # 使用相同的目标模型
            callback=callback,
            url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
        )
        
        print("🔄 连接到TTS服务...")
        tts.connect()
        
        # 配置会话
        tts.update_session(
            voice=voice_name,
            response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
            mode='server_commit'
        )
        
        print("📤 发送测试文本...")
        tts.append_text(test_text)
        tts.finish()
        
        # 等待播放完成
        player_thread.join(timeout=30)
        
        print("✅ 音色测试完成!")
        return True
        
    except Exception as e:
        print(f"❌ 音色测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🎯 严格按照原始预设创建音色系统")
    print("完全复制用户test_loli_voice.py中的参数和逻辑")
    print("=" * 60)
    
    # 第一步：创建音色
    voice_name = create_exact_original_voice()
    
    if voice_name:
        print(f"\n🎉 音色创建成功: {voice_name}")
        
        # 第二步：测试音色
        print("\n" + "=" * 60)
        test_success = test_created_voice(voice_name)
        
        if test_success:
            print(f"\n🎊 完美! 严格按照原始预设创建的音色测试成功!")
            print(f"🎤 音色名称: {voice_name}")
            print("✅ 这就是您要的原始预设效果!")
        else:
            print(f"\n❌ 音色测试失败，但创建成功: {voice_name}")
    else:
        print("\n❌ 音色创建失败")

if __name__ == "__main__":
    main()