#!/usr/bin/env python3
# 自动测试天气查询功能

from ai_chat_system import AIChatSystem

print("测试天气查询功能...")

# 创建AI聊天系统实例
chat_system = AIChatSystem()

# 测试北京天气查询
print("\n测试: 北京今天天气")
response = chat_system.generate_response("北京今天天气")
print(f"AI回复: {response}")

# 测试上海天气查询
print("\n测试: 上海今天天气")
response = chat_system.generate_response("上海今天天气")
print(f"AI回复: {response}")

print("\n测试完成！")
