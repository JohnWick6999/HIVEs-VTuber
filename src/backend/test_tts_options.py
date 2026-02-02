#!/usr/bin/env python3
# 测试多种TTS方案

from voice_api import VoiceAPISystem
import os

print("测试多种TTS方案...")

# 创建语音API系统实例
voice_api = VoiceAPISystem()

# 测试文本
test_text = "你好，我是你的AI虚拟主播，很高兴认识你！"

print(f"测试文本: {test_text}")
print("=" * 60)

# 测试1: 本地TTS (pyttsx3)
print("\n测试1: 本地TTS (pyttsx3)")
local_output = "test_local_tts.wav"
local_result = voice_api._local_text_to_speech(test_text, local_output)

if local_result and os.path.exists(local_output):
    file_size = os.path.getsize(local_output) / 1024
    print(f"✅ 本地TTS生成成功！")
    print(f"文件大小: {file_size:.2f} KB")
    os.remove(local_output)
    print("测试文件已清理")
else:
    print("❌ 本地TTS生成失败")

# 测试2: Edge TTS
print("\n测试2: Edge TTS")
edge_output = "test_edge_tts.mp3"
# Edge TTS不需要API密钥，直接调用
edge_result = voice_api._edge_text_to_speech("", "", test_text, "zh-CN-YunxiNeural", edge_output)

if edge_result and os.path.exists(edge_output):
    file_size = os.path.getsize(edge_output) / 1024
    print(f"✅ Edge TTS生成成功！")
    print(f"文件大小: {file_size:.2f} KB")
    os.remove(edge_output)
    print("测试文件已清理")
else:
    print("❌ Edge TTS生成失败")

print("\n" + "=" * 60)
print("测试完成！")
