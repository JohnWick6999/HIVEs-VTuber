#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VTB角色动作控制 - 最简版本
直接使用WebSocket连接VTube Studio
"""

import asyncio
import json
import websockets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleVTBController:
    """简化版VTB控制器"""
    
    def __init__(self):
        self.websocket = None
        self.token = None
        
    async def connect(self):
        """连接到VTube Studio"""
        try:
            self.websocket = await websockets.connect("ws://localhost:8001")
            logger.info("✅ 连接到VTube Studio")
            
            # 认证
            auth_request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "auth_request",
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": "SimpleVTBController",
                    "pluginDeveloper": "User"
                }
            }
            
            await self.websocket.send(json.dumps(auth_request))
            response = await self.websocket.recv()
            logger.info("认证请求已发送，请在VTube Studio中确认授权")
            
            return True
        except Exception as e:
            logger.error(f"连接失败: {e}")
            return False
    
    async def trigger_hotkey(self, hotkey_name):
        """触发热键"""
        if not self.websocket:
            logger.warning("未连接")
            return
            
        request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0", 
            "requestID": f"hotkey_{hotkey_name}",
            "messageType": "HotkeyTriggerRequest",
            "data": {
                "hotkeyName": hotkey_name
            }
        }
        
        try:
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            logger.info(f"触发动作: {hotkey_name}")
        except Exception as e:
            logger.error(f"触发失败: {e}")

async def main():
    """主函数"""
    controller = SimpleVTBController()
    
    if not await controller.connect():
        return
    
    print("VTB动作控制器 - 最简版")
    print("输入动作名称来控制角色，输入'quit'退出")
    print("示例动作: Wave, Happy, Clap, Nod, Surprise")
    
    try:
        while True:
            action = input("> ").strip()
            if action.lower() == 'quit':
                break
            elif action:
                await controller.trigger_hotkey(action)
    except KeyboardInterrupt:
        pass
    finally:
        if controller.websocket:
            await controller.websocket.close()

if __name__ == "__main__":
    asyncio.run(main())