import asyncio
from voice_api import voice_api_system
from vts_integration import vts_integration

async def test_tts_options():
    """测试不同TTS引擎选项"""
    print("🔍 测试TTS引擎选项...")
    
    test_text = "你好，我是一个虚拟主播，正在测试不同的TTS引擎。"
    
    # 优先测试通义千问TTS
    print("\n1. 测试通义千问TTS...")
    qwen_result = voice_api_system.text_to_speech(test_text, "test_qwen.wav", engine="qwen")
    print(f"通义千问TTS结果: {'成功' if qwen_result else '失败'}")
    
    # 测试本地TTS
    print("\n2. 测试本地TTS...")
    local_result = voice_api_system.text_to_speech(test_text, "test_local.wav", engine="local")
    print(f"本地TTS结果: {'成功' if local_result else '失败'}")
    
    # 测试Edge TTS（暂时放在后面）
    print("\n3. 测试Edge TTS...")
    edge_result = voice_api_system.text_to_speech(test_text, "test_edge.wav", engine="edge")
    print(f"Edge TTS结果: {'成功' if edge_result else '失败'}")
    
    return True

async def test_virtual_audio():
    """测试虚拟声卡/麦克风功能"""
    print("\n🔍 测试虚拟音频功能...")
    
    test_text = "你好，我是一个虚拟主播，正在测试虚拟声卡功能。"
    
    # 测试语音生成和虚拟声卡播放
    success = vts_integration.text_to_speech_with_lip_sync(test_text, "test_virtual.wav")
    print(f"虚拟音频测试结果: {'成功' if success else '失败'}")
    
    return success

async def main():
    """主测试函数"""
    print("🚀 开始测试TTS选项和虚拟音频功能...")
    
    # 测试TTS选项
    await test_tts_options()
    
    # 测试虚拟音频
    await test_virtual_audio()
    
    print("\n✅ 所有测试完成！")

if __name__ == "__main__":
    asyncio.run(main())
