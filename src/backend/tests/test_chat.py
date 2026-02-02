#!/usr/bin/env python3
# 测试Deepseek API聊天功能

from ai_chat_system import AIChatSystem

print("测试Deepseek API聊天功能...")

# 创建AI聊天系统实例
chat_system = AIChatSystem()

# 测试基本聊天
print("\n测试1: 基本问候")
response = chat_system.generate_response("你好，你是谁？")
print(f"回复: {response}")

print("\n测试2: 询问天气")
response = chat_system.generate_response("今天天气怎么样？")
print(f"回复: {response}")

print("\n测试3: 简单数学问题")
response = chat_system.generate_response("123 + 456等于多少？")
print(f"回复: {response}")

print("\n测试完成！")
