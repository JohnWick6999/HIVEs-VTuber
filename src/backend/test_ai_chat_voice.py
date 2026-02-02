#!/usr/bin/env python3
# 测试AI对话 + 实时语音结合

from ai_chat_system import AIChatSystem
from voice_api import voice_api_system
import os

def test_ai_chat_with_voice():
    """测试AI对话与实时语音结合"""
    print("测试AI对话 + 实时语音结合")
    print("=" * 60)
    print("系统将：")
    print("1. 接收您的输入")
    print("2. 使用AI生成回复");
    print("3. 使用萝莉音实时朗读回复")
    print("=" * 60)
    
    # 初始化AI聊天系统
    print("正在初始化AI聊天系统...")
    chat_system = AIChatSystem()
    print("✅ AI聊天系统初始化完成")
    
    # 获取通义千问API Key
    import config
    config_manager = config.ConfigManager()
    voice_config = config_manager.get_voice_api_config()
    api_key = voice_config.get("tts", {}).get("api_key")
    
    if not api_key:
        print("❌ 未配置通义千问API Key")
        return False
    
    print("✅ 已配置通义千问API Key")
    
    # 使用之前创建的萝莉音音色
    loli_voice = "qwen-tts-vc-loli_voice-voice-20260203005435327-786e"
    print(f"✅ 使用萝莉音音色: {loli_voice}")
    
    print("\n开始对话测试（输入 'exit' 退出）...")
    
    while True:
        try:
            # 获取用户输入
            user_input = input("\n你: ")
            
            # 检查是否退出
            if user_input.lower() == 'exit':
                print("再见！")
                break
            
            # 检查输入是否为空
            if not user_input.strip():
                print("请输入消息内容")
                continue
            
            # 生成AI回复
            print("AI: ", end="", flush=True)
            ai_response = chat_system.generate_response(user_input)
            print(ai_response)
            
            # 使用实时TTS朗读回复
            print("\n🎤 正在使用萝莉音朗读...")
            tts_result = voice_api_system._qwen_realtime_tts(api_key, ai_response, loli_voice)
            
            if not tts_result:
                print("❌ 语音朗读失败，使用本地TTS...")
                # 使用本地TTS作为备选
                local_output = "local_tts_output.wav"
                local_result = voice_api_system._local_text_to_speech(ai_response, local_output)
                if local_result and os.path.exists(local_output):
                    # 播放本地TTS文件
                    if os.name == 'nt':  # Windows
                        os.startfile(local_output)
                    elif os.name == 'posix':  # macOS/Linux
                        import subprocess
                        subprocess.run(['open', local_output] if os.uname().sysname == 'Darwin' else ['xdg-open', local_output])
                    os.remove(local_output)
                
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"错误: {e}")
            continue
    
    return True

def main():
    test_ai_chat_with_voice()

if __name__ == "__main__":
    main()
