#!/usr/bin/env python3
# 测试Moonshot（KIMI）文字转语音功能

from voice_api import VoiceAPISystem
import os

print("测试Moonshot（KIMI）文字转语音功能...")

# 创建语音API系统实例
voice_api = VoiceAPISystem()

# 测试文本转语音
print("\n测试1: 基本问候")
test_text_1 = "你好，我是你的AI虚拟主播，很高兴认识你！"
result_1 = voice_api.text_to_speech(test_text_1, "test_hello.mp3")
print(f"生成结果: {result_1}")
if result_1 and os.path.exists("test_hello.mp3"):
    print(f"音频文件已生成，大小: {os.path.getsize('test_hello.mp3') / 1024:.2f} KB")
else:
    print("音频文件生成失败")

print("\n测试2: 天气播报")
test_text_2 = "今天天气晴朗，温度适宜，非常适合户外活动。"
result_2 = voice_api.text_to_speech(test_text_2, "test_weather.mp3")
print(f"生成结果: {result_2}")
if result_2 and os.path.exists("test_weather.mp3"):
    print(f"音频文件已生成，大小: {os.path.getsize('test_weather.mp3') / 1024:.2f} KB")
else:
    print("音频文件生成失败")

print("\n测试3: 数学问题")
test_text_3 = "123加456等于579，这是一个简单的数学问题。"
result_3 = voice_api.text_to_speech(test_text_3, "test_math.mp3")
print(f"生成结果: {result_3}")
if result_3 and os.path.exists("test_math.mp3"):
    print(f"音频文件已生成，大小: {os.path.getsize('test_math.mp3') / 1024:.2f} KB")
else:
    print("音频文件生成失败")

# 清理测试文件
print("\n清理测试文件...")
test_files = ["test_hello.mp3", "test_weather.mp3", "test_math.mp3"]
for file in test_files:
    if os.path.exists(file):
        os.remove(file)
        print(f"已删除: {file}")

print("\n测试完成！")
