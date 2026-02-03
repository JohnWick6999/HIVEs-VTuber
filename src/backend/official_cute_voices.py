#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于官方文档的可爱音色配置
使用通义千问TTS的原生参数实现真正的音色定制
"""

# 基于官方参数的可爱音色配置
OFFICIAL_CUTE_VOICES = {
    "傲娇萝莉": {
        "voice": "Cherry",
        "pitch": 1.3,      # 音调提高30%
        "rate": 0.85,      # 语速降低15%（显得更可爱）
        "volume": 60,      # 音量稍微提高
        "seed": 12345,     # 固定种子确保一致性
        "description": "傲娇可爱的小萝莉音色 - 高音调慢语速"
    },
    
    "甜美少女": {
        "voice": "Emily", 
        "pitch": 1.15,
        "rate": 1.0,
        "volume": 55,
        "seed": 23456,
        "description": "温柔甜美的标准少女音色"
    },
    
    "活泼元气": {
        "voice": "Alice",
        "pitch": 1.2,
        "rate": 1.2,       # 语速加快体现活力
        "volume": 65,
        "seed": 34567,
        "description": "充满活力的元气少女音色"
    },
    
    "温柔姐姐": {
        "voice": "Sophia",
        "pitch": 0.9,
        "rate": 0.9,
        "volume": 50,
        "seed": 45678,
        "description": "温柔体贴的姐姐音色 - 低音调慢语速"
    },
    
    "天然呆萌": {
        "voice": "Luna",
        "pitch": 1.4,      # 更高的音调
        "rate": 0.8,       # 更慢的语速
        "volume": 58,
        "seed": 56789,
        "description": "天真可爱的呆萌音色 - 超高音调超慢语速"
    },
    
    "调皮小恶魔": {
        "voice": "Rose",
        "pitch": 1.25,
        "rate": 1.1,
        "volume": 62,
        "seed": 67890,
        "description": "调皮捣蛋的小恶魔音色"
    }
}

# 默认音色
DEFAULT_OFFICIAL_VOICE = "傲娇萝莉"

def get_official_voice_config(voice_name=None):
    """获取基于官方参数的音色配置"""
    if voice_name and voice_name in OFFICIAL_CUTE_VOICES:
        return OFFICIAL_CUTE_VOICES[voice_name]
    return OFFICIAL_CUTE_VOICES[DEFAULT_OFFICIAL_VOICE]

def list_official_cute_voices():
    """列出所有基于官方参数的可爱音色"""
    print("🎀 基于官方参数的可爱音色:")
    print("=" * 40)
    for name, config in OFFICIAL_CUTE_VOICES.items():
        print(f"  🎤 {name}: {config['description']}")
        print(f"     音调: {config['pitch']}, 语速: {config['rate']}, 音量: {config['volume']}")
        print(f"     种子: {config['seed']}")
    print("=" * 40)
    print(f"💡 默认音色: {DEFAULT_OFFICIAL_VOICE}")

def apply_official_voice_to_tts(tts_instance, voice_config):
    """
    将官方音色配置应用到TTS实例
    注意：这需要修改stable_real_time_tts.py来支持这些参数
    """
    print(f"🎀 应用官方音色配置:")
    print(f"   音色: {voice_config['voice']}")
    print(f"   音调: {voice_config['pitch']}")
    print(f"   语速: {voice_config['rate']}")
    print(f"   音量: {voice_config['volume']}")
    print(f"   种子: {voice_config['seed']}")
    
    return voice_config

# 音色应用示例文本
VOICE_DEMO_TEXTS = {
    "傲娇萝莉": [
        "哼！才不是特意为你准备的呢！",
        "要、要加油什么的...才不是关心你啦！"
    ],
    "甜美少女": [
        "今天的天气真好呢，一起出去走走吧～",
        "谢谢你一直以来的陪伴，我很开心哦"
    ],
    "活泼元气": [
        "LET'S GO！今天也要元气满满！",
        "加油加油！没有什么困难能打败我们！"
    ],
    "温柔姐姐": [
        "慢慢来就好，不用太着急的...",
        "累了的话就休息一下吧，我会在这里陪着你的"
    ],
    "天然呆萌": [
        "诶？这个是要这样用的吗？",
        "唔...好像搞错了什么的样子..."
    ],
    "调皮小恶魔": [
        "嘿嘿，让你久等啦～",
        "猜猜我给你准备了什么惊喜？"
    ]
}

if __name__ == "__main__":
    # 测试音色列表
    list_official_cute_voices()