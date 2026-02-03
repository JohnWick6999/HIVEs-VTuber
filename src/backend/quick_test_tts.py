#!/usr/bin/env python3
# 快速测试修复后的通义千问TTS功能

from voice_api import voice_api_system
import os
import time

def quick_test():
    """快速测试TTS功能"""
    print("⚡ 快速测试通义千问TTS修复")
    print("=" * 50)
    
    # 获取配置
    import config
    config_manager = config.ConfigManager()
    voice_config = config_manager.get_voice_api_config()
    api_key = voice_config.get("tts", {}).get("api_key")
    
    if not api_key:
        print("❌ 未配置API Key")
        return False
    
    print("✅ API Key配置正常")
    
    # 简单测试文本
    test_text = "你好，测试成功！"
    output_file = "quick_test.wav"
    
    print(f"📝 测试文本: {test_text}")
    print("🔄 开始TTS合成...")
    
    try:
        start_time = time.time()
        result = voice_api_system.text_to_speech(test_text, output_file, engine="qwen")
        end_time = time.time()
        
        print(f"⏱️  耗时: {end_time - start_time:.2f}秒")
        
        if result and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✅ TTS成功! 文件大小: {file_size} bytes")
            
            # 播放测试
            if os.name == 'nt':
                print("🔊 播放音频...")
                os.startfile(output_file)
                time.sleep(3)
            
            # 询问保留
            choice = input("保留测试文件? (y/n): ").strip().lower()
            if choice != 'y':
                os.remove(output_file)
                print("🗑️  文件已删除")
            else:
                print(f"💾 文件保存为: {output_file}")
            
            return True
        else:
            print("❌ TTS失败")
            return False
            
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_test()
    print("\n" + "=" * 50)
    if success:
        print("🎉 TTS修复成功！")
    else:
        print("⚠️  TTS仍有问题")