#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可爱的音色配置
提供多种萌系音色选择
"""

# 可爱音色配置
CUTE_VOICES = {
    "傲娇萝莉": {
        "voice": "Cherry",
        "pitch": 1.2,      # 音调提高
        "speed": 0.9,      # 语速稍慢
        "emotion": "happy", # 开心情绪
        "description": "傲娇可爱的小萝莉音色"
    },
    
    "甜美少女": {
        "voice": "Emily",
        "pitch": 1.1,
        "speed": 1.0,
        "emotion": "gentle",
        "description": "温柔甜美的少女音色"
    },
    
    "活泼元气": {
        "voice": "Alice",
        "pitch": 1.15,
        "speed": 1.1,
        "emotion": "excited",
        "description": "充满活力的元气音色"
    },
    
    "温柔姐姐": {
        "voice": "Sophia",
        "pitch": 0.95,
        "speed": 0.9,
        "emotion": "warm",
        "description": "温柔体贴的姐姐音色"
    },
    
    "天然呆萌": {
        "voice": "Luna",
        "pitch": 1.25,
        "speed": 0.85,
        "emotion": "innocent",
        "description": "天真可爱的呆萌音色"
    }
}

# 默认音色
DEFAULT_CUTE_VOICE = "傲娇萝莉"

def get_cute_voice_config(voice_name=None):
    """获取可爱的音色配置"""
    if voice_name and voice_name in CUTE_VOICES:
        return CUTE_VOICES[voice_name]
    return CUTE_VOICES[DEFAULT_CUTE_VOICE]

def list_available_cute_voices():
    """列出所有可用的可爱音色"""
    print("🎀 可用的可爱音色:")
    print("=" * 30)
    for name, config in CUTE_VOICES.items():
        print(f"  🎤 {name}: {config['description']}")
        print(f"     音调: {config['pitch']}, 语速: {config['speed']}")
    print("=" * 30)
    print(f"💡 默认音色: {DEFAULT_CUTE_VOICE}")

def apply_cute_voice_settings(tts_instance, voice_name=None):
    """应用可爱的音色设置到TTS实例"""
    config = get_cute_voice_config(voice_name)
    
    # 应用音色设置（如果TTS支持的话）
    settings = {
        'voice': config['voice'],
        'pitch': config['pitch'],
        'speed': config['speed']
    }
    
    print(f"🎀 应用音色: {voice_name or DEFAULT_CUTE_VOICE}")
    print(f"   配置: {settings}")
    
    return settings

if __name__ == "__main__":
    # 测试音色列表
    list_available_cute_voices()