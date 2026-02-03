#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速音频完整性验证测试
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from stable_real_time_tts import StableRealTimeTTS
import time

def quick_verification_test():
    """快速验证测试"""
    print("⚡ 快速音频完整性验证")
    print("=" * 30)
    
    tts = StableRealTimeTTS()
    
    # 简单测试文本
    test_text = "你好，这是一个完整性测试。"
    print(f"📝 测试文本: {test_text}")
    print(f"📏 长度: {len(test_text)} 字符")
    
    start_time = time.time()
    
    # 执行TTS
    success = tts.stable_realtime_tts([test_text])
    
    end_time = time.time()
    actual_duration = end_time - start_time
    
    if success:
        print(f"✅ 播放成功")
        print(f"⏱️  实际耗时: {actual_duration:.2f}秒")
        
        # 预期时长计算
        expected_duration = len(test_text) / 3.0  # 中文每秒3字
        print(f"📊 预期时长: {expected_duration:.2f}秒")
        
        # 判断完整性
        if actual_duration >= expected_duration * 0.7:  # 至少70%的时间
            print("🎯 音频播放完整 ✓")
            return True
        else:
            print("⚠️  音频可能被截断 ✗")
            return False
    else:
        print("❌ 播放失败")
        return False

def comparison_test():
    """对比测试 - 测试不同长度文本"""
    print("\n⚖️  对比测试")
    print("=" * 30)
    
    tts = StableRealTimeTTS()
    
    test_cases = [
        ("短文本", "你好"),
        ("中等文本", "欢迎使用虚拟主播系统"),
        ("长文本", "今天天气非常好，适合外出活动，虚拟主播技术也越来越成熟了")
    ]
    
    results = []
    
    for name, text in test_cases:
        print(f"\n📋 {name}: {text}")
        
        start_time = time.time()
        success = tts.stable_realtime_tts([text])
        end_time = time.time()
        
        if success:
            actual_time = end_time - start_time
            expected_time = len(text) / 3.0
            ratio = actual_time / expected_time if expected_time > 0 else 0
            
            print(f"   实际: {actual_time:.2f}s, 预期: {expected_time:.2f}s, 比率: {ratio:.2f}")
            
            is_complete = ratio >= 0.7
            status = "✓" if is_complete else "✗"
            print(f"   完整性: {status}")
            
            results.append(is_complete)
        else:
            print("   ❌ 播放失败")
            results.append(False)
    
    # 总结
    complete_count = sum(results)
    total_count = len(results)
    
    print(f"\n📊 总结: {complete_count}/{total_count} 通过完整性测试")
    if complete_count == total_count:
        print("🎉 所有测试通过！音频截断问题已解决。")
        return True
    else:
        print("⚠️  部分测试仍有问题。")
        return False

if __name__ == "__main__":
    print("🚀 开始音频完整性验证...")
    
    # 快速验证
    quick_result = quick_verification_test()
    
    # 对比测试
    comparison_result = comparison_test()
    
    # 最终结论
    print("\n" + "=" * 30)
    print("📋 最终结论")
    print("=" * 30)
    
    if quick_result and comparison_result:
        print("✅ 音频截断问题已成功修复！")
        print("✅ 现在可以正常使用实时TTS功能。")
    else:
        print("⚠️  音频完整性仍需进一步优化。")
    
    print("🏁 测试完成！")