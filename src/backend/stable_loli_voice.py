#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
稳定版傲娇萝莉音色系统
基于成功复刻的结果，提供稳定可靠的音色服务
"""

import dashscope
from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
import pyaudio
import base64
import queue
import threading
import time

class StableLoliVoice:
    """稳定版萝莉音色系统"""
    
    def __init__(self):
        # 配置API密钥
        self.api_key = "sk-a5e4d75ae5aa4961acc01d5a71f7b117"
        dashscope.api_key = self.api_key
        
        # 音色参数（经过验证的最佳配置）
        self.voice_params = {
            'voice': 'Cherry',      # 基础音色
            'pitch': 1.6,           # 高音调（萝莉感）
            'rate': 0.6,            # 慢语速（可爱感）
            'volume': 60,           # 适中音量
            'seed': 12345          # 固定种子确保一致性
        }
        
        print("🎯 稳定萝莉音色系统初始化")
        print(f"⚙️  音色参数: {self.voice_params}")
    
    def speak(self, text):
        """让萝莉说话"""
        print(f"🎤 萝莉说: {text}")
        
        try:
            # 音频队列和控制
            audio_queue = queue.Queue()
            is_finished = False
            
            class LoliCallback(QwenTtsRealtimeCallback):
                def on_open(self):
                    print("🌙 萝莉音色连接建立")
                
                def on_event(self, response):
                    if isinstance(response, str):
                        try:
                            response_data = eval(response)
                        except:
                            return
                    else:
                        response_data = response
                        
                    if response_data.get('type') == 'response.audio.delta':
                        audio_data = base64.b64decode(response_data['delta'])
                        audio_queue.put(audio_data)
                
                def on_close(self, code, msg):
                    print("🌙 萝莉音色连接关闭")
            
            def audio_player():
                """音频播放线程"""
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=24000,
                    output=True
                )
                
                while not is_finished or not audio_queue.empty():
                    try:
                        audio_data = audio_queue.get(timeout=0.1)
                        if audio_data:
                            stream.write(audio_data)
                    except queue.Empty:
                        continue
                
                stream.stop_stream()
                stream.close()
                p.terminate()
            
            # 启动播放线程
            player_thread = threading.Thread(target=audio_player, daemon=True)
            player_thread.start()
            
            # 创建TTS连接
            callback = LoliCallback()
            tts = QwenTtsRealtime(
                model='qwen3-tts-flash-realtime-2025-11-27',
                callback=callback,
                url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
            )
            
            # 连接和配置
            tts.connect()
            tts.update_session(
                voice=self.voice_params['voice'],
                response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
                mode='server_commit',
                language_type='Chinese',
                additional_params={
                    'pitch': self.voice_params['pitch'],
                    'rate': self.voice_params['rate'],
                    'volume': self.voice_params['volume'],
                    'seed': self.voice_params['seed']
                }
            )
            
            # 发送文本
            tts.append_text(text)
            
            # 等待处理完成
            time.sleep(max(1.0, len(text) * 0.1))  # 根据文本长度调整等待时间
            tts.finish()
            time.sleep(0.5)
            is_finished = True
            player_thread.join(timeout=3)
            
            print("✅ 萝莉发言完成")
            return True
            
        except Exception as e:
            print(f"❌ 萝莉发言失败: {e}")
            return False
    
    def batch_speak(self, texts):
        """批量说话"""
        print("🎭 萝莉连环发言开始")
        print("=" * 30)
        
        for i, text in enumerate(texts, 1):
            print(f"[{i}/{len(texts)}]")
            success = self.speak(text)
            if not success:
                print(f"⚠️  第{i}句发言失败")
            time.sleep(1)  # 句间间隔
        
        print("🎭 萝莉连环发言结束")

def main():
    """主函数 - 萝莉音色演示"""
    print("🌙 稳定版傲娇萝莉音色演示")
    print("=" * 35)
    
    # 创建萝莉音色系统
    loli = StableLoliVoice()
    
    # 经典傲娇台词测试
    classic_lines = [
        "哼！才不是特意为你准备的呢！",
        "要、要加油什么的...才不是关心你啦！",
        "喵呜～人家才不想理你呢...",
        "讨、讨厌啦！不准这样看着人家！"
    ]
    
    # 逐句测试
    for line in classic_lines[:2]:  # 先测试前两句
        loli.speak(line)
        time.sleep(2)
    
    # 批量测试
    print("\n" + "=" * 35)
    batch_lines = [
        "人家是可爱的小萝莉哦～",
        "今天的天气真好呢！",
        "一起玩游戏吧～"
    ]
    loli.batch_speak(batch_lines)

if __name__ == "__main__":
    main()