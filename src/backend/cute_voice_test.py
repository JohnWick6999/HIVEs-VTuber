#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可爱音色测试脚本
测试各种萌系音色效果
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from vts_integration import vts_integration
from cute_voices import list_available_cute_voices, CUTE_VOICES
import time

def test_cute_voices():
    """测试所有可爱音色"""
    print("🎀 可爱音色大赏")
    print("=" * 40)
    
    # 显示可用音色
    list_available_cute_voices()
    
    # 测试用语句
    test_sentences = [
        "主人，人家才不是故意要迟到的呢！",
        "哼！才不是为了你才这么努力的！",
        "要、要加油哦...虽然是为了我自己啦！",
        "呜哇！你怎么可以这样对我！",
        "好啦好啦，我知道了啦～"
    ]
    
    print(f"\n🎤 开始音色测试...")
    print("=" * 40)
    
    # 测试每个音色
    for voice_name in CUTE_VOICES.keys():
        print(f"\n🌟 测试音色: {voice_name}")
        print("-" * 30)
        
        for i, sentence in enumerate(test_sentences[:2], 1):  # 每个音色测试2句
            print(f"[{i}] {sentence}")
            
            # 使用对应音色播放
            success = vts_integration.text_to_speech_with_lip_sync(
                sentence, 
                voice_style=voice_name
            )
            
            if success:
                print(f"   ✅ 播放成功")
            else:
                print(f"   ❌ 播放失败")
            
            # 间隔等待
            time.sleep(2)
        
        # 音色间等待
        print(f"💤 切换到下一个音色...")
        time.sleep(3)
    
    print("\n" + "=" * 40)
    print("🎉 音色测试完成！")
    print("请选择您最喜欢的音色风格～")

def interactive_cute_voice_test():
    """交互式可爱音色测试"""
    print("💬 交互式可爱音色测试")
    print("=" * 30)
    
    list_available_cute_voices()
    
    while True:
        print(f"\n请输入要测试的内容 (输入 'quit' 退出):")
        user_input = input("🗣️  您要说: ").strip()
        
        if user_input.lower() in ['quit', 'exit', '退出']:
            print("👋 再见啦～")
            break
            
        if not user_input:
            continue
            
        print("请选择音色风格:")
        voice_keys = list(CUTE_VOICES.keys())
        for i, voice_name in enumerate(voice_keys, 1):
            print(f"  {i}. {voice_name}")
        
        try:
            choice = int(input("请选择 (1-{}): ".format(len(voice_keys)))) - 1
            if 0 <= choice < len(voice_keys):
                selected_voice = voice_keys[choice]
                print(f"\n🎭 使用音色: {selected_voice}")
                
                success = vts_integration.text_to_speech_with_lip_sync(
                    user_input,
                    voice_style=selected_voice
                )
                
                if success:
                    print("✅ 播放完成")
                else:
                    print("❌ 播放失败")
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入数字")
        
        time.sleep(1)

def quick_demo():
    """快速演示"""
    print("⚡ 快速可爱音色演示")
    print("=" * 25)
    
    demo_text = "哼！才不想理你呢！不过...如果你求我的话，勉为其难帮你一下好了啦～"
    
    print("使用默认傲娇萝莉音色:")
    vts_integration.text_to_speech_with_lip_sync(demo_text, voice_style="傲娇萝莉")
    
    time.sleep(2)
    
    print("\n使用天然呆萌音色:")
    vts_integration.text_to_speech_with_lip_sync(demo_text, voice_style="天然呆萌")

if __name__ == "__main__":
    print("🎀 欢迎来到可爱音色世界！")
    
    while True:
        print("\n请选择测试模式:")
        print("1. 🎭 完整音色测试")
        print("2. 💬 交互式测试") 
        print("3. ⚡ 快速演示")
        print("4. 📋 查看音色列表")
        print("5. 👋 退出")
        
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == "1":
            test_cute_voices()
        elif choice == "2":
            interactive_cute_voice_test()
        elif choice == "3":
            quick_demo()
        elif choice == "4":
            list_available_cute_voices()
        elif choice == "5":
            print("bye bye～")
            break
        else:
            print("❌ 无效选择，请重新输入")
        
        if choice != "2":  # 交互式测试有自己的退出机制
            input("\n按回车键继续...")