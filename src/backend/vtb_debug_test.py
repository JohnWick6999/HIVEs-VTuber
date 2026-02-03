#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VTB角色动作诊断测试
先获取可用热键，再执行动作
"""

import asyncio
import json
import websockets
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class VTBDebugger:
    """VTB调试器"""
    
    def __init__(self):
        self.websocket = None
        self.token = None
        
    async def connect_and_setup(self):
        """连接并设置"""
        try:
            logger.info("正在连接VTube Studio...")
            self.websocket = await websockets.connect("ws://localhost:8001")
            logger.info("✅ 已连接")
            
            # 认证
            auth_req = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "debug_auth",
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": "VTBDebugger",
                    "pluginDeveloper": "DebugUser"
                }
            }
            
            await self.websocket.send(json.dumps(auth_req))
            response = await self.websocket.recv()
            data = json.loads(response)
            
            if data.get('messageType') == 'AuthenticationTokenResponse':
                self.token = data['data']['authenticationToken']
                logger.info("✅ 认证成功")
                return True
            else:
                logger.error("❌ 认证失败")
                return False
                
        except Exception as e:
            logger.error(f"连接失败: {e}")
            return False
    
    async def get_hotkeys(self):
        """获取可用热键"""
        if not self.websocket:
            return []
            
        try:
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "get_hotkeys",
                "messageType": "HotkeysInCurrentModelRequest",
                "data": {}
            }
            
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            data = json.loads(response)
            
            if data.get('messageType') == 'HotkeysInCurrentModelResponse':
                hotkeys = data['data'].get('availableHotkeys', [])
                logger.info(f"🔍 发现 {len(hotkeys)} 个可用热键:")
                for i, hk in enumerate(hotkeys[:15]):  # 显示前15个
                    logger.info(f"  {i+1}. {hk['name']} (ID: {hk['hotkeyID']})")
                return hotkeys
            else:
                logger.error("获取热键列表失败")
                return []
                
        except Exception as e:
            logger.error(f"获取热键失败: {e}")
            return []
    
    async def execute_hotkey_by_id(self, hotkey_id, name="Unknown"):
        """通过ID执行热键"""
        try:
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": f"execute_{hotkey_id}",
                "messageType": "HotkeyTriggerRequest",
                "data": {
                    "hotkeyID": hotkey_id
                }
            }
            
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            data = json.loads(response)
            
            if data.get('messageType') == 'HotkeyTriggerResponse':
                logger.info(f"✅ 成功执行: {name}")
                return True
            else:
                logger.warning(f"⚠️ 执行可能失败: {name}")
                return False
                
        except Exception as e:
            logger.error(f"执行失败 {name}: {e}")
            return False
    
    async def run_detailed_test(self):
        """运行详细测试"""
        if not await self.connect_and_setup():
            return
        
        # 获取热键列表
        hotkeys = await self.get_hotkeys()
        
        if not hotkeys:
            logger.error("❌ 没有找到可用的热键")
            return
        
        logger.info("=" * 50)
        logger.info("🎯 开始详细动作测试")
        logger.info("=" * 50)
        
        # 测试前几个热键
        test_count = min(8, len(hotkeys))
        success_count = 0
        
        for i in range(test_count):
            hotkey = hotkeys[i]
            name = hotkey['name']
            hotkey_id = hotkey['hotkeyID']
            
            logger.info(f"\n[{i+1}/{test_count}] 测试: {name}")
            
            if await self.execute_hotkey_by_id(hotkey_id, name):
                success_count += 1
                await asyncio.sleep(2)  # 等待动作完成
            else:
                await asyncio.sleep(1)
        
        logger.info("=" * 50)
        logger.info(f"📊 测试结果: {success_count}/{test_count} 个动作成功执行")
        logger.info("=" * 50)
        
        if self.websocket:
            await self.websocket.close()

async def main():
    """主函数"""
    debugger = VTBDebugger()
    await debugger.run_detailed_test()

if __name__ == "__main__":
    asyncio.run(main())