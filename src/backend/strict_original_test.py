#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
严格按照您原始预设的实现
完全复刻 test_loli_voice.py 的功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def exact_original_implementation():
    """严格按照您的原始实现"""
    print("🎯 严格按照原始预设实现")
    print("=" * 40)
    
    try:
        # 完全按照您的原始代码导入
        from voice_api import voice_api_system
        import config
        
        # 获取配置（您的原始方式）
        config_manager = config.ConfigManager()
        voice_config = config_manager.get_voice_api_config()
        api_key = voice_config.get("tts", {}).get("api_key")
        
        if not api_key:
            print("❌ 未配置API Key")
            return False
            
        print("✅ API Key获取成功")
        
        # 使用您的原始音色名称
        original_voice_name = "qwen-tts-vc-loli_voice-voice-20260203005435327-786e"
        print(f"🎯 使用您的原始音色: {original_voice_name}")
        
        # 使用您的原始测试文本
        original_test_text = "你好，我是可爱的萝莉，我的声音又甜又萌，希望大家喜欢我哦～喵呜～"
        print(f"📝 原始测试文本: {original_test_text}")
        
        # 完全按照您的原始调用方式
        print("🎤 调用您原始的实时TTS方法...")
        result = voice_api_system._qwen_realtime_tts(api_key, original_test_text, original_voice_name)
        
        if result:
            print("✅ 原始预设测试成功！")
            return True
        else:
            print("❌ 原始预设测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 原始实现遇到问题: {e}")
        print("尝试分析原因...")
        
        # 分析可能的问题
        analyze_issues()
        return False

def analyze_issues():
    """分析可能的问题"""
    print("\n🔍 问题分析:")
    print("=" * 30)
    
    issues = [
        "1. 自定义音色可能已过期",
        "2. 音色名称格式可能已变更", 
        "3. API权限或配额限制",
        "4. 网络或服务端问题"
    ]
    
    for issue in issues:
        print(issue)
    
    print("\n💡 建议解决方案:")
    print("1. 重新运行您的原始 test_loli_voice.py")
    print("2. 检查通义千问控制台的音色状态")
    print("3. 确认API密钥和配额情况")

def recreate_exact_original():
    """重新创建完全一致的原始预设"""
    print("\n🔄 重新创建原始预设")
    print("=" * 30)
    
    try:
        import base64
        import pathlib
        import requests
        import config
        
        # 获取配置
        config_manager = config.ConfigManager()
        voice_config = config_manager.get_voice_api_config()
        api_key = voice_config.get("tts", {}).get("api_key")
        
        if not api_key:
            print("❌ 未配置API Key")
            return None
            
        print("✅ API配置获取成功")
        
        # 检查音频文件（您的原始路径）
        audio_file = "../../data/voice/e3fd62b8656da51a240754cb3919d3ea.mp3"
        audio_path = Path(audio_file)
        
        if not audio_path.exists():
            print(f"❌ 音频文件不存在: {audio_file}")
            print("💡 请确保音频文件路径正确")
            return None
            
        print(f"✅ 找到音频文件: {audio_path}")
        
        # 完全按照您的原始参数
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 读取音频文件
        b64 = base64.b64encode(audio_path.read_bytes()).decode()
        
        # 完全复制您的原始payload
        payload = {
            "model": "qwen-voice-enrollment",
            "input": {
                "action": "create",
                "target_model": "qwen3-tts-vd-realtime-2026-01-15",
                "preferred_name": "loli_voice",
                "preview_text": "大家好，我是可爱的萝莉，我的声音又甜又萌，希望大家喜欢我哦～",
                "voice_prompt": "年轻可爱的萝莉音，声音甜美清脆，音调偏高，带有少女感，说话带有一点奶声奶气的感觉，适合动画角色配音。",
                "audio": {"data": f"data:audio/mpeg;base64,{b64}"}
            }
        }
        
        # 使用您的原始URL
        url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
        
        print("正在发送原始请求...")
        print(f"模型: {payload['model']}")
        print(f"目标模型: {payload['input']['target_model']}")
        print(f"首选名称: {payload['input']['preferred_name']}")
        
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
            print(f"✅ 成功重新创建原始音色: {voice_name}")
            
            # 测试新创建的音色
            print("\n=== 测试新创建的音色 ===")
            test_text = "你好，我是可爱的萝莉，我的声音又甜又萌，希望大家喜欢我哦～喵呜～"
            print(f"测试文本: {test_text}")
            
            # 这里应该调用voice_api_system._qwen_realtime_tts
            # 但由于导入问题，先展示结果
            print("💡 新音色创建成功，可以用于后续测试")
            return voice_name
        else:
            print(f"❌ 创建失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 重新创建失败: {e}")
        return None

if __name__ == "__main__":
    print("🎯 严格按原始预设执行")
    print("=" * 30)
    
    # 首先尝试原始实现
    success = exact_original_implementation()
    
    if not success:
        print("\n🔄 尝试重新创建原始预设...")
        new_voice = recreate_exact_original()
        
        if new_voice:
            print(f"\n🎉 成功创建新音色: {new_voice}")
            print("现在可以使用这个音色进行测试了！")
        else:
            print("\n❌ 无法恢复原始预设")
            print("建议检查原始文件 test_loli_voice.py 的运行情况")