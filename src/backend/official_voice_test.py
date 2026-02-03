#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
官方音色参数测试
基于通义千问官方文档实现的真正自定义音色
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from stable_real_time_tts import StableRealTimeTTS
from official_cute_voices import (
    OFFICIAL_CUTE_VOICES, 
    list_official_cute_voices, 
    get_official_voice_config,
    VOICE_DEMO_TEXTS
)
import time

def test_official_voice_parameters():
    """测试官方音色参数效果"""
    print("🎯 官方音色参数测试")
    print("=" * 40)
    
    # 显示所有可用音色
    list_official_cute_voices()
    
    # 创建TTS实例
    tts = StableRealTimeTTS()
    
    print(f"\n🎤 开始官方音色测试...")
    print("=" * 40)
    
    # 测试每个音色
    for voice_name, voice_config in OFFICIAL_CUTE_VOICES.items():
        print(f"\n🌟 测试音色: {voice_name}")
        print(f"   描述: {voice_config['description']}")
        print(f"   参数: 音调={voice_config['pitch']}, 语速={voice_config['rate']}, 音量={voice_config['volume']}")
        print("-" * 30)
        
        # 设置音色参数
        tts.set_voice_style(voice_config)
        
        # 获取对应的测试文本
        demo_texts = VOICE_DEMO_TEXTS.get(voice_name, [
            "你好，我是虚拟主播。",
            "很高兴认识你！"
        ])
        
        # 测试前两句
        test_texts = demo_texts[:2] if len(demo_texts) >= 2 else demo_texts
        
        for i, text in enumerate(test_texts, 1):
            print(f"[{i}] {text}")
            
            success = tts.stable_realtime_tts([text])
            
            if success:
                print(f"   ✅ 播放成功")
            else:
                print(f"   ❌ 播放失败")
            
            # 音色间间隔
            time.sleep(2)
        
        print(f"💤 切换到下一个音色...")
        time.sleep(3)
    
    print("\n" + "=" * 40)
    print("🎉 官方音色参数测试完成！")
    print("现在支持真正的音调、语速、音量调节！")

def interactive_official_voice_test():
    """交互式官方音色测试"""
    print("💬 交互式官方音色测试")
    print("=" * 30)
    
    list_official_cute_voices()
    
    tts = StableRealTimeTTS()
    
    while True:
        print(f"\n请输入要测试的内容 (输入 'quit' 退出):")
        user_input = input("🗣️  您要说: ").strip()
        
        if user_input.lower() in ['quit', 'exit', '退出']:
            print("👋 再见啦～")
            break
            
        if not user_input:
            continue
            
        print("请选择音色风格:")
        voice_keys = list(OFFICIAL_CUTE_VOICES.keys())
        for i, voice_name in enumerate(voice_keys, 1):
            config = OFFICIAL_CUTE_VOICES[voice_name]
            print(f"  {i}. {voice_name} (音调:{config['pitch']}, 语速:{config['rate']})")
        
        try:
            choice = int(input("请选择 (1-{}): ".format(len(voice_keys)))) - 1
            if 0 <= choice < len(voice_keys):
                selected_voice = voice_keys[choice]
                voice_config = OFFICIAL_CUTE_VOICES[selected_voice]
                
                print(f"\n🎭 使用音色: {selected_voice}")
                print(f"   参数详情: {voice_config}")
                
                # 设置并应用音色
                tts.set_voice_style(voice_config)
                
                success = tts.stable_realtime_tts([user_input])
                
                if success:
                    print("✅ 播放完成")
                else:
                    print("❌ 播放失败")
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入数字")
        
        time.sleep(1)

def parameter_effect_demo():
    """音色参数效果演示"""
    print("🎛️  音色参数效果演示")
    print("=" * 30)
    
    tts = StableRealTimeTTS()
    base_text = "测试音色参数效果"
    
    # 对比不同参数的效果
    parameter_tests = [
        {
            "name": "标准参数",
            "params": {"pitch": 1.0, "rate": 1.0, "volume": 50, "voice": "Cherry"}
        },
        {
            "name": "傲娇萝莉风格",
            "params": {"pitch": 1.3, "rate": 0.85, "volume": 60, "voice": "Cherry"}
        },
        {
            "name": "天然呆萌风格", 
            "params": {"pitch": 1.4, "rate": 0.8, "volume": 58, "voice": "Luna"}
        },
        {
            "name": "活泼元气风格",
            "params": {"pitch": 1.2, "rate": 1.2, "volume": 65, "voice": "Alice"}
        }
    ]
    
    for test in parameter_tests:
        print(f"\n🎤 {test['name']}:")
        print(f"   参数: {test['params']}")
        
        tts.set_voice_style(test['params'])
        success = tts.stable_realtime_tts([base_text])
        
        if success:
            print("   ✅ 效果演示完成")
        else:
            print("   ❌ 演示失败")
        
        time.sleep(3)

if __name__ == "__main__":
    print("🎯 欢迎使用官方音色参数测试！")
    
    while True:
        print("\n请选择测试模式:")
        print("1. 🎭 完整官方音色测试")
        print("2. 💬 交互式参数测试")
        print("3. 🎛️  参数效果对比")
        print("4. 📋 查看音色列表")
        print("5. 👋 退出")
        
        choice = input("\n请选择 (1-5): ").strip()
        
        if choice == "1":
            test_official_voice_parameters()
        elif choice == "2":
            interactive_official_voice_test()
        elif choice == "3":
            parameter_effect_demo()
        elif choice == "4":
            list_official_cute_voices()
        elif choice == "5":
            print("bye bye～")
            break
        else:
            print("❌ 无效选择，请重新输入")
        
        if choice != "2":  # 交互式测试有自己的退出机制
            input("\n按回车键继续...")