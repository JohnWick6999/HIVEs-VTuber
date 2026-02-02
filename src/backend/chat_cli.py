#!/usr/bin/env python3
# 简单的命令行聊天工具，用于测试AI聊天功能

from ai_chat_system import AIChatSystem
import os

class ChatCLI:
    def __init__(self):
        """初始化命令行聊天工具"""
        print("正在初始化AI聊天系统...")
        self.chat_system = AIChatSystem()
        print("初始化完成！\n")
        print("====================================")
        print("AI Vtuber 命令行聊天工具")
        print("====================================")
        print("输入消息与AI聊天，输入 'exit' 退出")
        print("====================================\n")
    
    def run(self):
        """运行命令行聊天"""
        while True:
            try:
                # 获取用户输入
                user_input = input("你: ")
                
                # 检查是否退出
                if user_input.lower() == 'exit':
                    print("再见！")
                    break
                
                # 检查输入是否为空
                if not user_input.strip():
                    print("请输入消息内容")
                    continue
                
                # 发送消息给AI并获取回复
                print("AI: ", end="", flush=True)
                response = self.chat_system.generate_response(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n再见！")
                break
            except Exception as e:
                print(f"错误: {e}")
                print()

if __name__ == "__main__":
    cli = ChatCLI()
    cli.run()
