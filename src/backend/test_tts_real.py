#!/usr/bin/env python3
# 实际测试TTS功能

from voice_api import voice_api_system
import os

def test_tts(text, description):
    """测试单个文本的TTS功能"""
    print(f"\n=== 测试: {description} ===")
    print(f"文本: {text}")
    
    output_file = f"test_{description.replace(' ', '_')}.mp3"
    result = voice_api_system.text_to_speech(text, output_file)
    
    if result and os.path.exists(output_file):
        file_size = os.path.getsize(output_file) / 1024
        print(f"✅ 成功生成音频文件！")
        print(f"文件大小: {file_size:.2f} KB")
        os.remove(output_file)
        print("测试文件已清理")
        return True
    else:
        print("❌ 音频文件生成失败")
        return False

print("实际测试TTS功能...")
print("=" * 60)

# 测试1: 基本问候
test_tts("你好，我是你的AI虚拟主播，很高兴认识你！", "基本问候")

# 测试2: 天气播报
test_tts("今天天气晴朗，温度适宜，非常适合户外活动。", "天气播报")

# 测试3: 数学问题
test_tts("123加456等于579，这是一个简单的数学问题。", "数学问题")

# 测试4: 长文本
test_tts("你好，欢迎使用AI虚拟主播系统。我可以为你提供各种信息和服务，包括天气查询、新闻资讯、数学计算等。如果你有任何问题，随时可以问我。", "长文本")

print("\n" + "=" * 60)
print("所有测试完成！")
