#!/usr/bin/env python3
# VTubeStudio集成功能测试

import asyncio
import time
from vts_integration import vts_integration
from voice_api import voice_api_system

class VTSTester:
    """VTubeStudio功能测试器"""
    
    def __init__(self):
        self.vts = vts_integration
        self.is_connected = False
    
    async def test_basic_connection(self):
        """测试基础连接功能"""
        print("🔌 测试VTS基础连接...")
        
        try:
            # 测试连接
            success = await self.vts.connect()
            if success:
                print("✅ VTS连接成功")
                self.is_connected = True
                
                # 获取状态信息
                status = await self.vts.get_status()
                print(f"📊 VTS状态: {status}")
                
                # 获取当前模型信息
                current_model = await self.vts.get_current_model()
                print(f"🎭 当前模型: {current_model}")
                
                return True
            else:
                print("❌ VTS连接失败")
                print("请确保:")
                print("  1. VTubeStudio正在运行")
                print("  2. VTubeStudio的API服务器已启用")
                print("  3. 端口配置正确(默认9001)")
                return False
                
        except Exception as e:
            print(f"❌ 连接测试异常: {e}")
            return False
    
    async def test_model_operations(self):
        """测试模型操作功能"""
        if not self.is_connected:
            print("❌ 请先建立VTS连接")
            return False
        
        print("\n🎭 测试模型操作...")
        
        try:
            # 获取可用模型列表
            models = await self.vts.get_available_models()
            print(f"📋 可用模型数量: {len(models)}")
            
            if models:
                print("前3个模型:")
                for i, model in enumerate(models[:3]):
                    print(f"  {i+1}. {model}")
            
            # 测试模型切换（如果不只有一个模型）
            if len(models) > 1:
                print(f"\n🔄 测试切换到模型: {models[1]}")
                switch_success = await self.vts.load_model(models[1])
                if switch_success:
                    print("✅ 模型切换成功")
                    # 切换回原模型
                    await asyncio.sleep(1)
                    await self.vts.load_model(models[0])
                    print("🔄 已切回原模型")
                else:
                    print("❌ 模型切换失败")
            
            return True
            
        except Exception as e:
            print(f"❌ 模型操作测试失败: {e}")
            return False
    
    async def test_hotkey_triggers(self):
        """测试热键触发功能"""
        if not self.is_connected:
            print("❌ 请先建立VTS连接")
            return False
        
        print("\n🔥 测试热键触发...")
        
        try:
            # 获取可用热键
            hotkeys = await self.vts.get_hotkeys()
            print(f"📋 可用热键数量: {len(hotkeys)}")
            
            if hotkeys:
                print("前5个热键:")
                for i, hotkey in enumerate(hotkeys[:5]):
                    print(f"  {i+1}. {hotkey}")
                
                # 测试触发第一个热键
                print(f"\n⚡ 触发热键: {hotkeys[0]}")
                trigger_success = await self.vts.trigger_hotkey(hotkeys[0])
                if trigger_success:
                    print("✅ 热键触发成功")
                else:
                    print("❌ 热键触发失败")
            else:
                print("⚠️ 未找到可用热键")
            
            return True
            
        except Exception as e:
            print(f"❌ 热键测试失败: {e}")
            return False
    
    async def test_expressions(self):
        """测试表情功能"""
        if not self.is_connected:
            print("❌ 请先建立VTS连接")
            return False
        
        print("\n😊 测试表情功能...")
        
        try:
            # 获取可用表情
            expressions = await self.vts.get_expressions()
            print(f"📋 可用表情数量: {len(expressions)}")
            
            if expressions:
                print("前5个表情:")
                for i, expr in enumerate(expressions[:5]):
                    print(f"  {i+1}. {expr}")
                
                # 测试激活第一个表情
                print(f"\n🎭 激活表情: {expressions[0]}")
                activate_success = await self.vts.activate_expression(expressions[0])
                if activate_success:
                    print("✅ 表情激活成功")
                    # 等待2秒后停用
                    await asyncio.sleep(2)
                    await self.vts.deactivate_expression(expressions[0])
                    print("🔄 表情已停用")
                else:
                    print("❌ 表情激活失败")
            else:
                print("⚠️ 未找到可用表情")
            
            return True
            
        except Exception as e:
            print(f"❌ 表情测试失败: {e}")
            return False
    
    async def test_tts_integration(self):
        """测试TTS与VTS集成"""
        if not self.is_connected:
            print("❌ 请先建立VTS连接")
            return False
        
        print("\n🎙️ 测试TTS与VTS集成...")
        
        try:
            test_text = "你好，我是AI虚拟主播，现在测试语音驱动功能！"
            print(f"📝 测试文本: {test_text}")
            
            # 生成语音并驱动口型
            print("🔄 生成语音并驱动VTS...")
            success = await self.vts.text_to_speech_with_lip_sync(test_text, "tts_vts_test.wav")
            
            if success:
                print("✅ TTS+VTS集成成功")
                print("🎙️ 语音已生成并通过虚拟麦克风输出到VTS")
                print("👄 VTS模型应该正在同步口型动画")
            else:
                print("❌ TTS+VTS集成失败")
            
            return success
            
        except Exception as e:
            print(f"❌ TTS集成测试失败: {e}")
            return False
    
    async def test_performance_monitoring(self):
        """测试性能监控"""
        if not self.is_connected:
            print("❌ 请先建立VTS连接")
            return False
        
        print("\n📊 测试性能监控...")
        
        try:
            # 获取性能数据
            performance = await self.vts.get_performance_stats()
            print("📈 性能统计数据:")
            for key, value in performance.items():
                print(f"  {key}: {value}")
            
            # 监控一段时间
            print("\n⏱️ 开始5秒性能监控...")
            for i in range(5):
                stats = await self.vts.get_performance_stats()
                fps = stats.get('fps', 'N/A')
                print(f"  第{i+1}秒 - FPS: {fps}")
                await asyncio.sleep(1)
            
            return True
            
        except Exception as e:
            print(f"❌ 性能监控测试失败: {e}")
            return False
    
    async def run_comprehensive_test(self):
        """运行综合测试"""
        print("🎯 VTubeStudio综合功能测试")
        print("=" * 50)
        
        # 测试顺序
        tests = [
            ("基础连接测试", self.test_basic_connection),
            ("模型操作测试", self.test_model_operations),
            ("热键触发测试", self.test_hotkey_triggers),
            ("表情功能测试", self.test_expressions),
            ("TTS集成测试", self.test_tts_integration),
            ("性能监控测试", self.test_performance_monitoring)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                result = await test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} 异常: {e}")
                results.append((test_name, False))
        
        # 输出测试总结
        print("\n" + "=" * 50)
        print("📋 测试结果总结:")
        print("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{status} {test_name}")
            if result:
                passed += 1
        
        print("=" * 50)
        print(f"总体结果: {passed}/{total} 项测试通过")
        print(f"成功率: {passed/total*100:.1f}%")
        
        if passed == total:
            print("🎉 所有测试通过！VTS集成功能完美运行！")
        elif passed >= total * 0.8:
            print("✅ 大部分功能正常，可以正常使用")
        else:
            print("⚠️ 存在较多问题，建议检查配置")
        
        return passed == total

async def main():
    """主测试函数"""
    tester = VTSTester()
    
    # 运行综合测试
    success = await tester.run_comprehensive_test()
    
    # 断开连接
    if tester.is_connected:
        print("\n🔌 断开VTS连接...")
        await tester.vts.disconnect()
        print("✅ 连接已断开")
    
    return success

if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())