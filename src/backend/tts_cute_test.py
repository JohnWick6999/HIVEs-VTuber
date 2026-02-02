#!/usr/bin/env python3
# 测试可爱的TTS语音预设

from voice_api import voice_api_system
import os

def test_cute_voice(text, voice_preset, description):
    """测试可爱的语音预设"""
    print(f"\n=== 测试: {description} ===")
    print(f"语音预设: {voice_preset}")
    print(f"文本: {text}")
    
    output_file = f"test_{voice_preset.replace('-', '_')}.mp3"
    
    # 测试语音预设
    result = voice_api_system.test_voice_preset(text, voice_preset, output_file)
    
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
    print("测试可爱的TTS语音预设")
    print("=" * 60)
    
    # 可爱的测试文本
    cute_text = "你好，我是你的AI虚拟主播，很高兴认识你！我会用可爱的声音和你聊天哦～喵呜～"
    
    # 可爱的语音预设列表
    cute_voice_presets = [
        ("zh-CN-YunxiNeural", "云溪 (可爱女声)"),
        ("zh-CN-XiaoxiaoNeural", "晓晓 (活泼女声)"),
        ("zh-CN-YunyangNeural", "云扬 (温柔男声)"),
        ("zh-CN-liaoning-YunxiNeural", "云溪 (辽宁话)"),
        ("zh-CN-shaanxi-YunxiNeural", "云溪 (陕西话)")
    ]
    
    # 测试每种语音预设
    for voice_preset, desc in cute_voice_presets:
        test_cute_voice(cute_text, voice_preset, desc)
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("\n推荐选择:")
    print("- 可爱女声: zh-CN-YunxiNeural (云溪)")
    print("- 活泼女声: zh-CN-XiaoxiaoNeural (晓晓)")
    print("- 温柔男声: zh-CN-YunyangNeural (云扬)")

if __name__ == "__main__":
    main()
