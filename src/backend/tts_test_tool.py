#!/usr/bin/env python3
# 简单的TTS测试工具

from voice_api import voice_api_system
import os

def test_voice_preset(text, voice_preset, description):
    """测试特定语音预设的TTS功能"""
    print(f"\n=== 测试: {description} ===")
    print(f"语音预设: {voice_preset}")
    print(f"文本: {text}")
    
    output_file = f"test_{voice_preset.replace('-', '_')}.mp3"
    
    # 临时修改voice_api_system的配置来测试不同的语音
    import config
    config_manager = config.ConfigManager()
    temp_config = config_manager.get_config()
    temp_config['voice_api']['tts']['voice'] = voice_preset
    
    # 保存临时配置
    import json
    with open('data/config.json', 'w', encoding='utf-8') as f:
        json.dump(temp_config, f, ensure_ascii=False, indent=2)
    
    # 重新初始化voice_api_system
    global voice_api_system
    from voice_api import VoiceAPISystem
    voice_api_system = VoiceAPISystem()
    
    # 测试TTS
    result = voice_api_system.text_to_speech(text, output_file)
    
    if result and os.path.exists(output_file):
        file_size = os.path.getsize(output_file) / 1024
        print(f"✅ 成功生成音频文件！")
        print(f"文件大小: {file_size:.2f} KB")
        os.remove(output_file)
        print("测试文件已清理")
        return True
    else:
        print("❌ 音频文件生成失败")
        return False

def main():
    print("简单的TTS测试工具")
    print("=" * 60)
    
    # 测试文本
    test_text = "你好，我是你的AI虚拟主播，很高兴认识你！我会用可爱的声音和你聊天哦～"
    
    # 可爱的语音预设
    cute_voices = [
        "zh-CN-YunxiNeural",  # 云溪（可爱女声）
        "zh-CN-XiaoxiaoNeural",  # 晓晓（活泼女声）
        "zh-CN-YunyangNeural",  # 云扬（温柔男声）
        "zh-CN-liaoning-YunxiNeural"  # 云溪（辽宁话）
    ]
    
    # 测试每种语音预设
    for voice in cute_voices:
        test_voice_preset(test_text, voice, f"可爱语音 - {voice}")
    
    print("\n" + "=" * 60)
    print("所有测试完成！")

if __name__ == "__main__":
    main()
