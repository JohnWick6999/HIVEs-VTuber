#!/usr/bin/env python3
# 测试通义千问TTS完整流程

from voice_api import voice_api_system
import os

def test_qwen_full_flow():
    """测试通义千问TTS完整流程"""
    print("测试通义千问TTS完整流程")
    print("=" * 60)
    print("请按照以下步骤操作:")
    print("1. 准备一个10-30秒的单声道音频文件 (推荐16kHz)")
    print("2. 将音频文件命名为 'my_voice_10s.mp3' 并放在当前目录")
    print("3. 确保已安装依赖: pip install -U dashscope pyaudio")
    print("4. 确保已配置通义千问API Key")
    print("=" * 60)
    
    # 检查音频文件是否存在
    audio_file = "../../data/voice/e3fd62b8656da51a240754cb3919d3ea.mp3"
    if not os.path.exists(audio_file):
        print(f"❌ 音频文件不存在: {audio_file}")
        print("请确认音频文件路径正确")
        return False
    
    print(f"✅ 找到音频文件: {audio_file}")
    print(f"文件大小: {os.path.getsize(audio_file) / (1024*1024):.2f} MB")
    
    # 获取API Key
    import config
    config_manager = config.ConfigManager()
    voice_config = config_manager.get_voice_api_config()
    api_key = voice_config.get("tts", {}).get("api_key")
    
    if not api_key:
        print("❌ 未配置通义千问API Key")
        print("请在 data/config.json 中配置 voice_api.tts.api_key")
        return False
    
    print("✅ 已配置通义千问API Key")
    
    # Step 1: 创建专属音色
    print("\n=== Step 1: 创建专属音色 ===")
    print("正在使用音频文件创建专属音色...")
    
    voice_name = voice_api_system._qwen_voice_enrollment(api_key, audio_file, "my_ai_voice")
    
    if not voice_name:
        print("❌ 音色创建失败")
        return False
    
    print(f"✅ 成功创建专属音色: {voice_name}")
    
    # Step 2: 实时流式合成
    print("\n=== Step 2: 实时流式合成 ===")
    test_text = "你好，这是使用我的专属音色进行实时流式合成的测试。首包延迟大约三百毫秒，支持无限长文本流式输出。"
    print(f"测试文本: {test_text}")
    
    print("正在进行实时流式合成...")
    result = voice_api_system._qwen_realtime_tts(api_key, test_text, voice_name)
    
    if result:
        print("✅ 实时流式合成成功！")
    else:
        print("❌ 实时流式合成失败")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print(f"你的专属音色名称: {voice_name}")
    print("你可以在后续的TTS调用中使用这个音色")
    return result

def main():
    # 检查依赖
    try:
        import dashscope
        import pyaudio
        print("✅ 依赖库已安装")
    except ImportError:
        print("❌ 缺少依赖库")
        print("请运行: pip install -U dashscope pyaudio")
        return
    
    # 运行测试
    test_qwen_full_flow()

if __name__ == "__main__":
    main()
