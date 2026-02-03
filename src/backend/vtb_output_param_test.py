#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VTB输出参数控制测试
专门测试Param开头的正确输出参数
"""

import asyncio
import json
import websockets
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class OutputParamController:
    """输出参数控制器"""
    
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
                "requestID": "output_param_test",
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": "OutputParamController",
                    "pluginDeveloper": "ParamTest"
                }
            }
            
            await self.websocket.send(json.dumps(auth_request))
            response = await self.websocket.recv()
            
            if json.loads(response).get('messageType') == 'AuthenticationTokenResponse':
                self.is_authenticated = True
                logger.info("✅ 输出参数控制器认证成功")
                return True
            return False
            
        except Exception as e:
            logger.error(f"连接失败: {e}")
            return False
    
    async def set_output_parameter(self, param_name: str, value: float, weight: float = 1.0):
        """设置输出参数"""
        if not self.is_authenticated:
            return False
            
        try:
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": f"set_output_{param_name}",
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
            response = await self.websocket.recv()
            
            if json.loads(response).get('messageType') == 'InjectParameterDataResponse':
                logger.info(f"✅ 设置输出参数 {param_name} = {value}")
                return True
            else:
                logger.warning(f"⚠️ 设置输出参数可能失败: {param_name}")
                return False
                
        except Exception as e:
            logger.error(f"设置输出参数失败 {param_name}: {e}")
            return False
    
    async def head_movement_demo(self):
        """头部运动演示"""
        if not await self.connect():
            return
        
        logger.info("=" * 60)
        logger.info("🤖 头部运动控制演示")
        logger.info("=" * 60)
        
        movements = [
            ("ParamAngleX", 30.0, "👉 头部右转30度"),
            ("ParamAngleX", 0.0, "😐 头部回正"),
            ("ParamAngleX", -30.0, "👈 头部左转30度"),
            ("ParamAngleX", 0.0, "😐 头部回正"),
            ("ParamAngleY", 20.0, "👆 抬头20度"),
            ("ParamAngleY", 0.0, "😐 头部水平"),
            ("ParamAngleY", -20.0, "👇 低头20度"),
            ("ParamAngleY", 0.0, "😐 头部回正"),
            ("ParamAngleZ", 15.0, "🌀 头部右倾15度"),
            ("ParamAngleZ", 0.0, "😐 头部端正")
        ]
        
        for param, value, desc in movements:
            logger.info(f"\n🎬 {desc}")
            await self.set_output_parameter(param, value, 1.0)
            await asyncio.sleep(2)
        
        logger.info("=" * 60)
        logger.info("✅ 头部运动演示完成")
        logger.info("=" * 60)
        
        if self.websocket:
            await self.websocket.close()
    
    async def facial_expression_demo(self):
        """面部表情演示"""
        if not await self.connect():
            return
        
        logger.info("=" * 60)
        logger.info("🎭 面部表情控制演示")
        logger.info("=" * 60)
        
        expressions = [
            ("ParamMouthOpenY", 1.0, "😮 大张嘴"),
            ("ParamMouthOpenY", 0.5, "😯 半张嘴"),
            ("ParamMouthOpenY", 0.0, "🙂 闭嘴"),
            ("ParamEyeLOpen", 0.0, "😴 闭左眼"),
            ("ParamEyeLOpen", 1.0, "👁 睁左眼"),
            ("ParamEyeROpen", 0.0, "😴 闭右眼"),
            ("ParamEyeROpen", 1.0, "👁 睁右眼"),
            ("ParamEyeBallX", 1.0, "👀 眼球右转"),
            ("ParamEyeBallX", -1.0, "👀 眼球左转"),
            ("ParamEyeBallX", 0.0, "👀 眼球回正")
        ]
        
        for param, value, desc in expressions:
            logger.info(f"\n🎬 {desc}")
            await self.set_output_parameter(param, value, 1.0)
            await asyncio.sleep(1.5)
        
        # 恢复所有参数到默认状态
        logger.info("\n🔄 恢复默认状态...")
        reset_params = ["ParamMouthOpenY", "ParamEyeLOpen", "ParamEyeROpen", "ParamEyeBallX"]
        for param in reset_params:
            await self.set_output_parameter(param, 0.0 if param != "ParamEyeLOpen" and param != "ParamEyeROpen" else 1.0, 1.0)
        
        logger.info("=" * 60)
        logger.info("✅ 面部表情演示完成")
        logger.info("=" * 60)
        
        if self.websocket:
            await self.websocket.close()
    
    async def full_body_demo(self):
        """全身动作演示"""
        if not await self.connect():
            return
        
        logger.info("=" * 60)
        logger.info("💃 全身动作控制演示")
        logger.info("=" * 60)
        
        body_movements = [
            ("ParamBodyAngleX", 10.0, "💃 身体右倾"),
            ("ParamBodyAngleX", 0.0, "🕺 身体回正"),
            ("ParamBodyAngleX", -10.0, "💃 身体左倾"),
            ("ParamBodyAngleX", 0.0, "🕺 身体回正"),
            ("ParamBreath", 1.0, "💨 深呼吸"),
            ("ParamBreath", 0.0, "😌 呼吸平稳")
        ]
        
        for param, value, desc in body_movements:
            logger.info(f"\n🎬 {desc}")
            await self.set_output_parameter(param, value, 1.0)
            await asyncio.sleep(2)
        
        logger.info("=" * 60)
        logger.info("✅ 全身动作演示完成")
        logger.info("=" * 60)
        
        if self.websocket:
            await self.websocket.close()

async def interactive_output_control():
    """交互式输出参数控制"""
    controller = OutputParamController()
    
    if not await controller.connect():
        return
    
    print("\n" + "="*60)
    print("🎮 VTB输出参数交互控制")
    print("="*60)
    print("重要提醒：请先在VTube Studio中关闭对应参数的输入绑定！")
    print()
    print("常用命令:")
    print("head - 头部运动演示")
    print("face - 面部表情演示") 
    print("body - 全身动作演示")
    print("参数名 数值 - 直接设置参数 (如: ParamAngleX 25.0)")
    print("quit - 退出")
    print()
    print("常用输出参数:")
    print("• ParamAngleX - 头部左右转动 (-30到30度)")
    print("• ParamAngleY - 头部上下转动 (-30到30度)")
    print("• ParamMouthOpenY - 嘴巴张开 (0.0到1.0)")
    print("• ParamEyeLOpen - 左眼睁闭 (0.0到1.0)")
    print("• ParamEyeROpen - 右眼睁闭 (0.0到1.0)")
    print("="*60)
    
    try:
        while True:
            command = input("\n.param> ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'head':
                await controller.head_movement_demo()
            elif command == 'face':
                await controller.facial_expression_demo()
            elif command == 'body':
                await controller.full_body_demo()
            elif command:
                parts = command.split()
                if len(parts) >= 2:
                    param_name = parts[0]
                    try:
                        value = float(parts[1])
                        weight = float(parts[2]) if len(parts) > 2 else 1.0
                        await controller.set_output_parameter(param_name, value, weight)
                    except ValueError:
                        print("❌ 数值格式错误")
                else:
                    print("❌ 命令格式: 参数名 数值 [权重]")
                    
    except KeyboardInterrupt:
        print("\n\n程序被中断")
    finally:
        if controller.websocket:
            await controller.websocket.close()

if __name__ == "__main__":
    print("VTB输出参数控制器")
    print("请选择模式:")
    print("1. 头部运动演示")
    print("2. 面部表情演示")
    print("3. 全身动作演示")
    print("4. 交互式控制")
    
    choice = input("请输入选择 (1-4): ").strip()
    
    controller = OutputParamController()
    
    if choice == "1":
        asyncio.run(controller.head_movement_demo())
    elif choice == "2":
        asyncio.run(controller.facial_expression_demo())
    elif choice == "3":
        asyncio.run(controller.full_body_demo())
    elif choice == "4":
        asyncio.run(interactive_output_control())
    else:
        print("无效选择，运行交互式控制")
        asyncio.run(interactive_output_control())