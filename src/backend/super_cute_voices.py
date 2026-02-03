#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超级可爱的音色配置
专门为傲娇萝莉风格定制的音色参数
"""

# 超级可爱的音色配置 - 更夸张的参数
SUPER_CUTE_VOICES = {
    "傲娇小公主": {
        "voice": "Cherry",
        "pitch": 1.5,      # 超高音调
        "rate": 0.7,       # 超慢语速
        "volume": 65,      # 稍大声
        "seed": 99999,     # 特殊种子
        "description": "👑 傲娇小公主 - 超高音调超慢语速，满满的公主范儿"
    },
    
    "软萌小奶音": {
        "voice": "Emily",
        "pitch": 1.6,      # 极高音调
        "rate": 0.6,       # 极慢语速
        "volume": 60,
        "seed": 88888,
        "description": "🍼 软萌小奶音 - 像小朋友一样的超萌音色"
    },
    
    "电波少女": {
        "voice": "Alice",
        "pitch": 1.4,
        "rate": 0.8,
        "volume": 70,      # 更大声
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

# 默认音色 - 最可爱的那个
DEFAULT_SUPER_VOICE = "软萌小奶音"

def get_super_voice_config(voice_name=None):
    """获取超级可爱的音色配置"""
    if voice_name and voice_name in SUPER_CUTE_VOICES:
        return SUPER_CUTE_VOICES[voice_name]
    return SUPER_CUTE_VOICES[DEFAULT_SUPER_VOICE]

def list_super_cute_voices():
    """列出所有超级可爱的音色"""
    print("🎀 超级可爱音色大赏:")
    print("=" * 50)
    for name, config in SUPER_CUTE_VOICES.items():
        print(f"  🌟 {name}: {config['description']}")
        print(f"     音调: {config['pitch']}x (超高!)")
        print(f"     语速: {config['rate']}x (超慢!)")
        print(f"     音量: {config['volume']}")
        print(f"     种子: {config['seed']}")
        print()
    print("=" * 50)
    print(f"💖 推荐默认: {DEFAULT_SUPER_VOICE}")

def apply_super_voice_to_tts(tts_instance, voice_config):
    """应用超级音色配置"""
    print(f"🎀 应用超级音色配置:")
    print(f"   音色: {voice_config['voice']}")
    print(f"   音调: {voice_config['pitch']}x (超高音调)")
    print(f"   语速: {voice_config['rate']}x (超慢语速)")
    print(f"   音量: {voice_config['volume']}")
    print(f"   种子: {voice_config['seed']}")
    
    return voice_config

# 专门的傲娇台词库
SUPER_CUTE_QUOTES = {
    "傲娇小公主": [
        "哼！本 princess 才不屑和你说话呢！",
        "喂！不准用那种眼神看着本 princess 啦！",
        "讨、讨厌啦！才不是为了你才这么做的呢！"
    ],
    "软萌小奶音": [
        "咿呀...人家、人家才不想理你呢...",
        "呜哇...不要这样嘛...好害羞的说...",
        "那个...可不可以...轻轻地...抱一下下就好..."
    ],
    "电波少女": [
        "哔哔！检测到可疑生物接近中！",
        "警告警告！心情指数正在急剧上升！",
        "系统错误！无法抑制想要撒娇的冲动！"
    ],
    "害羞小鹿": [
        "那、那个...请问...可以...陪我聊聊天吗？",
        "好、好紧张呢...第一次和陌生人说话...",
        "如、如果打扰到你的话...我就悄悄离开..."
    ],
    "元气JK": [
        "よし！今日も元気いっぱいがんばるぞ～！",
        "先輩！一緒に帰ろうよ～お夕飯作ってあげるね♪",
        "えへへ～ちょっとだけ休憩しようかしら？"
    ],
    "腹黑小恶魔": [
        "哎呀呀...真是个有趣的提议呢...",
        "呵呵呵...你以为我会轻易答应吗？",
        "呐呐...要不要来玩个游戏？输了的人要听我的哦～"
    ]
}

if __name__ == "__main__":
    # 测试音色列表
    list_super_cute_voices()