#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终极可爱音色测试
测试最夸张的可爱音色效果
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from stable_real_time_tts import StableRealTimeTTS
from super_cute_voices import (
    SUPER_CUTE_VOICES, 
    list_super_cute_voices, 
    get_super_voice_config,
    SUPER_CUTE_QUOTES
)
import time

def ultimate_cute_voice_showcase():
    """终极可爱音色展示"""
    print("🌟 终极可爱音色大赏")
    print("=" * 50)
    print("💫 这里有最夸张、最可爱的音色效果！")
    print("=" * 50)
    
    # 显示所有超级音色
    list_super_cute_voices()
    
    tts = StableRealTimeTTS()
    
    print(f"\n🎤 开始终极可爱音色展示...")
    print("=" * 50)
    
    # 按顺序测试每个音色
    for voice_name, voice_config in SUPER_CUTE_VOICES.items():
        print(f"\n💎 {voice_name}")
        print(f"   📝 {voice_config['description']}")
        print(f"   ⚙️  音调:{voice_config['pitch']}x | 语速:{voice_config['rate']}x | 音量:{voice_config['volume']}")
        print("-" * 40)
        
        # 设置超可爱音色参数
        tts.set_voice_style(voice_config)
        
        # 获取专属台词
        quotes = SUPER_CUTE_QUOTES.get(voice_name, [
            "你好呀～我是可爱的小主播！",
            "今天也要元气满满哦！"
        ])
        
        # 测试2句代表性台词
        for i, quote in enumerate(quotes[:2], 1):
            print(f"[{i}] {quote}")
            
            success = tts.stable_realtime_tts([quote])
            
            if success:
                print(f"   ✨ 效果展示成功")
            else:
                print(f"   ❌ 展示失败")
            
            time.sleep(2)  # 音色间间隔
        
        print(f"💤 准备切换到下一个超可爱音色...")
        time.sleep(3)
    
    print("\n" + "=" * 50)
    print("🎉 终极可爱音色展示完成！")
    print("💝 哪个音色最戳中你的心呢？")

def interactive_ultra_cute_test():
    """交互式超可爱音色测试"""
    print("💬 交互式超可爱音色实验室")
    print("=" * 40)
    
    list_super_cute_voices()
    
    tts = StableRealTimeTTS()
    
    while True:
        print(f"\n请输入你想说的话 (输入 'quit' 退出):")
        user_input = input("💕 你的台词: ").strip()
        
        if user_input.lower() in ['quit', 'exit', '退出']:
            print("✨ 再见啦，记得想我哦～")
            break
            
        if not user_input:
            continue
            
        print("请选择你的专属音色:")
        voice_keys = list(SUPER_CUTE_VOICES.keys())
        for i, voice_name in enumerate(voice_keys, 1):
            config = SUPER_CUTE_VOICES[voice_name]
            print(f"  {i}. {voice_name}")
            print(f"     🎵 音调:{config['pitch']}x 语速:{config['rate']}x")
        
        try:
            choice = int(input("请选择你的style (1-{}): ".format(len(voice_keys)))) - 1
            if 0 <= choice < len(voice_keys):
                selected_voice = voice_keys[choice]
                voice_config = SUPER_CUTE_VOICES[selected_voice]
                
                print(f"\n🎭 激活音色: {selected_voice}")
                print(f"   💝 风格描述: {voice_config['description']}")
                print(f"   ⚙️  技术参数: 音调{voice_config['pitch']}x, 语速{voice_config['rate']}x")
                
                # 应用并播放
                tts.set_voice_style(voice_config)
                success = tts.stable_realtime_tts([user_input])
                
                if success:
                    print("💫 声音魔法发动成功！")
                else:
                    print("💔 魔法似乎失效了...")
            else:
                print("❌ 数字超出范围啦")
        except ValueError:
            print("❌ 请输入正确的数字哦")
        
        time.sleep(1)

def extreme_parameter_demo():
    """极限参数效果演示"""
    print("🎛️  极限音色参数实验室")
    print("=" * 35)
    
    tts = StableRealTimeTTS()
    
    # 极限参数对比测试
    extreme_tests = [
        {
            "name": "_baseline_ 标准参数",
            "params": {"pitch": 1.0, "rate": 1.0, "volume": 50, "voice": "Cherry"}
        },
        {
            "name": "🌟 超高音调测试",
            "params": {"pitch": 1.8, "rate": 1.0, "volume": 60, "voice": "Cherry"}
        },
        {
            "name": "🐌 超慢语速测试", 
            "params": {"pitch": 1.0, "rate": 0.5, "volume": 60, "voice": "Cherry"}
        },
        {
            "name": "💫 综合超可爱",
            "params": {"pitch": 1.6, "rate": 0.6, "volume": 65, "voice": "Cherry"}
        },
        {
            "name": "👑 终极傲娇公主",
            "params": {"pitch": 1.7, "rate": 0.5, "volume": 70, "voice": "Cherry"}
        }
    ]
    
    test_sentence = "人家才不是故意要这样的呢！"
    
    for test in extreme_tests:
        print(f"\n🔬 {test['name']}:")
        print(f"   参数: {test['params']}")
        
        tts.set_voice_style(test['params'])
        success = tts.stable_realtime_tts([test_sentence])
        
        if success:
            print("   ✅ 极限效果达成")
        else:
            print("   ❌ 参数可能超出范围")
        
        time.sleep(3)

def cute_voice_battle():
    """可爱音色对决"""
    print("⚔️  可爱情感大对决")
    print("=" * 30)
    
    tts = StableRealTimeTTS()
    battle_quote = "哼！才不想承认你喜欢我呢！"
    
    contenders = ["傲娇小公主", "软萌小奶音", "腹黑小恶魔"]
    
    print("🎤 今日对决选手:")
    for i, name in enumerate(contenders, 1):
        print(f"  {i}. {name}")
    
    print(f"\n⚔️  对决台词: {battle_quote}")
    print("-" * 30)
    
    for voice_name in contenders:
        voice_config = SUPER_CUTE_VOICES[voice_name]
        print(f"\n💎 {voice_name} 出场!")
        print(f"   风格: {voice_config['description']}")
        
        tts.set_voice_style(voice_config)
        success = tts.stable_realtime_tts([battle_quote])
        
        if success:
            print(f"   ✨ {voice_name} 的魅力爆发!")
        else:
            print(f"   😔 {voice_name} 状态不佳...")
        
        time.sleep(2)

if __name__ == "__main__":
    print("🎀 欢迎来到超可爱音色实验室！")
    print("💝 这里有世界上最可爱的音色等着你～")
    
    while True:
        print("\n请选择实验项目:")
        print("1. 🌟 终极可爱音色展示")
        print("2. 💬 交互式超可爱测试")
        print("3. 🎛️  极限参数实验室")
        print("4. ⚔️  可爱情感大对决")
        print("5. 📋 查看所有音色")
        print("6. 👋 离开可爱实验室")
        
        choice = input("\n请选择你的冒险 (1-6): ").strip()
        
        if choice == "1":
            ultimate_cute_voice_showcase()
        elif choice == "2":
            interactive_ultra_cute_test()
        elif choice == "3":
            extreme_parameter_demo()
        elif choice == "4":
            cute_voice_battle()
        elif choice == "5":
            list_super_cute_voices()
        elif choice == "6":
            print("💕 再见啦，要记得回来看我哦～")
            break
        else:
            print("❌ 选择错误，请输入1-6之间的数字")
        
        if choice not in ["2", "6"]:  # 交互式测试有自己的退出机制
            input("\n按回车键继续探索...")