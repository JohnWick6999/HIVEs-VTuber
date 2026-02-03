#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动测试稳定版实时TTS
"""

import sys
import os

# 直接导入，因为我们在正确的目录下
from stable_real_time_tts import StableRealTimeTTS

def auto_test():
    """自动测试函数"""
    print("🚀 自动测试稳定版实时TTS...")
    
    tts_system = StableRealTimeTTS()
    
    # 测试文本
    test_texts = [
        "你好，这是一个实时语音测试。",
        "欢迎使用虚拟主播系统。",
        "今天的天气真不错呢！"
    ]
    
    # 将所有测试文本作为一个列表传递
    print(f"\n📝 开始批量测试 {len(test_texts)} 条文本...")
    success = tts_system.stable_realtime_tts(test_texts)
    if success:
        print(f"✅ 批量测试成功")
    else:
        print(f"❌ 批量测试失败")
        
        # 等待一小段时间
        import time
        time.sleep(1)
    
    print("\n🏁 所有测试完成！")

if __name__ == "__main__":
    auto_test()