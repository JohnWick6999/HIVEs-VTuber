#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VTB角色动作控制 - 最简方案
直接通过VTube Studio API控制角色动作
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional
import pyvts

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vtb_motion.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimpleVTBMotionController:
    """简单的VTB动作控制器"""
    
    def __init__(self):
        self.vts = None
        self.is_connected = False
        self.hotkeys_cache = {}
        
    async def connect(self) -> bool:
        """连接到VTube Studio"""
        try:
            logger.info("正在连接VTube Studio...")
            self.vts = pyvts.vts()
            await self.vts.connect()
            self.is_connected = True
            logger.info("✅ 成功连接到VTube Studio")
            return True
        except Exception as e:
            logger.error(f"❌ 连接失败: {e}")
            return False
    
    async def disconnect(self):
        """断开连接"""
        if self.vts and self.is_connected:
            await self.vts.close()
            self.is_connected = False
            logger.info("已断开VTube Studio连接")
    
    async def get_available_hotkeys(self) -> List[Dict]:
        """获取可用的热键列表"""
        if not self.is_connected:
            logger.warning("未连接到VTube Studio")
            return []
        
        try:
            response = await self.vts.request({
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "hotkeys_request",
                "messageType": "HotkeysInCurrentModelRequest",
                "data": {}
            })
            
            hotkeys = response.get('data', {}).get('availableHotkeys', [])
            self.hotkeys_cache = {hk['name']: hk['hotkeyID'] for hk in hotkeys}
            
            logger.info(f"发现 {len(hotkeys)} 个可用热键:")
            for hotkey in hotkeys:
                logger.info(f"  - {hotkey['name']} (ID: {hotkey['hotkeyID']})")
                
            return hotkeys
        except Exception as e:
            logger.error(f"获取热键列表失败: {e}")
            return []
    
    async def trigger_hotkey_by_name(self, hotkey_name: str) -> bool:
        """通过名称触发热键"""
        if not self.is_connected:
            logger.warning("未连接到VTube Studio")
            return False
        
        # 如果缓存中有，直接使用
        if hotkey_name in self.hotkeys_cache:
            hotkey_id = self.hotkeys_cache[hotkey_name]
        else:
            # 否则重新获取列表
            await self.get_available_hotkeys()
            if hotkey_name not in self.hotkeys_cache:
                logger.warning(f"未找到热键: {hotkey_name}")
                return False
            hotkey_id = self.hotkeys_cache[hotkey_name]
        
        try:
            await self.vts.request(
                self.vts.api.HotkeyTriggerRequest(hotkeyID=hotkey_id)
            )
            logger.info(f"✅ 触发热键: {hotkey_name}")
            return True
        except Exception as e:
            logger.error(f"❌ 触发热键失败 {hotkey_name}: {e}")
            return False
    
    async def trigger_hotkey_by_id(self, hotkey_id: str) -> bool:
        """通过ID触发热键"""
        if not self.is_connected:
            logger.warning("未连接到VTube Studio")
            return False
        
        try:
            await self.vts.request(
                self.vts.api.HotkeyTriggerRequest(hotkeyID=hotkey_id)
            )
            logger.info(f"✅ 触发热键 ID: {hotkey_id}")
            return True
        except Exception as e:
            logger.error(f"❌ 触发热键失败 ID {hotkey_id}: {e}")
            return False
    
    async def move_model(self, x: float = 0, y: float = 0, rotation: float = 0, 
                        time_seconds: float = 1.0) -> bool:
        """移动模型位置"""
        if not self.is_connected:
            logger.warning("未连接到VTube Studio")
            return False
        
        try:
            await self.vts.request({
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "move_request",
                "messageType": "MoveModelRequest",
                "data": {
                    "timeInSeconds": time_seconds,
                    "valuesAreRelativeToModel": False,
                    "positionX": x,
                    "positionY": y,
                    "rotation": rotation
                }
            })
            logger.info(f"✅ 移动模型到位置 ({x}, {y}), 旋转 {rotation}°")
            return True
        except Exception as e:
            logger.error(f"❌ 移动模型失败: {e}")
            return False
    
    async def inject_parameter(self, param_id: str, value: float, weight: float = 1.0) -> bool:
        """注入参数值（控制面部表情等）"""
        if not self.is_connected:
            logger.warning("未连接到VTube Studio")
            return False
        
        try:
            await self.vts.request({
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "inject_request",
                "messageType": "InjectParameterDataRequest",
                "data": {
                    "parameterValues": [{
                        "id": param_id,
                        "value": value,
                        "weight": weight
                    }]
                }
            })
            logger.info(f"✅ 注入参数 {param_id} = {value}")
            return True
        except Exception as e:
            logger.error(f"❌ 注入参数失败: {e}")
            return False

