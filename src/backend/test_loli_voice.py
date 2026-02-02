#!/usr/bin/env python3
# 测试创建萝莉音音色

from voice_api import voice_api_system
import os

def test_loli_voice():
    """测试创建萝莉音音色"""
    print("测试创建萝莉音音色")
    print("=" * 60)
    
    # 音频文件路径
    audio_file = "../../data/voice/e3fd62b8656da51a240754cb3919d3ea.mp3"
    
    if not os.path.exists(audio_file):
        print(f"❌ 音频文件不存在: {audio_file}")
        return False
    
    print(f"✅ 找到音频文件: {audio_file}")
    print(f"文件大小: {os.path.getsize(audio_file) / (1024*1024):.2f} MB")
    
    # 获取API Key
    import config
    config_manager = config.ConfigManager()
    voice_config = config_manager.get_voice_api_config()
    api_key = voice_config.get("tts", {}).get("api_key")
    
    if not api_key:
        print("❌ 未配置通义千问API Key")
        return False
    
    print("✅ 已配置通义千问API Key")
    
    # 创建萝莉音音色
    print("\n=== 创建萝莉音音色 ===")
    print("正在使用音频文件创建萝莉音音色...")
    
    # 使用更具体的preferred_name和preview_text
    preferred_name = "loli_voice"
    
    # 修改voice_api.py中的方法，添加voice_prompt参数
    # 由于我们不能直接修改方法参数，我们需要创建一个临时的修改版本
    
    # 直接调用API创建萝莉音音色
    try:
        import base64
        import pathlib
        import requests
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 读取音频文件并编码为base64
        b64 = base64.b64encode(pathlib.Path(audio_file).read_bytes()).decode()
        
        # 使用更具体的参数来创建萝莉音音色
        payload = {
            "model": "qwen-voice-enrollment",
            "input": {
                "action": "create",
                "target_model": "qwen3-tts-vd-realtime-2026-01-15",
                "preferred_name": preferred_name,
                "preview_text": "大家好，我是可爱的萝莉，我的声音又甜又萌，希望大家喜欢我哦～",
                "voice_prompt": "年轻可爱的萝莉音，声音甜美清脆，音调偏高，带有少女感，说话带有一点奶声奶气的感觉，适合动画角色配音。",
                "audio": {"data": f"data:audio/mpeg;base64,{b64}"}
            }
        }
        
        # 正确的北京地域URL
        url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
        
        print("正在发送请求...")
        print(f"Preferred Name: {preferred_name}")
        print(f"Preview Text: 大家好，我是可爱的萝莉，我的声音又甜又萌，希望大家喜欢我哦～")
        
        # 发送请求
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            voice_name = result["output"]["voice"]
            print(f"✅ 成功创建萝莉音音色: {voice_name}")
            
            # 测试实时流式合成
            print("\n=== 测试萝莉音实时合成 ===")
            test_text = "你好，我是可爱的萝莉，我的声音又甜又萌，希望大家喜欢我哦～喵呜～"
            print(f"测试文本: {test_text}")
            
            # 调用实时流式TTS
            result = voice_api_system._qwen_realtime_tts(api_key, test_text, voice_name)
            
            if result:
                print("✅ 萝莉音实时合成成功！")
            else:
                print("❌ 萝莉音实时合成失败")
            
            return True
        else:
            print(f"❌ 创建音色失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False

def main():
    test_loli_voice()

if __name__ == "__main__":
    main()
