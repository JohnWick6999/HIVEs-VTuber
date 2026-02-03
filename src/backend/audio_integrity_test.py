#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音截断问题测试
专门测试音频播放完整性
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from stable_real_time_tts import StableRealTimeTTS
import time

def test_audio_completeness():
    """测试音频播放完整性"""
    print("🎵 音频完整性测试")
    print("=" * 40)
    
    tts = StableRealTimeTTS()
    
    # 测试不同长度的文本
    test_cases = [
        ("短句测试", "你好世界"),
        ("中等长度", "欢迎使用虚拟主播系统，这是一个实时语音测试。"),
        ("较长文本", "今天天气真不错，阳光明媚，非常适合出门散步。虚拟主播技术越来越成熟，能够提供流畅自然的语音交互体验。"),
        ("完整句子", "非常感谢您的关注和支持，我们会继续努力改进系统性能，为您提供更好的服务体验。")
    ]
    
    results = []
    
    for case_name, text in test_cases:
        print(f"\n📋 测试用例: {case_name}")
        print(f"📝 文本内容: {text}")
        print(f"📏 文本长度: {len(text)} 字符")
        
        start_time = time.time()
        
        # 播放音频
        success = tts.stable_realtime_tts([text])
        
        end_time = time.time()
        duration = end_time - start_time
        
        if success:
            print(f"✅ 播放成功")
            print(f"⏱️  播放耗时: {duration:.2f}秒")
            # 估算应该的播放时间（中文约每秒3字）
            expected_duration = len(text) / 3.0
            print(f"📊 预期时长: {expected_duration:.2f}秒")
            print(f"📈 效率比: {expected_duration/duration:.2f}")
            
            # 判断是否完整播放
            if duration >= expected_duration * 0.8:  # 至少80%的时间
                print("🎯 音频播放完整")
                results.append((case_name, True, duration))
            else:
                print("⚠️  音频可能被截断")
                results.append((case_name, False, duration))
        else:
            print("❌ 播放失败")
            results.append((case_name, False, 0))
        
        # 等待间隔
        time.sleep(1)
    
    # 输出总结
    print("\n" + "=" * 40)
    print("📊 测试总结")
    print("=" * 40)
    
    successful_tests = sum(1 for _, success, _ in results if success)
    total_tests = len(results)
    
    print(f"✅ 成功测试: {successful_tests}/{total_tests}")
    print(f"成功率: {successful_tests/total_tests*100:.1f}%")
    
    if successful_tests == total_tests:
        print("🎉 所有测试通过！音频截断问题已解决。")
    else:
        print("⚠️  部分测试存在问题，需要进一步优化。")
    
    # 详细结果
    print("\n📋 详细结果:")
    for case_name, success, duration in results:
        status = "✅" if success else "❌"
        print(f"  {status} {case_name}: {duration:.2f}秒")

def test_continuous_playback():
    """测试连续播放场景"""
    print("\n🎵 连续播放测试")
    print("=" * 40)
    
    tts = StableRealTimeTTS()
    
    continuous_texts = [
        "这是第一句话。",
        "这是第二句话。",
        "这是第三句话。",
        "这是最后一句话，比较长一些用来测试完整性。"
    ]
    
    print("开始连续播放测试...")
    start_time = time.time()
    
    success = tts.stable_realtime_tts(continuous_texts)
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    if success:
        print(f"✅ 连续播放成功")
        print(f"⏱️  总耗时: {total_duration:.2f}秒")
        print(f"📊 平均每句: {total_duration/len(continuous_texts):.2f}秒")
    else:
        print("❌ 连续播放失败")

if __name__ == "__main__":
    print("🚀 开始音频完整性测试...")
    
    # 运行完整性测试
    test_audio_completeness()
    
    # 运行连续播放测试
    test_continuous_playback()
    
    print("\n🏁 所有测试完成！")