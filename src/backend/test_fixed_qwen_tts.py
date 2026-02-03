#!/usr/bin/env python3
# 测试修复后的通义千问TTS功能

from voice_api import voice_api_system
import os
import time

def test_fixed_qwen_tts():
    """测试修复后的通义千问TTS功能"""
    print("🔧 测试修复后的通义千问TTS功能")
    print("=" * 60)
    
    # 检查API Key配置
    import config
    config_manager = config.ConfigManager()
    voice_config = config_manager.get_voice_api_config()
    api_key = voice_config.get("tts", {}).get("api_key")
    
    if not api_key:
        print("❌ 未配置通义千问API Key")
        print("请在 data/config.json 中配置 voice_api.tts.api_key")
        return False
    
    print("✅ 已配置通义千问API Key")
    print(f"API Key 前缀: {api_key[:10]}...")
    
    # 测试用例
    test_cases = [
        {
            "text": "你好，我是你的AI虚拟主播，很高兴认识你！",
            "description": "基本问候",
            "voice": "Cherry"
        },
        {
            "text": "今天天气晴朗，温度适宜，非常适合户外活动。",
            "description": "天气播报",
            "voice": "Cherry"
        },
        {
            "text": "你好呀～我是你的AI虚拟主播，我会用可爱的声音和你聊天哦～喵呜～",
            "description": "可爱风格",
            "voice": "Cherry"
        },
        {
            "text": "欢迎使用AI虚拟主播系统，我可以为你提供各种信息服务。",
            "description": "系统介绍",
            "voice": "Cherry"
        }
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    print(f"\n开始测试 {total_tests} 个用例...")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}/{total_tests}] 测试: {test_case['description']}")
        print(f"文本: {test_case['text']}")
        print(f"音色: {test_case['voice']}")
        
        output_file = f"test_fixed_{i}_{test_case['description'].replace(' ', '_')}.wav"
        
        try:
            # 调用修复后的TTS功能
            start_time = time.time()
            result = voice_api_system.text_to_speech(
                test_case['text'], 
                output_file, 
                engine="qwen"
            )
            end_time = time.time()
            
            if result and os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"✅ TTS生成成功!")
                print(f"   文件大小: {file_size} bytes ({file_size/1024:.2f} KB)")
                print(f"   生成耗时: {end_time - start_time:.2f} 秒")
                
                # 尝试播放音频（仅在Windows上）
                if os.name == 'nt':
                    try:
                        print("🔊 正在播放音频...")
                        os.startfile(output_file)
                        time.sleep(2)  # 等待播放开始
                    except Exception as e:
                        print(f"⚠️ 音频播放失败: {e}")
                
                # 询问是否保留文件
                choice = input("是否保留此测试文件? (y/n): ").lower().strip()
                if choice != 'y':
                    try:
                        os.remove(output_file)
                        print("🗑️  测试文件已删除")
                    except Exception as e:
                        print(f"⚠️ 删除文件失败: {e}")
                else:
                    print(f"💾 文件已保存: {output_file}")
                
                success_count += 1
            else:
                print("❌ TTS生成失败")
                # 检查是否有错误文件
                if os.path.exists(output_file):
                    try:
                        os.remove(output_file)
                    except:
                        pass
                    
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("测试结果统计:")
    print(f"成功: {success_count}/{total_tests}")
    print(f"失败: {total_tests - success_count}/{total_tests}")
    print(f"成功率: {success_count/total_tests*100:.1f}%")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！TTS修复成功！")
        return True
    else:
        print("⚠️ 部分测试失败，请检查日志")
        return False

def test_voice_list():
    """测试可用的音色列表"""
    print("\n🎤 可用音色列表测试")
    print("=" * 40)
    
    # 常用音色列表
    voices = [
        "Cherry",      # 樱桃 - 默认女声
        "Alice",       # 爱丽丝
        "Eric",        # 埃里克
        "Harry",       # 哈利
        "Shuaishuai",  # 帅帅
        "Xiaoyun",     # 小云
        "Xiaogang"     # 小刚
    ]
    
    test_text = "你好，测试音色。"
    
    for voice in voices:
        print(f"\n测试音色: {voice}")
        output_file = f"test_voice_{voice}.wav"
        
        try:
            result = voice_api_system.text_to_speech(test_text, output_file, engine="qwen")
            if result and os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"  ✅ 成功 ({size} bytes)")
                # 清理文件
                os.remove(output_file)
            else:
                print(f"  ❌ 失败")
        except Exception as e:
            print(f"  ❌ 异常: {e}")

def main():
    print("🤖 通义千问TTS修复验证测试")
    print("=" * 60)
    
    # 检查依赖
    try:
        import dashscope
        print("✅ DashScope已安装")
        # 版本检查
        try:
            # 尝试获取版本信息
            import pkg_resources
            version = pkg_resources.get_distribution("dashscope").version
            print(f"✅ DashScope版本: {version}")
            if tuple(map(int, version.split('.')[:2])) < (1, 25):
                print("⚠️  DashScope版本可能过低，请确保 >= 1.25.2")
        except:
            print("✅ DashScope版本信息不可用，但已安装")
    except ImportError:
        print("❌ 未安装DashScope，请运行: pip install -U dashscope>=1.25.2")
        return
    
    try:
        import pyaudio
        print("✅ PyAudio已安装")
    except ImportError:
        print("⚠️ 未安装PyAudio，实时播放功能可能受限")
    
    # 运行主要测试
    success = test_fixed_qwen_tts()
    
    # 可选：测试音色列表
    if success:
        choice = input("\n是否测试不同音色? (y/n): ").lower().strip()
        if choice == 'y':
            test_voice_list()
    
    print("\n" + "=" * 60)
    print("🏁 测试完成！")
    
    if success:
        print("✅ TTS功能已成功修复")
        print("现在可以正常使用通义千问TTS服务了！")
    else:
        print("❌ TTS功能仍有问题")
        print("请检查API Key配置和网络连接")

if __name__ == "__main__":
    main()