# 预定义的常用动作
class VTBActions:
    """预定义的VTB动作集合"""
    
    # 基础表情动作
    EXPRESSIONS = {
        '开心': 'Happy',
        '悲伤': 'Sad',
        '生气': 'Angry',
        '惊讶': 'Surprised',
        '害羞': 'Shy',
        '困倦': 'Sleepy'
    }
    
    # 手势动作
    GESTURES = {
        '挥手': 'Wave',
        '鼓掌': 'Clap',
        '点赞': 'ThumbsUp',
        '比心': 'Heart',
        '打招呼': 'Greeting'
    }
    
    # 身体动作
    BODY_ACTIONS = {
        '点头': 'Nod',
        '摇头': 'ShakeHead',
        '跳跃': 'Jump',
        '转身': 'TurnAround'
    }

async def demo_basic_control():
    """演示基本控制功能"""
    controller = SimpleVTBMotionController()
    
    # 连接
    if not await controller.connect():
        return
    
    try:
        # 获取可用热键
        hotkeys = await controller.get_available_hotkeys()
        
        if hotkeys:
            # 演示触发第一个热键
            first_hotkey = hotkeys[0]
            await controller.trigger_hotkey_by_name(first_hotkey['name'])
            
            # 等待一下
            await asyncio.sleep(2)
            
            # 演示移动模型
            await controller.move_model(x=0.2, y=0.1, rotation=15, time_seconds=2.0)
            
            # 等待一下
            await asyncio.sleep(2)
            
            # 回到原位
            await controller.move_model(x=0, y=0, rotation=0, time_seconds=1.0)
        
    finally:
        await controller.disconnect()

async def interactive_control():
    """交互式控制"""
    controller = SimpleVTBMotionController()
    
    if not await controller.connect():
        return
    
    try:
        # 获取热键列表
        hotkeys = await controller.get_available_hotkeys()
        
        print("\n=== VTB动作控制器 ===")
        print("可用的热键动作:")
        for i, hotkey in enumerate(hotkeys[:10]):  # 显示前10个
            print(f"{i+1}. {hotkey['name']}")
        
        print("\n预定义动作:")
        print("E. 表情控制")
        print("G. 手势控制") 
        print("B. 身体动作")
        print("M. 模型移动")
        print("Q. 退出")
        
        while True:
            choice = input("\n请选择动作 (输入编号或字母): ").strip().upper()
            
            if choice == 'Q':
                break
            elif choice == 'E':
                print("表情:", list(VTBActions.EXPRESSIONS.keys()))
                expr = input("选择表情: ").strip()
                if expr in VTBActions.EXPRESSIONS:
                    await controller.trigger_hotkey_by_name(VTBActions.EXPRESSIONS[expr])
            elif choice == 'G':
                print("手势:", list(VTBActions.GESTURES.keys()))
                gesture = input("选择手势: ").strip()
                if gesture in VTBActions.GESTURES:
                    await controller.trigger_hotkey_by_name(VTBActions.GESTURES[gesture])
            elif choice == 'B':
                print("身体动作:", list(VTBActions.BODY_ACTIONS.keys()))
                body = input("选择动作: ").strip()
                if body in VTBActions.BODY_ACTIONS:
                    await controller.trigger_hotkey_by_name(VTBActions.BODY_ACTIONS[body])
            elif choice == 'M':
                try:
                    x = float(input("X坐标 (-1到1): ") or "0")
                    y = float(input("Y坐标 (-1到1): ") or "0")
                    rot = float(input("旋转角度 (-180到180): ") or "0")
                    await controller.move_model(x, y, rot, 1.0)
                except ValueError:
                    print("输入格式错误")
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(hotkeys):
                    await controller.trigger_hotkey_by_name(hotkeys[idx]['name'])
                else:
                    print("无效的选择")
            else:
                print("无效输入")
                
    finally:
        await controller.disconnect()

if __name__ == "__main__":
    print("VTB角色动作控制 - 最简方案")
    print("请选择模式:")
    print("1. 演示模式")
    print("2. 交互模式")
    
    mode = input("输入选择 (1/2): ").strip()
    
    if mode == "1":
        asyncio.run(demo_basic_control())
    elif mode == "2":
        asyncio.run(interactive_control())
    else:
        print("无效选择")