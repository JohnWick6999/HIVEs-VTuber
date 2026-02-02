#!/usr/bin/env python3
# 测试通义千问TTS功能

from voice_api import voice_api_system
import os

def test_qwen_voice_design():
    """测试通义千问声音设计功能"""
    print("测试通义千问声音设计功能...")
    
    # 可爱的声音描述
    cute_voice_prompt = "年轻活泼的可爱女性声音，语速较快，语调上扬，音色甜美清脆，带有少女感，适合动画角色配音或语音助手。"
    
    # 试听文本
    preview_text = "你好，我是你的AI虚拟主播，很高兴认识你！我会用可爱的声音和你聊天哦～喵呜～"
    
    # 获取API Key
    import config
    config_manager = config.ConfigManager()
    voice_config = config_manager.get_voice_api_config()
    api_key = voice_config.get("tts", {}).get("api_key")
    
    if not api_key:
        print("❌ 未配置通义千问API Key")
        return None
    
    print("正在创建定制音色...")
    print(f"声音描述: {cute_voice_prompt}")
    print(f"试听文本: {preview_text}")
    
    # 调用声音设计API
    voice_name = voice_api_system._qwen_voice_design(api_key, cute_voice_prompt, preview_text)
    
    if voice_name:
        print(f"✅ 成功创建定制音色: {voice_name}")
        return voice_name
    else:
        print("❌ 声音设计失败")
        return None

def test_qwen_tts(text, voice_name, description):
    """测试通义千问TTS功能"""
    print(f"\n=== 测试: {description} ===")
    print(f"文本: {text}")
    print(f"音色: {voice_name}")
    
    output_file = f"test_qwen_{description.replace(' ', '_')}.mp3"
    
    # 调用TTS功能
    result = voice_api_system.text_to_speech(text, output_file)
    
    if result and os.path.exists(output_file):
        file_size = os.path.getsize(output_file) / 1024
        print(f"✅ 成功生成音频文件！")
        print(f"文件大小: {file_size:.2f} KB")
        
        # 播放音频
        print("正在播放音频...")
        if os.name == 'nt':  # Windows
            os.startfile(output_file)
        elif os.name == 'posix':  # macOS/Linux
            import subprocess
            subprocess.run(['open', output_file] if os.uname().sysname == 'Darwin' else ['xdg-open', output_file])
        
        # 等待用户确认
        input("\n按回车键清理测试文件...")
        
        # 清理测试文件
        os.remove(output_file)
        print("测试文件已清理")
        return True
    else:
        print("❌ 音频文件生成失败")
        return False

def main():
    print("测试通义千问TTS功能")
    print("=" * 60)
    
    # 测试1: 创建定制音色
    # voice_name = test_qwen_voice_design()
    # if not voice_name:
    #     print("声音设计失败，使用默认音色继续测试...")
    #     voice_name = "default"
    
    # 暂时使用默认音色测试
    voice_name = "default"
    
    # 测试2: 基本语音合成
    test_text = "你好，我是你的AI虚拟主播，很高兴认识你！"
    test_qwen_tts(test_text, voice_name, "基本问候")
    
    # 测试3: 可爱风格
    cute_text = "你好呀～我是你的AI虚拟主播，很高兴认识你！我会用可爱的声音和你聊天哦～喵呜～"
    test_qwen_tts(cute_text, voice_name, "可爱风格")
    
    # 测试4: 天气播报
    weather_text = "今天天气晴朗，温度适宜，非常适合户外活动。"
    test_qwen_tts(weather_text, voice_name, "天气播报")
    
    print("\n" + "=" * 60)
    print("所有测试完成！")

if __name__ == "__main__":
    main()
