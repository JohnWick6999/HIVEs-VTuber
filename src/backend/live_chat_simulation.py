#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直播间聊天模拟器
模拟真实直播环境，支持实时语音对话和VTS口型同步
"""

import asyncio
import sys
import os
from pathlib import Path
import threading
import time

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.backend.vts_integration import vts_integration
from src.backend.voice_api import voice_api_system

class LiveChatSimulator:
    """直播间聊天模拟器"""
    
    def __init__(self):
        self.is_running = False
        self.message_counter = 0
        self.session_id = f"live_session_{int(time.time())}"
        
    async def initialize_system(self):
        """初始化系统"""
        print("=" * 60)
        print("🎮 虚拟主播直播间模拟器")
        print("=" * 60)
        print(f"📅 会话ID: {self.session_id}")
        print("🔄 正在初始化系统...")
        
        # 连接VTS
        print("🔌 连接VTubeStudio...")
        vts_connected = await vts_integration.connect()
        if not vts_connected:
            print("❌ VTS连接失败，将继续进行语音测试")
        
        print("✅ 系统初始化完成！")
        print("\n💡 使用说明：")
        print("   - 直接输入文字与虚拟主播对话")
        print("   - 输入 'quit' 或 'exit' 退出")
        print("   - 输入 'stats' 查看统计信息")
        print("   - 输入 'test' 进行功能测试")
        print("-" * 60)
    
    def play_audio_with_vts_sync(self, text, filename=None):
        """播放音频并同步VTS口型"""
        if filename is None:
            filename = f"live_message_{self.message_counter}.wav"
        
        # 生成语音并播放
        success = vts_integration.text_to_speech_with_lip_sync(text, filename)
        return success
    
    async def handle_user_input(self):
        """处理用户输入"""
        while self.is_running:
            try:
                user_input = input("👤 您: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', '退出']:
                    await self.shutdown()
                    break
                    
                elif user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                    
                elif user_input.lower() == 'test':
                    await self.run_diagnostics()
                    continue
                
                # 处理普通聊天
                self.message_counter += 1
                print(f"🤖 虚拟主播: {user_input}")
                
                # 在后台线程中播放音频
                audio_thread = threading.Thread(
                    target=self.play_audio_with_vts_sync,
                    args=(user_input,),
                    daemon=True
                )
                audio_thread.start()
                
            except KeyboardInterrupt:
                await self.shutdown()
                break
            except Exception as e:
                print(f"❌ 输入处理错误: {e}")
    
    async def run_diagnostics(self):
        """运行诊断测试"""
        print("\n🔧 运行系统诊断...")
        
        # 测试TTS
        print("🔊 测试文本转语音...")
        test_text = "系统诊断测试，检查语音功能是否正常。"
        tts_success = vts_integration.text_to_speech_with_lip_sync(
            test_text, "diagnostic_test.wav"
        )
        print(f"   TTS测试: {'✅ 通过' if tts_success else '❌ 失败'}")
        
        # 测试VTS连接状态
        print("🔌 检查VTS连接状态...")
        try:
            # 简单的VTS状态检查
            print(f"   VTS连接: {'✅ 已连接' if hasattr(vts_integration, 'is_connected') and vts_integration.is_connected else '⚪ 未连接'}")
        except Exception as e:
            print(f"   VTS检查: ❌ 错误 - {e}")
        
        print("✅ 诊断完成\n")
    
    def show_stats(self):
        """显示统计信息"""
        print(f"\n📊 直播间统计信息:")
        print(f"   会话ID: {self.session_id}")
        print(f"   消息数量: {self.message_counter}")
        print(f"   运行时间: {int(time.time() - int(self.session_id.split('_')[-1]))} 秒")
        print(f"   VTS状态: {'已连接' if hasattr(vts_integration, 'is_connected') and vts_integration.is_connected else '未连接'}")
        print()
    
    async def shutdown(self):
        """关闭系统"""
        print("\n👋 正在关闭直播间...")
        self.is_running = False
        
        # 尝试断开VTS连接
        try:
            if hasattr(vts_integration, 'is_connected') and vts_integration.is_connected:
                # 注意：pyvts可能没有disconnect方法
                print("🔌 VTS连接已保持（如需完全断开请重启VTS）")
        except Exception as e:
            print(f"ℹ️  VTS断开提示: {e}")
        
        print("✅ 直播间已关闭")
        print("=" * 60)

async def main():
    """主函数"""
    simulator = LiveChatSimulator()
    
    try:
        # 初始化系统
        await simulator.initialize_system()
        
        # 启动聊天循环
        simulator.is_running = True
        await simulator.handle_user_input()
        
    except Exception as e:
        print(f"❌ 系统错误: {e}")
    finally:
        await simulator.shutdown()

if __name__ == "__main__":
    print("🚀 启动虚拟主播直播间模拟器...")
    asyncio.run(main())