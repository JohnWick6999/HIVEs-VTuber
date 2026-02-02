#!/usr/bin/env python3
# TTS播放测试 - 让用户听到声音

from voice_api import voice_api_system
import os
import platform
import subprocess

def play_audio_file(file_path):
    """播放音频文件"""
    try:
        system = platform.system()
        
        if system == 'Windows':
            # Windows系统使用默认播放器
            os.startfile(file_path)
        elif system == 'Darwin':
            # macOS系统使用afplay
            subprocess.run(['afplay', file_path], check=True)
        else:
            # Linux系统使用aplay或mpg123
            try:
                subprocess.run(['mpg123', file_path], check=True)
            except FileNotFoundError:
                subprocess.run(['aplay', file_path], check=True)
        
        print("正在播放音频...")
        return True
    except Exception as e:
        print(f"播放音频失败: {e}")
        return False

def main():
    print("TTS播放测试 - 让你听到声音")
    print("=" * 60)
    
    # 可爱的测试文本
    cute_text = "你好，我是你的AI虚拟主播，很高兴认识你！我会用可爱的声音和你聊天哦～喵呜～"
    
    # 选择可爱的语音预设
    cute_voice = "zh-CN-YunxiNeural"  # 云溪 (可爱女声)
    output_file = "test_playback.mp3"
    
    print(f"测试文本: {cute_text}")
    print(f"语音预设: {cute_voice}")
    print("\n正在生成音频...")
    
    # 生成音频
    result = voice_api_system.test_voice_preset(cute_text, cute_voice, output_file)
    
    if result and os.path.exists(output_file):
        file_size = os.path.getsize(output_file) / 1024
        print(f"✅ 音频文件生成成功！")
        print(f"文件大小: {file_size:.2f} KB")
        
        # 播放音频
        print("\n准备播放音频，请稍等...")
        play_audio_file(output_file)
        
        # 等待用户确认
        input("\n按回车键清理测试文件...")
        
        # 清理测试文件
        os.remove(output_file)
        print("测试文件已清理")
    else:
        print("❌ 音频文件生成失败")
    
    print("\n" + "=" * 60)
    print("测试完成！")

if __name__ == "__main__":
    main()
