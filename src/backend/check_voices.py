#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询可用的自定义音色
"""

import dashscope
from dashscope.audio.tts_v2 import VoiceEnrollmentService

def check_available_voices():
    """检查可用的自定义音色"""
    print("🔍 查询可用音色")
    print("=" * 30)
    
    # 配置API密钥
    dashscope.api_key = "sk-a5e4d75ae5aa4961acc01d5a71f7b117"
    
    try:
        # 创建音色服务实例
        service = VoiceEnrollmentService()
        
        # 查询可用音色列表
        voices = service.list()
        print("✅ 查询成功")
        print(f"可用音色数量: {len(voices)}")
        
        if voices:
            print("\n🎤 可用音色列表:")
            for i, voice in enumerate(voices, 1):
                print(f"  [{i}] {voice}")
        else:
            print("📭 暂无自定义音色")
            
        return voices
        
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return []

def recreate_loli_voice():
    """重新创建萝莉音色"""
    print("\n🔄 重新创建萝莉音色")
    print("=" * 30)
    
    try:
        import base64
        import pathlib
        import requests
        
        # 配置
        api_key = "sk-a5e4d75ae5aa4961acc01d5a71f7b117"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 检查是否有所需的音频文件
        audio_file = "../../data/voice/e3fd62b8656da51a240754cb3919d3ea.mp3"
        
        if not pathlib.Path(audio_file).exists():
            print(f"❌ 音频文件不存在: {audio_file}")
            print("💡 请提供一个合适的音频样本文件用于创建音色")
            return None
        
        # 读取音频文件
        b64 = base64.b64encode(pathlib.Path(audio_file).read_bytes()).decode()
        
        # 创建音色的参数
        payload = {
            "model": "qwen-voice-enrollment",
            "input": {
                "action": "create",
                "target_model": "qwen3-tts-vd-realtime-2026-01-15",
                "preferred_name": "new_loli_voice",
                "preview_text": "大家好，我是可爱的萝莉，我的声音又甜又萌，希望大家喜欢我哦～",
                "voice_prompt": "年轻可爱的萝莉音，声音甜美清脆，音调偏高，带有少女感，说话带有一点奶声奶气的感觉，适合动画角色配音。",
                "audio": {"data": f"data:audio/mpeg;base64,{b64}"}
            }
        }
        
        url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
        
        print("正在创建新的萝莉音色...")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            voice_name = result["output"]["voice"]
            print(f"✅ 成功创建新萝莉音色: {voice_name}")
            return voice_name
        else:
            print(f"❌ 创建失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 创建过程出错: {e}")
        return None

if __name__ == "__main__":
    # 首先检查现有音色
    available_voices = check_available_voices()
    
    # 如果没有合适的音色，询问是否重新创建
    if not available_voices or input("\n是否重新创建萝莉音色？(y/n): ").lower() == 'y':
        new_voice = recreate_loli_voice()
        if new_voice:
            print(f"\n🎉 新音色创建成功: {new_voice}")
            print("现在可以使用这个音色进行测试了！")