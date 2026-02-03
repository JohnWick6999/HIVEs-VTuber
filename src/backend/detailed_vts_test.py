#!/usr/bin/env python3
# VTS连接详细测试

import asyncio
import time
import socket
from vts_integration import vts_integration

async def detailed_vts_test():
    """详细测试VTS连接"""
    print("🔍 VTS详细连接测试")
    print("=" * 40)
    
    # 1. 检查端口是否开放
    print("1️⃣ 检查端口9001状态...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('localhost', 9001))
        sock.close()
        
        if result == 0:
            print("✅ 端口9001已开放")
        else:
            print("❌ 端口9001未开放")
            print("💡 请确保:")
            print("   • VTubeStudio正在运行")
            print("   • API服务器已启用(F12 → Misc → Enable Access to VTubeStudio API)")
            print("   • 端口设置为9001")
            return False
    except Exception as e:
        print(f"❌ 端口检查失败: {e}")
        return False
    
    # 2. 测试VTS连接
    print("\n2️⃣ 测试VTS连接...")
    try:
        success = await vts_integration.connect()
        if success:
            print("✅ VTS连接成功")
            
            # 3. 获取基本信息
            print("\n3️⃣ 获取VTS信息...")
            try:
                # 获取状态
                status = await vts_integration.vts.request("StatisticsRequest")
                print(f"📊 VTS统计信息: {status}")
                
                # 获取当前模型
                current_model = await vts_integration.vts.request("CurrentModelRequest")
                print(f"🎭 当前模型: {current_model}")
                
                # 获取可用热键
                hotkeys = await vts_integration.vts.request("HotkeysInCurrentModelRequest")
                print(f"🔥 可用热键数量: {len(hotkeys.get('availableHotkeys', []))}")
                
                print("\n🎉 VTS连接测试成功！")
                return True
                
            except Exception as e:
                print(f"⚠️ 获取信息时出错: {e}")
                print("✅ 但基础连接成功")
                return True
        else:
            print("❌ VTS连接失败")
            return False
            
    except Exception as e:
        print(f"❌ 连接测试异常: {e}")
        return False

async def test_vts_features():
    """测试VTS具体功能"""
    print("\n🎯 VTS功能测试")
    print("=" * 30)
    
    try:
        # 连接VTS
        connected = await vts_integration.connect()
        if not connected:
            print("❌ 无法连接VTS")
            return False
        
        print("✅ VTS连接成功")
        
        # 测试文本转语音+口型同步
        print("\n🎙️ 测试TTS+口型同步...")
        test_text = "你好，我是AI虚拟主播，现在测试VTS集成功能！"
        success = vts_integration.text_to_speech_with_lip_sync(test_text, "vts_test.wav")
        
        if success:
            print("✅ TTS+口型同步测试成功")
        else:
            print("❌ TTS+口型同步测试失败")
        
        # 测试热键触发
        print("\n🔥 测试热键触发...")
        try:
            # 获取热键列表
            hotkeys_response = await vts_integration.vts.request("HotkeysInCurrentModelRequest")
            available_hotkeys = hotkeys_response.get('availableHotkeys', [])
            
            if available_hotkeys:
                first_hotkey = available_hotkeys[0]['name']
                print(f"触发热键: {first_hotkey}")
                
                # 触发热键
                trigger_response = await vts_integration.vts.request("HotkeyTriggerRequest", {
                    "hotkeyID": first_hotkey
                })
                print(f"热键触发结果: {trigger_response}")
            else:
                print("⚠️ 未找到可用热键")
                
        except Exception as e:
            print(f"❌ 热键测试失败: {e}")
        
        # 断开连接
        await vts_integration.disconnect()
        print("🔌 VTS连接已断开")
        
        return True
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🤖 VTS集成详细测试")
    print("=" * 25)
    
    # 运行详细连接测试
    connection_success = asyncio.run(detailed_vts_test())
    
    if connection_success:
        # 如果连接成功，测试具体功能
        feature_success = asyncio.run(test_vts_features())
        
        print("\n" + "=" * 40)
        print("📋 测试总结:")
        print("=" * 40)
        print("✅ VTS连接测试: 通过")
        print(f"{'✅' if feature_success else '❌'} VTS功能测试: {'通过' if feature_success else '失败'}")
        print("=" * 40)
        
        if feature_success:
            print("🎉 VTS集成功能完美运行！")
        else:
            print("⚠️ VTS基础连接成功，但某些功能需要配置")
    else:
        print("\n❌ VTS连接失败，请检查:")
        print("1. VTubeStudio是否正在运行")
        print("2. 是否启用了API服务器")
        print("3. 端口9001是否正确配置")

if __name__ == "__main__":
    main()