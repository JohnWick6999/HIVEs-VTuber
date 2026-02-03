#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用现成pyvts库的VTB控制方案
直接使用官方推荐的Python库
"""

import pyvts
import asyncio
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class ReadyToUseVTBController:
    """现成方案的VTB控制器"""
    
    def __init__(self):
        self.vts = None
        
    async def connect(self):
        """连接VTube Studio"""
        try:
            logger.info("正在连接VTube Studio...")
            self.vts = pyvts.vts()
            await self.vts.connect()
            logger.info("✅ 成功连接到VTube Studio")
            return True
        except Exception as e:
            logger.error(f"❌ 连接失败: {e}")
            return False
    
    async def disconnect(self):
        """断开连接"""
        if self.vts:
            await self.vts.close()
            logger.info("已断开连接")
    
    async def get_hotkeys(self):
        """获取可用热键"""
        try:
            hotkeys = await self.vts.request(self.vts.api.HotkeysInCurrentModelRequest())
            available = hotkeys.get('data', {}).get('availableHotkeys', [])
            logger.info(f"发现 {len(available)} 个可用热键:")
            for hk in available[:10]:  # 显示前10个
                logger.info(f"  - {hk['name']} (ID: {hk['hotkeyID']})")
            return available
        except Exception as e:
            logger.error(f"获取热键失败: {e}")
            return []
    
    async def trigger_hotkey(self, hotkey_name_or_id):
        """触发热键"""
        try:
            # 如果是名称，先转换为ID
            if isinstance(hotkey_name_or_id, str) and not hotkey_name_or_id.startswith('hotkey_'):
                # 获取热键列表找到对应ID
                hotkeys = await self.get_hotkeys()
                for hk in hotkeys:
                    if hk['name'] == hotkey_name_or_id:
                        hotkey_name_or_id = hk['hotkeyID']
                        break
            
            response = await self.vts.request(
                self.vts.api.HotkeyTriggerRequest(hotkeyID=hotkey_name_or_id)
            )
            logger.info(f"✅ 触发热键: {hotkey_name_or_id}")
            return True
        except Exception as e:
            logger.error(f"❌ 触发热键失败: {e}")
            return False
    
    async def simple_demo(self):
        """简单演示"""
        if not await self.connect():
            return
        
        try:
            # 获取热键
            hotkeys = await self.get_hotkeys()
            
            if hotkeys:
                # 触发前3个热键作为演示
                for i, hk in enumerate(hotkeys[:3]):
                    logger.info(f"\n🎬 演示动作 {i+1}: {hk['name']}")
                    await self.trigger_hotkey(hk['hotkeyID'])
                    await asyncio.sleep(2)
            
            logger.info("🎉 演示完成!")
            
        finally:
            await self.disconnect()

async def interactive_mode():
    """交互模式"""
    controller = ReadyToUseVTBController()
    
    if not await controller.connect():
        return
    
    try:
        print("\n" + "="*50)
        print("🎮 VTB现成方案控制面板")
        print("="*50)
        print("命令:")
        print("list - 显示可用热键")
        print("热键名称 - 触发热键")
        print("demo - 运行简单演示")
        print("quit - 退出")
        print("="*50)
        
        while True:
            command = input("\n> ").strip()
            
            if command.lower() == 'quit':
                break
            elif command.lower() == 'list':
                await controller.get_hotkeys()
            elif command.lower() == 'demo':
                await controller.simple_demo()
            elif command:
                await controller.trigger_hotkey(command)
                
    except KeyboardInterrupt:
        print("\n程序被中断")
    finally:
        await controller.disconnect()

if __name__ == "__main__":
    print("VTB现成方案控制器 (基于pyvts)")
    print("1. 简单演示")
    print("2. 交互控制")
    
    choice = input("请选择模式 (1/2): ").strip()
    
    if choice == "1":
        asyncio.run(ReadyToUseVTBController().simple_demo())
    elif choice == "2":
        asyncio.run(interactive_mode())
    else:
        print("运行简单演示...")
        asyncio.run(ReadyToUseVTBController().simple_demo())