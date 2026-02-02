#!/usr/bin/env python3
# 简单测试文字转语音功能

from voice_api import voice_api_system
import os

print("测试文字转语音功能...")

# 测试基本功能
test_text = "你好，我是你的AI虚拟主播，很高兴认识你！"
output_file = "test_tts_output.mp3"

print(f"测试文本: {test_text}")
print(f"输出文件: {output_file}")

# 调用TTS功能
result = voice_api_system.text_to_speech(test_text, output_file)

print(f"\n生成结果: {result}")

# 检查输出文件
if result and os.path.exists(output_file):
    file_size = os.path.getsize(output_file) / 1024
    print(f"✅ 音频文件生成成功！")
    print(f"文件大小: {file_size:.2f} KB")
    
    # 清理测试文件
    os.remove(output_file)
    print("测试文件已清理")
else:
    print("❌ 音频文件生成失败")

print("\n测试完成！")
