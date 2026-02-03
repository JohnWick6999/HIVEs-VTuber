#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试可爱傲娇萝莉音功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.backend.voice_api import voice_api_system

def test_cute_loli_voice():
    """测试可爱傲娇萝莉音"""
    print("🎀 测试可爱傲娇萝莉音功能")
    print("=" * 50)
    
    # 1. 获取当前配置
    print("1. 当前语音配置:")
    print(f"   引擎: {voice_api_system.voice_config.get('tts', {}).get('engine')}")
    print(f"   音色: {voice_api_system.voice_config.get('tts', {}).get('voice')}")
    print()
    
    # 2. 创建可爱傲娇萝莉音
    print("2. 创建可爱傲娇萝莉音...")
    cute_voice = voice_api_system.create_cute_loli_voice()
    print()
    
    # 3. 测试TTS功能
    print("3. 测试TTS功能...")
    test_text = "你好呀！人家是你的可爱傲娇萝莉助手哦～ 有什么事情要人家帮忙的吗？哼，才不是想帮你呢，只是觉得你太笨了啦！"
    output_file = "test_cute_loli_voice.wav"
    
    success = voice_api_system.text_to_speech(test_text, output_file)
    if success:
        print(f"✅ TTS测试成功！")
        print(f"📁 生成的音频文件: {output_file}")
        print(f"🎵 请播放该文件查看可爱傲娇萝莉音效果")
    else:
        print("❌ TTS测试失败")
    print()
    
    # 4. 测试实时TTS播放
    print("4. 测试实时TTS播放...")
    real_time_text = "喂，你有没有在听人家说话呀？真是的，一点都不认真！不过...如果你想听人家再说话的话，人家也不是不可以啦～"
    
    real_time_success = voice_api_system.real_time_tts_and_play(real_time_text)
    if real_time_success:
        print("✅ 实时TTS播放测试成功！")
    else:
        print("❌ 实时TTS播放测试失败")
    print()
    
    # 5. 总结
    print("5. 测试总结:")
    print("=" * 50)
    print("🎉 可爱傲娇萝莉音功能测试完成！")
    print(f"🎵 当前使用的音色: {cute_voice}")
    print("💡 提示: 您可以在config.json文件中修改voice字段来切换其他音色")

if __name__ == "__main__":
    test_cute_loli_voice()
