#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VTB综合控制面板
集成动作控制和面部追踪
"""

import asyncio
import json
import websockets
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class VTBControlPanel:
    """VTB综合控制面板"""
    
    def __init__(self):
        self.websocket = None
        self.is_authenticated = False
        
    async def connect(self):
        """连接VTube Studio"""
        try:
            logger.info("正在连接VTube Studio...")
            self.websocket = await websockets.connect("ws://localhost:8001")
            
            auth_request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "control_panel_auth",
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": "VTBControlPanel",
                    "pluginDeveloper": "ComprehensiveControl"
                }
            }
            
            await self.websocket.send(json.dumps(auth_request))
            response = await self.websocket.recv()
            
            if json.loads(response).get('messageType') == 'AuthenticationTokenResponse':
                self.is_authenticated = True
                logger.info("✅ 控制面板连接成功")
                return True
            return False
            
        except Exception as e:
            logger.error(f"连接失败: {e}")
            return False
    
    async def trigger_hotkey(self, hotkey_name: str):
        """触发热键动作"""
        if not self.is_authenticated:
            return False
            
        try:
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": f"hotkey_{hotkey_name}",
                "messageType": "HotkeyTriggerRequest",
                "data": {
                    "hotkeyName": hotkey_name
                }
            }
            
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            
            if json.loads(response).get('messageType') == 'HotkeyTriggerResponse':
                logger.info(f"🎬 执行动作: {hotkey_name}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"动作执行失败: {e}")
            return False
    
    async def set_parameter(self, param_name: str, value: float, weight: float = 1.0):
        """设置面部参数"""
        if not self.is_authenticated:
            return False
            
        try:
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": f"param_{param_name}",
                "messageType": "InjectParameterDataRequest",
                "data": {
                    "parameterValues": [{
                        "id": param_name,
                        "value": value,
                        "weight": weight
                    }]
                }
            }
            
            await self.websocket.send(json.dumps(request))
            await self.websocket.recv()
            logger.info(f"🎭 设置面部参数: {param_name} = {value}")
            return True
            
        except Exception as e:
            logger.error(f"参数设置失败: {e}")
            return False
    
    async def run_comprehensive_demo(self):
        """运行综合演示"""
        if not await self.connect():
            return
        
        logger.info("=" * 60)
        logger.info("🎮 VTB综合控制演示开始")
        logger.info("=" * 60)
        
        # 1. 动作演示
        logger.info("\n🤖 动作控制演示:")
        actions = [
            ("Wave", "👋 挥手打招呼"),
            ("Happy", "😊 开心表情"),
            ("Nod", "👍 点头确认")
        ]
        
        for action, desc in actions:
            logger.info(f"  {desc}")
            await self.trigger_hotkey(action)
            await asyncio.sleep(2)
        
        # 2. 面部表情演示
        logger.info("\n🎭 面部表情演示:")
        expressions = [
            ("MouthSmile", 1.0, "😊 微笑"),
            ("MouthOpen", 0.8, "😮 张嘴惊讶"),
            ("EyesClosed", 1.0, "😴 闭眼休息")
        ]
        
        for param, value, desc in expressions:
            logger.info(f"  {desc}")
            await self.set_parameter(param, value)
            await asyncio.sleep(2)
            await self.set_parameter(param, 0.0)  # 恢复
            await asyncio.sleep(1)
        
        # 3. 组合演示
        logger.info("\n🎪 综合表演:")
        performance = [
            # 挥手 + 微笑
            [("Wave", None), ("MouthSmile", 1.0)],
            # 鼓掌 + 张嘴
            [("Clap", None), ("MouthOpen", 0.8)],
            # 点头 + 闭眼
            [("Nod", None), ("EyesClosed", 1.0)]
        ]
        
        for combo_actions in performance:
            for action, value in combo_actions:
                if value is None:
                    await self.trigger_hotkey(action)
                else:
                    await self.set_parameter(action, value)
            await asyncio.sleep(3)
            
            # 恢复状态
            for action, value in combo_actions:
                if value is not None:
                    await self.set_parameter(action, 0.0)
            await asyncio.sleep(1)
        
        logger.info("=" * 60)
        logger.info("🎉 综合演示完成!")
        logger.info("=" * 60)
        
        if self.websocket:
            await self.websocket.close()

async def main():
    """主函数"""
    panel = VTBControlPanel()
    
    print("🎮 VTB综合控制面板")
    print("功能:")
    print("1. 动作控制 (挥手、鼓掌、点头等)")
    print("2. 面部表情 (微笑、张嘴、闭眼等)")
    print("3. 综合表演 (动作+表情组合)")
    print()
    
    choice = input("是否运行综合演示? (y/n): ").strip().lower()
    
    if choice == 'y':
        await panel.run_comprehensive_demo()
    else:
        print("程序退出")

if __name__ == "__main__":
    asyncio.run(main())