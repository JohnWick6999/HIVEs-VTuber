#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VTubeStudio连接专用测试脚本
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.backend.vts_integration import vts_integration
    VTS_AVAILABLE = True
    print("✅ VTS模块导入成功")
except ImportError as e:
    print(f"❌ VTS模块导入失败: {e}")
    VTS_AVAILABLE = False

async def test_vts_connection():
    """测试VTS连接"""
    if not VTS_AVAILABLE:
        print("❌ VTS控制器不可用")
        return False
    
    print("=" * 50)
    print("🔌 VTubeStudio 连接测试")
    print("=" * 50)
    
    try:
        print("🔄 正在连接到VTubeStudio...")
        print(f"   目标地址: ws://localhost:8001")
        
        connected = await vts_integration.connect()
        
        if connected:
            print("✅ VTS连接成功！")
            print("🎮 现在可以进行以下操作：")
            print("   1. 测试语音播放到VTS")
            print("   2. 测试口型同步")
            print("   3. 测试模型控制")
            return True
        else:
            print("❌ VTS连接失败")
            print("💡 请检查：")
            print("   • VTubeStudio是否正在运行")
            print("   • API服务器是否已启用")
            print("   • 端口8001是否可访问")
            return False
            
    except Exception as e:
        print(f"❌ 连接异常: {e}")
        return False

async def interactive_vts_test():
    """交互式VTS测试"""
    if not await test_vts_connection():
        return
    
    print("\n" + "=" * 50)
    print("🎮 交互式VTS测试模式")
    print("=" * 50)
    print("可用命令：")
    print("  speak <文本>  - 让虚拟主播说话")
    print("  test         - 运行完整测试")
    print("  quit         - 退出")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("👤 命令: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 退出VTS测试")
                break
                
            elif user_input.lower() == 'test':
                await run_full_test()
                
            elif user_input.startswith('speak '):
                text = user_input[6:].strip()
                if text:
                    print(f"🤖 虚拟主播: {text}")
                    success = vts_integration.text_to_speech_with_lip_sync(text)
                    if success:
                        print("✅ 语音播放成功")
                    else:
                        print("❌ 语音播放失败")
                else:
                    print("⚠️ 请输入要播放的文本")
            else:
                print("❓ 未知命令，请使用 'speak <文本>'、'test' 或 'quit'")
                
        except KeyboardInterrupt:
            print("\n👋 退出VTS测试")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

async def run_full_test():
    """运行完整测试"""
    print("\n🧪 运行完整VTS集成测试...")
    
    # 测试1: 语音生成
    print("1️⃣ 测试语音生成...")
    test_text = "大家好，我是虚拟主播，正在进行VTS集成测试！"
    success = vts_integration.text_to_speech_with_lip_sync(test_text, "vts_full_test.wav")
    print(f"   语音生成: {'✅ 成功' if success else '❌ 失败'}")
    
    # 测试2: VTS状态
    print("2️⃣ 检查VTS状态...")
    try:
        if hasattr(vts_integration, 'is_connected') and vts_integration.is_connected:
            print("   VTS连接: ✅ 已连接")
        else:
            print("   VTS连接: ⚪ 未连接")
    except Exception as e:
        print(f"   VTS状态检查: ❌ {e}")

if __name__ == "__main__":
    print("🚀 启动VTS连接测试...")
    asyncio.run(interactive_vts_test())