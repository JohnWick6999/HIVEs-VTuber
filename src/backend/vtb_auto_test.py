#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VTB角色自动动作测试
让角色执行一系列预设动作
"""

import asyncio
import json
import websockets
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class AutoVTBTester:
    """自动VTB测试器"""
    
    def __init__(self):
        self.websocket = None
        self.is_authenticated = False
        
    async def connect_and_authenticate(self):
        """连接并认证"""
        try:
            logger.info("正在连接VTube Studio...")
            self.websocket = await websockets.connect("ws://localhost:8001")
            logger.info("✅ 已连接到VTube Studio")
            
            # 发送认证请求
            auth_request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "auto_test_auth",
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": "AutoVTBTester",
                    "pluginDeveloper": "TestUser"
                }
            }
            
            await self.websocket.send(json.dumps(auth_request))
            logger.info("🔑 认证请求已发送，请在VTube Studio中确认授权...")
            
            # 等待认证响应
            response = await self.websocket.recv()
            response_data = json.loads(response)
            logger.info(f"收到响应: {response_data}")
            
            if response_data.get('messageType') == 'AuthenticationTokenResponse':
                self.is_authenticated = True
                logger.info("✅ 认证成功！")
                return True
            else:
                logger.error("❌ 认证失败")
                return False
                
        except Exception as e:
            logger.error(f"连接失败: {e}")
            return False
    
    async def trigger_action(self, action_name, delay=1.5):
        """触发单个动作"""
        if not self.is_authenticated:
            logger.warning("未认证，无法执行动作")
            return False
            
        try:
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": f"action_{action_name}_{int(time.time())}",
                "messageType": "HotkeyTriggerRequest",
                "data": {
                    "hotkeyName": action_name
                }
            }
            
            await self.websocket.send(json.dumps(request))
            logger.info(f"🎬 执行动作: {action_name}")
            
            # 等待响应
            response = await self.websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get('messageType') == 'HotkeyTriggerResponse':
                logger.info(f"✅ 动作 {action_name} 执行成功")
                await asyncio.sleep(delay)  # 等待动作完成
                return True
            else:
                logger.warning(f"⚠️ 动作 {action_name} 执行可能失败")
                await asyncio.sleep(delay)
                return False
                
        except Exception as e:
            logger.error(f"执行动作 {action_name} 失败: {e}")
            await asyncio.sleep(delay)
            return False
    
    async def run_test_sequence(self):
        """运行测试序列"""
        if not await self.connect_and_authenticate():
            return
        
        # 测试动作序列
        test_actions = [
            ("Wave", "👋 挥手打招呼"),
            ("Happy", "😊 开心表情"),
            ("Nod", "👍 点头确认"),
            ("Clap", "👏 鼓掌庆祝"),
            ("Surprise", "😲 惊讶表情"),
            ("Shy", "😳 害羞表情"),
            ("Angry", "😠 生气表情"),
            ("Heart", "💕 比心爱心"),
            ("Jump", "🦘 跳跃动作")
        ]
        
        logger.info("=" * 50)
        logger.info("🚀 开始VTB角色动作测试序列")
        logger.info("=" * 50)
        
        success_count = 0
        total_actions = len(test_actions)
        
        for i, (action, description) in enumerate(test_actions, 1):
            logger.info(f"\n[{i}/{total_actions}] {description}")
            
            if await self.trigger_action(action):
                success_count += 1
                logger.info(f"✅ 完成 {i}/{total_actions}")
            else:
                logger.info(f"❌ 跳过 {i}/{total_actions}")
            
            # 在动作间稍作停顿
            if i < total_actions:
                await asyncio.sleep(2)
        
        logger.info("=" * 50)
        logger.info(f"📊 测试完成! 成功执行 {success_count}/{total_actions} 个动作")
        logger.info("=" * 50)
        
        # 断开连接
        if self.websocket:
            await self.websocket.close()
            logger.info("🔌 已断开连接")

async def interactive_mode():
    """交互模式"""
    tester = AutoVTBTester()
    
    if not await tester.connect_and_authenticate():
        return
    
    print("\n" + "="*50)
    print("🎮 VTB角色交互控制模式")
    print("="*50)
    print("可用命令:")
    print("test - 运行完整测试序列")
    print("wave, happy, clap, nod, surprise, shy, angry, heart, jump - 单个动作")
    print("quit - 退出程序")
    print("="*50)
    
    try:
        while True:
            command = input("\n请输入命令: ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'test':
                await tester.run_test_sequence()
                break
            elif command in ['wave', 'happy', 'clap', 'nod', 'surprise', 'shy', 'angry', 'heart', 'jump']:
                action_name = command.capitalize()
                await tester.trigger_action(action_name, delay=2.0)
            else:
                print("❌ 未知命令，请重新输入")
                
    except KeyboardInterrupt:
        print("\n\n程序被中断")
    finally:
        if tester.websocket:
            await tester.websocket.close()
            print("🔌 已断开连接")

if __name__ == "__main__":
    print("VTB角色动作测试器")
    print("选择模式:")
    print("1. 自动测试模式 (执行预设动作序列)")
    print("2. 交互控制模式 (手动控制动作)")
    
    choice = input("请选择模式 (1/2): ").strip()
    
    if choice == "1":
        asyncio.run(AutoVTBTester().run_test_sequence())
    elif choice == "2":
        asyncio.run(interactive_mode())
    else:
        print("无效选择，运行自动测试模式")
        asyncio.run(AutoVTBTester().run_test_sequence())