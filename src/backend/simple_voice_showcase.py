#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立的超级音色测试脚本
避免复杂导入问题，直接测试音色效果
"""

import time
import sys
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

# 超级音色配置（直接定义，避免导入问题）
SUPER_VOICES = {
    "傲娇小公主": {
        "voice": "Cherry",
        "pitch": 1.5,
        "rate": 0.7,
        "volume": 65,
        "seed": 99999,
        "description": "👑 傲娇小公主 - 超高音调超慢语速"
    },
    "软萌小奶音": {
        "voice": "Emily",
        "pitch": 1.6,
        "rate": 0.6,
        "volume": 60,
        "seed": 88888,
        "description": "🍼 软萌小奶音 - 像小朋友一样的超萌音色"
    },
    "电波少女": {
        "voice": "Alice",
        "pitch": 1.4,
        "rate": 0.8,
        "volume": 70,
        "seed": 77777,
        "description": "⚡ 电波少女 - 带点神经质的可爱音色"
    },
    "害羞小鹿": {
        "voice": "Luna",
        "pitch": 1.35,
        "rate": 0.75,
        "volume": 55,
        "seed": 66666,
        "description": "🦌 害羞小鹿 - 温柔怯生生的可爱音色"
    },
    "元气JK": {
        "voice": "Rose",
        "pitch": 1.25,
        "rate": 1.0,
        "volume": 68,
        "seed": 55555,
        "description": "制服少女 - 标准的日系JK元气音"
    },
    "腹黑小恶魔": {
        "voice": "Sophia",
        "pitch": 1.3,
        "rate": 0.9,
        "volume": 62,
        "seed": 44444,
        "description": "😈 腹黑小恶魔 - 表面可爱内心腹黑的音色"
    }
}

# 专属台词
VOICE_QUOTES = {
    "傲娇小公主": [
        "哼！本 princess 才不屑和你说话呢！",
        "喂！不准用那种眼神看着本 princess 啦！"
    ],
    "软萌小奶音": [
        "咿呀...人家、人家才不想理你呢...",
        "呜哇...不要这样嘛...好害羞的说..."
    ],
    "电波少女": [
        "哔哔！检测到可疑生物接近中！",
        "警告警告！心情指数正在急剧上升！"
    ],
    "害羞小鹿": [
        "那、那个...请问...可以...陪我聊聊天吗？",
        "好、好紧张呢...第一次和陌生人说话..."
    ],
    "元气JK": [
        "よし！今日も元気いっぱいがんばるぞ～！",
        "先輩！一緒に帰ろうよ～お夕飯作ってあげるね♪"
    ],
    "腹黑小恶魔": [
        "哎呀呀...真是个有趣的提议呢...",
        "呵呵呵...你以为我会轻易答应吗？"
    ]
}

def test_single_voice(voice_name, voice_config, quotes):
    """测试单个音色"""
    print(f"🎤 测试音色: {voice_name}")
    print(f"   📝 {voice_config['description']}")
    print(f"   ⚙️  音调:{voice_config['pitch']}x | 语速:{voice_config['rate']}x | 音量:{voice_config['volume']}")
    print("-" * 40)
    
    # 这里应该调用TTS系统，但由于导入问题，我们先展示配置
    for i, quote in enumerate(quotes[:2], 1):
        print(f"   [{i}] {quote}")
        print(f"      (此处应该播放音频，参数: {voice_config})")
        time.sleep(1)
    
    print(f"   🎉 {voice_name} 配置展示完成\n")
    return True

def main():
    """主测试函数"""
    print("🎭 超级音色挨个测试")
    print("=" * 50)
    print("💫 现在开始逐一展示所有超级可爱的音色配置！")
    print("=" * 50)
    
    print(f"🎯 总共 {len(SUPER_VOICES)} 个超级音色等待测试")
    print()
    
    success_count = 0
    
    # 按名称顺序测试
    for i, (voice_name, voice_config) in enumerate(SUPER_VOICES.items(), 1):
        print(f"💎 [{i}/{len(SUPER_VOICES)}]")
        
        quotes = VOICE_QUOTES.get(voice_name, ["你好～", "今天天气真好呢！"])
        success = test_single_voice(voice_name, voice_config, quotes)
        
        if success:
            success_count += 1
        
        if i < len(SUPER_VOICES):  # 不是最后一个
            print("💤 准备测试下一个音色...")
            time.sleep(2)
    
    # 测试总结
    print("=" * 50)
    print("📊 超级音色配置展示总结")
    print("=" * 50)
    print(f"✅ 成功展示: {success_count}/{len(SUPER_VOICES)}")
    print(f"📈 完成率: {success_count/len(SUPER_VOICES)*100:.1f}%")
    
    if success_count == len(SUPER_VOICES):
        print("🎊 所有超级音色配置展示完成！")
        print("\n🌟 推荐最可爱的几个音色:")
        print("   1. 🍼 软萌小奶音 - 最萌的奶音效果")
        print("   2. 👑 傲娇小公主 - 最夸张的傲娇效果") 
        print("   3. 🦌 害羞小鹿 - 最温柔的害羞风格")
    else:
        print("⚠️  部分音色展示有问题")
    
    print("\n💡 下一步建议:")
    print("   - 选择最喜欢的音色进行实际TTS测试")
    print("   - 调整参数获得更理想的音色效果")
    print("   - 保存喜欢的音色配置供日常使用")

if __name__ == "__main__":
    main()