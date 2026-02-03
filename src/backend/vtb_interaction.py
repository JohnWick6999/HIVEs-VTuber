#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VTB互动场景控制器 - 简化版
"""

import asyncio
import logging
from vtb_motion_control import SimpleVTBMotionController

logger = logging.getLogger(__name__)

class VTBInteractionController:
    """VTB互动场景控制器"""
    
    def __init__(self):
        self.controller = SimpleVTBMotionController()
        self.is_ready = False
    
    async def initialize(self) -> bool:
        """初始化控制器"""
        if await self.controller.connect():
            await self.controller.get_available_hotkeys()
            self.is_ready = True
            logger.info("✅ VTB控制器初始化完成")
            return True
        return False
    
    async def cleanup(self):
        """清理资源"""
        await self.controller.disconnect()
        self.is_ready = False
    
    async def run_interaction(self, interaction_type: str):
        """执行互动"""
        if not self.is_ready:
            return False
            
        interactions = {
            'greeting': ['Wave', 'Happy', 'Nod'],
            'celebrate': ['Clap', 'Jump', 'Heart'],
            'surprise': ['Surprised', 'ShakeHead'],
            'shy': ['Shy', 'Nod'],
            'angry': ['Angry', 'ShakeHead']
        }
        
        if interaction_type in interactions:
            logger.info(f"🎬 执行互动: {interaction_type}")
            for action in interactions[interaction_type]:
                await self.controller.trigger_hotkey_by_name(action)
                await asyncio.sleep(1)
            return True
        return False

async def main():
    """主函数"""
    controller = VTBInteractionController()
    
    if not await controller.initialize():
        print("❌ 初始化失败")
        return
    
    try:
        print("VTB互动控制器")
        print("可用命令: greeting, celebrate, surprise, shy, angry, quit")
        
        while True:
            command = input("> ").strip().lower()
            if command == 'quit':
                break
            elif command:
                await controller.run_interaction(command)
                
    except KeyboardInterrupt:
        pass
    finally:
        await controller.cleanup()

if __name__ == "__main__":
    asyncio.run(main())