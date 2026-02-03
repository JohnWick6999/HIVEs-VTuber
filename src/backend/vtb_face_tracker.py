#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VTB面部捕捉控制
通过API控制面部追踪参数
"""

import asyncio
import json
import websockets
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class FaceTrackingController:
    """面部追踪控制器"""
    
    def __init__(self):
        self.websocket = None
        self.is_authenticated = False
        
    async def connect_and_auth(self):
        """连接并认证"""
        try:
            logger.info("正在连接VTube Studio...")
            self.websocket = await websockets.connect("ws://localhost:8001")
            logger.info("✅ 已连接")
            
            auth_request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "face_track_auth",
                "messageType": "AuthenticationTokenRequest",
                "data": {
                    "pluginName": "FaceTracker",
                    "pluginDeveloper": "VTBDev"
                }
            }
            
            await self.websocket.send(json.dumps(auth_request))
            response = await self.websocket.recv()
            data = json.loads(response)
            
            if data.get('messageType') == 'AuthenticationTokenResponse':
                self.is_authenticated = True
                logger.info("✅ 面捕控制器认证成功")
                return True
            else:
                logger.error("❌ 认证失败")
                return False
                
        except Exception as e:
            logger.error(f"连接失败: {e}")
            return False
    
    async def get_tracking_parameters(self):
        """获取当前追踪参数"""
        if not self.is_authenticated:
            return {}
            
        try:
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "get_params",
                "messageType": "InputParameterListRequest",
                "data": {}
            }
            
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            data = json.loads(response)
            
            if data.get('messageType') == 'InputParameterListResponse':
                parameters = data['data'].get('modelParameters', [])
                logger.info(f"🔍 检测到 {len(parameters)} 个面部参数:")
                for param in parameters[:10]:  # 显示前10个
                    logger.info(f"  - {param['name']}: {param['addedBy']}")
                return parameters
            return {}
            
        except Exception as e:
            logger.error(f"获取参数失败: {e}")
            return {}
    
    async def set_face_parameter(self, param_name: str, value: float, weight: float = 1.0):
        """设置面部参数"""
        if not self.is_authenticated:
            return False
            
        try:
            request = {
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": f"set_param_{param_name}",
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
                logger.info(f"✅ 设置参数 {param_name} = {value}")
                return True
            else:
                logger.warning(f"⚠️ 设置参数可能失败: {param_name}")
                return False
                
        except Exception as e:
            logger.error(f"设置参数失败 {param_name}: {e}")
            return False
    
    async def face_expression_test(self):
        """面部表情测试"""
        if not await self.connect_and_auth():
            return
        
        # 获取可用参数
        parameters = await self.get_tracking_parameters()
        
        # 常见面部输出参数（这才是要控制的！）
        face_params = {
            "ParamAngleX": "头部左右转动",
            "ParamAngleY": "头部上下转动", 
            "ParamAngleZ": "头部倾斜",
            "ParamEyeLOpen": "左眼睁闭",
            "ParamEyeROpen": "右眼睁闭",
            "ParamEyeBallX": "眼球左右",
            "ParamEyeBallY": "眼球上下",
            "ParamMouthOpenY": "嘴巴张开",
            "ParamMouthForm": "嘴巴形状",
            "ParamBodyAngleX": "身体左右倾斜",
            "ParamBreath": "呼吸动画"
        }
        
        logger.info("=" * 50)
        logger.info("🎭 开始面部表情测试")
        logger.info("=" * 50)
        
        # 测试基本表情 - 控制正确的输出参数
        expressions = [
            ("ParamAngleX", 20.0, "👉 头部右转"),
            ("ParamAngleX", -20.0, "👈 头部左转"),
            ("ParamAngleX", 0.0, "😐 头部回正"),
            ("ParamAngleY", 15.0, "👆 抬头"),
            ("ParamAngleY", -15.0, "👇 低头"),
            ("ParamAngleY", 0.0, "😐 头部水平"),
            ("ParamMouthOpenY", 1.0, "😮 张大嘴"),
            ("ParamMouthOpenY", 0.0, "🙂 闭嘴"),
            ("ParamEyeLOpen", 0.0, "😴 闭左眼"),
            ("ParamEyeLOpen", 1.0, "👁 睁左眼"),
            ("ParamEyeROpen", 0.0, "😴 闭右眼"),
            ("ParamEyeROpen", 1.0, "👁 睁右眼")
        ]
        
        for param, value, desc in expressions:
            logger.info(f"\n🎬 {desc}")
            await self.set_face_parameter(param, value, 1.0)
            await asyncio.sleep(2)  # 保持2秒
            
            # 恢复中性状态
            await self.set_face_parameter(param, 0.0, 1.0)
            await asyncio.sleep(1)
        
        logger.info("=" * 50)
        logger.info("✅ 面部表情测试完成")
        logger.info("=" * 50)
        
        if self.websocket:
            await self.websocket.close()

async def interactive_face_control():
    """交互式面部控制"""
    controller = FaceTrackingController()
    
    if not await controller.connect_and_auth():
        return
    
    print("\n" + "="*50)
    print("🎭 VTB面部追踪交互控制")
    print("="*50)
    print("命令格式: 参数名 数值 [权重]")
    print("示例: ParamAngleX 20.0 1.0")
    print("常用参数: ParamAngleX, ParamAngleY, ParamMouthOpenY, ParamEyeLOpen, ParamEyeROpen")
    print("输入 'test' 运行预设测试")
    print("输入 'quit' 退出")
    print("="*50)
    
    try:
        while True:
            command = input("\n.face> ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'test':
                await controller.face_expression_test()
            elif command:
                parts = command.split()
                if len(parts) >= 2:
                    param_name = parts[0]
                    try:
                        value = float(parts[1])
                        weight = float(parts[2]) if len(parts) > 2 else 1.0
                        await controller.set_face_parameter(param_name, value, weight)
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
    print("VTB面部追踪控制器")
    print("选择模式:")
    print("1. 自动表情测试")
    print("2. 交互式控制")
    
    choice = input("请选择模式 (1/2): ").strip()
    
    if choice == "1":
        asyncio.run(FaceTrackingController().face_expression_test())
    elif choice == "2":
        asyncio.run(interactive_face_control())
    else:
        print("无效选择，运行自动测试")
        asyncio.run(FaceTrackingController().face_expression_test())