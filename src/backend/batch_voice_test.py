#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超级音色挨个测试脚本
逐一测试所有超级可爱的音色效果
"""

import sys
import os
from pathlib import Path
import time

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 直接导入，避免相对导入问题
import stable_real_time_tts
import super_cute_voices
import voice_preset_manager

def batch_test_all_super_voices():
    """批量测试所有超级音色"""
    print("🎭 超级音色批量测试开始")
    print("=" * 50)
    print("💫 现在开始逐一测试所有超级可爱的音色！")
    print("=" * 50)
    
    tts = stable_real_time_tts.StableRealTimeTTS()
    
    # 获取所有超级音色
    super_voices = {k: v for k, v in voice_preset_manager.voice_manager.presets.items() if v["type"] == "super"}
    
    print(f"🎯 总共找到 {len(super_voices)} 个超级音色需要测试")
    print()
    
    test_results = []
    
    for i, (voice_name, preset) in enumerate(super_voices.items(), 1):
        config = preset["config"]
        print(f"🎤 [{i}/{len(super_voices)}] 测试音色: {voice_name}")
        print(f"   📝 描述: {config['description']}")
        print(f"   ⚙️  参数: 音调{config['pitch']}x | 语速{config['rate']}x | 音量{config['volume']}")
        print("-" * 40)
        
        # 设置音色
        tts.set_voice_style(config)
        
        # 获取测试台词
        clean_name = voice_name.replace("超级_", "")
        quotes = super_cute_voices.SUPER_CUTE_QUOTES.get(clean_name, [
            "你好呀～人家是可爱的小主播！",
            "今天也要开开心心的呢！"
        ])
        
        # 测试2句代表性的台词
        voice_success = True
        for j, quote in enumerate(quotes[:2], 1):
            print(f"   [{j}] {quote}")
            
            try:
                success = tts.stable_realtime_tts([quote])
                if success:
                    print(f"      ✨ 播放成功")
                else:
                    print(f"      ❌ 播放失败")
                    voice_success = False
            except Exception as e:
                print(f"      ❌ 播放异常: {e}")
                voice_success = False
            
            time.sleep(1.5)  # 台词间隔
        
        # 记录测试结果
        test_results.append({
            "name": voice_name,
            "success": voice_success,
            "config": config
        })
        
        if voice_success:
            print(f"   🎉 {voice_name} 测试通过")
        else:
            print(f"   ⚠️  {voice_name} 测试有问题")
        
        print(f"💤 准备测试下一个音色...")
        time.sleep(2)
        print()
    
    # 输出测试总结
    print("=" * 50)
    print("📊 超级音色测试总结")
    print("=" * 50)
    
    successful = sum(1 for r in test_results if r["success"])
    total = len(test_results)
    
    print(f"✅ 成功测试: {successful}/{total}")
    print(f"📈 成功率: {successful/total*100:.1f}%")
    
    if successful == total:
        print("🎊 所有超级音色测试通过！")
    else:
        print("⚠️  部分音色存在问题")
    
    print("\n📋 详细结果:")
    for result in test_results:
        status = "✅" if result["success"] else "❌"
        print(f"  {status} {result['name']}")
    
    return test_results

def main():
    """主函数"""
    print("🎀 欢迎来到超级音色测试实验室！")
    print("💫 现在开始挨个测试所有超级可爱的音色～")
    
    # 直接运行批量测试
    batch_test_all_super_voices()

if __name__ == "__main__":
    main()
