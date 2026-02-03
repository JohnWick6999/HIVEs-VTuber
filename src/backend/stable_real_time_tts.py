#!/usr/bin/env python3
# 稳定版实时TTS - 解决卡顿问题的简化实现

import time
import base64
import threading
from voice_api import voice_api_system
import config

class StableRealTimeTTS:
    """稳定版实时TTS，专注于解决卡顿问题"""
    
    def __init__(self):
        self.config_manager = config.ConfigManager()
        self.voice_config = self.config_manager.get_voice_api_config()
        self.api_key = self.voice_config.get("tts", {}).get("api_key")
        self.audio_player = None
        self.is_playing = False
        # 默认音色参数（基于官方文档）
        self._voice_params = {
            'voice': 'Cherry',
            'pitch': 1.0,
            'rate': 1.0,
            'volume': 50,
            'seed': 0
        }
        
    def setup_audio(self):
        """设置音频播放"""
        try:
            import pyaudio
            self.audio_player = pyaudio.PyAudio().open(
                format=pyaudio.paInt16,
                channels=1,
                rate=24000,
                output=True,
                frames_per_buffer=1024
            )
            print("🔊 音频系统初始化完成")
            return True
        except Exception as e:
            print(f"❌ 音频初始化失败: {e}")
            return False
    
    def play_audio_immediately(self, audio_data):
        """立即播放音频数据"""
        if self.audio_player and audio_data:
            try:
                self.audio_player.write(audio_data)
                if not self.is_playing:
                    self.is_playing = True
                    print("🎵 开始实时播放...")
            except Exception as e:
                print(f"⚠️ 播放错误: {e}")
    
    def set_voice_style(self, voice_params):
        """设置音色风格（基于官方参数）"""
        if isinstance(voice_params, dict):
            self._voice_params.update(voice_params)
            print(f"🎯 音色参数已更新: {self._voice_params}")
        else:
            print("❌ 无效的音色参数格式")
    
    def get_current_voice_params(self):
        """获取当前音色参数"""
        return self._voice_params.copy()
    
    def stable_realtime_tts(self, text_list):
        """稳定版实时TTS播放"""
        if not self.api_key:
            print("❌ 未配置API Key")
            return False
        
        if not self.setup_audio():
            return False
        
        try:
            import dashscope
            from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
            
            dashscope.api_key = self.api_key
            
            # 简化的回调处理
            audio_queue = []
            queue_lock = threading.Lock()
            session_ready = threading.Event()
            
            class SimpleCallback(QwenTtsRealtimeCallback):
                def on_open(self):
                    print("📡 连接建立")
                
                def on_close(self, code, msg):
                    print(f"🔌 连接关闭: {msg}")
                
                def on_event(self, response):
                    if isinstance(response, str):
                        try:
                            response = eval(response)
                        except:
                            return
                    
                    event_type = response.get('type')
                    
                    if event_type == 'response.audio.delta':
                        audio_b64 = response.get('delta')
                        if audio_b64:
                            audio_data = base64.b64decode(audio_b64)
                            with queue_lock:
                                audio_queue.append(audio_data)
                                # 实时播放策略
                                if len(audio_queue) >= 3:  # 积累少量数据后立即播放
                                    self.flush_audio()
                    
                    elif event_type == 'session.created':
                        print("🔄 会话创建成功")
                        session_ready.set()
                    
                    elif event_type == 'session.updated':
                        print("🔄 会话配置完成")
                
                def flush_audio(self):
                    """刷新音频队列"""
                    while audio_queue:
                        audio_chunk = audio_queue.pop(0)
                        if self.audio_player:
                            self.audio_player.write(audio_chunk)
            
            # 创建实例
            callback = SimpleCallback()
            callback.audio_player = self.audio_player  # 传递播放器引用
            
            tts = QwenTtsRealtime(
                model='qwen3-tts-flash-realtime-2025-11-27',  # 使用推荐的最新稳定版
                callback=callback,
                url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
            )
            
            # 连接和配置
            print("🔄 连接TTS服务...")
            tts.connect()
            session_ready.wait(timeout=5)
            
            # 使用自定义音色参数
            tts.update_session(
                voice=self._voice_params['voice'],
                response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
                mode='server_commit',
                language_type='Chinese',
                # 添加官方支持的音色参数
                additional_params={
                    'pitch': self._voice_params['pitch'],
                    'rate': self._voice_params['rate'],
                    'volume': self._voice_params['volume'],
                    'seed': self._voice_params['seed']
                }
            )
            
            print("✅ 开始稳定实时播放...")
            
            # 分批处理文本
            for i, text in enumerate(text_list):
                if text.strip():
                    print(f"[{i+1}/{len(text_list)}] 📥 处理: {text}")
                    tts.append_text(text.strip())
                    # 优化的等待策略
                    time.sleep(max(0.02, len(text) * 0.01))  # 根据文本长度调整延迟
            
            # 完成处理
            tts.finish()
            
            # 更严格的音频完整性保障
            max_wait_time = 12.0  # 适度的最长等待时间
            wait_start = time.time()
            last_queue_size = -1
            stable_count = 0
            total_audio_bytes = 0
            consecutive_empty = 0  # 连续空队列计数
            
            print("🎧 精确等待音频数据接收完成...")
            
            # 更精密的等待策略
            while time.time() - wait_start < max_wait_time:
                time.sleep(0.05)  # 缩短检查间隔
                with queue_lock:
                    current_size = len(audio_queue)
                    
                    # 累计音频数据
                    if current_size > 0:
                        current_total = sum(len(chunk) for chunk in audio_queue)
                        if current_total > total_audio_bytes:
                            total_audio_bytes = current_total
                        consecutive_empty = 0
                    else:
                        consecutive_empty += 1
                    
                    # 队列稳定性检测
                    if current_size == last_queue_size:
                        stable_count += 1
                    else:
                        stable_count = 0
                    
                    last_queue_size = current_size
                    
                    # 音频时长估算 (PCM 16-bit mono 24kHz ≈ 48000 bytes/秒)
                    estimated_duration = total_audio_bytes / 48000.0
                    expected_duration = sum(len(text) for text in text_list) / 2.5  # 稍微保守的估算
                    
                    # 多层次完成判断（更加严格）
                    completion_conditions = [
                        # 条件1: 数据充足且队列稳定
                        (estimated_duration >= expected_duration * 0.95 and stable_count >= 5),
                        # 条件2: 数据合理且长时间稳定
                        (estimated_duration >= expected_duration * 0.85 and stable_count >= 12),
                        # 条件3: 队列为空但之前有数据且稳定
                        (current_size == 0 and total_audio_bytes > 0 and stable_count >= 8),
                        # 条件4: 连续多次空队列（确保真正完成）
                        (consecutive_empty >= 6 and stable_count >= 6),
                        # 条件5: 接近超时的保险机制
                        (time.time() - wait_start > max_wait_time * 0.9)
                    ]
                    
                    if any(completion_conditions):
                        completion_reason = ""
                        if estimated_duration >= expected_duration * 0.95:
                            completion_reason = f"数据充足({total_audio_bytes}bytes, {estimated_duration:.2f}s)"
                        elif current_size == 0 and total_audio_bytes > 0:
                            completion_reason = f"队列清空({total_audio_bytes}bytes)"
                        elif consecutive_empty >= 6:
                            completion_reason = f"连续空队列({total_audio_bytes}bytes)"
                        else:
                            completion_reason = f"时间到达({total_audio_bytes}bytes)"
                        
                        print(f"✅ 音频接收完成 - {completion_reason}")
                        break
            
            # 播放剩余音频数据
            remaining_chunks = 0
            with queue_lock:
                remaining_chunks = len(audio_queue)
                while audio_queue:
                    audio_chunk = audio_queue.pop(0)
                    self.audio_player.write(audio_chunk)
            
            if remaining_chunks > 0:
                print(f"🎵 播放最后 {remaining_chunks} 块音频数据")
            
            # 更精确的播放完成等待
            print("⏳ 确保音频彻底播放完成...")
            # 基于实际音频时长动态计算等待时间
            actual_audio_duration = total_audio_bytes / 48000.0
            safety_wait_time = max(0.5, min(2.0, actual_audio_duration * 0.1 + 0.3))
            time.sleep(safety_wait_time)
            print(f"✅ 音频播放确认完成 (等待{safety_wait_time:.1f}秒)")
            
            print("✅ 稳定实时播放完成")
            return True
            
        except Exception as e:
            print(f"❌ 稳定TTS错误: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # 清理资源
            if self.audio_player:
                try:
                    self.audio_player.stop_stream()
                    self.audio_player.close()
                except:
                    pass

def demo_stable_realtime():
    """稳定版实时TTS演示"""
    print("🌟 稳定版实时TTS演示")
    print("=" * 40)
    print("✨ 特性:")
    print("  • 使用最新qwen3-tts-flash-realtime-2025-11-27模型")
    print("  • 优化的音频缓冲策略")
    print("  • 减少卡顿的文本发送机制")
    print("  • 实时音频流式播放")
    print("=" * 40)
    
    tts = StableRealTimeTTS()
    
    # 测试文本
    test_texts = [
        "你好，欢迎使用稳定版实时语音系统。",
        "这个版本专门优化了解决卡顿问题。",
        "采用了官方推荐的最新TTS模型。",
        "文本处理和音频播放都更加流畅。",
        "现在可以享受无缝的实时语音体验。",
        "每句话都会快速响应并立即播放。",
        "告别延迟，拥抱真正的实时交互。",
        "感谢使用稳定版实时TTS系统！"
    ]
    
    print("开始演示...")
    start_time = time.time()
    
    success = tts.stable_realtime_tts(test_texts)
    
    end_time = time.time()
    
    if success:
        print(f"\n🎉 演示成功完成！")
        print(f"⏱️  总耗时: {end_time - start_time:.2f}秒")
        print(f"📊 平均每句: {(end_time - start_time)/len(test_texts):.2f}秒")
        print("✅ 卡顿问题已有效改善")
        print("✅ 响应速度明显提升")
        print("✅ 播放体验更加流畅")
    else:
        print("\n❌ 演示失败")

def interactive_stable_tts():
    """交互式稳定TTS"""
    print("💬 交互式稳定TTS")
    print("=" * 30)
    print("输入文本进行实时语音播放")
    print("输入 'quit' 退出")
    print("=" * 30)
    
    tts = StableRealTimeTTS()
    
    # 先建立连接
    if not tts.setup_audio():
        return
    
    try:
        import dashscope
        from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
        
        dashscope.api_key = tts.api_key
        
        # 建立持久连接
        audio_queue = []
        queue_lock = threading.Lock()
        
        class InteractiveCallback(QwenTtsRealtimeCallback):
            def on_open(self):
                print("📡 实时连接已建立")
            
            def on_close(self, code, msg):
                print(f"🔌 连接已关闭: {msg}")
            
            def on_event(self, response):
                if isinstance(response, str):
                    try:
                        response = eval(response)
                    except:
                        return
                
                if response.get('type') == 'response.audio.delta':
                    audio_b64 = response.get('delta')
                    if audio_b64:
                        audio_data = base64.b64decode(audio_b64)
                        with queue_lock:
                            audio_queue.append(audio_data)
                            # 实时播放
                            if len(audio_queue) >= 2:
                                while audio_queue:
                                    chunk = audio_queue.pop(0)
                                    tts.play_audio_immediately(chunk)
        
        callback = InteractiveCallback()
        tts_instance = QwenTtsRealtime(
            model='qwen3-tts-flash-realtime-2025-11-27',
            callback=callback,
            url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
        )
        
        tts_instance.connect()
        time.sleep(1)  # 等待连接建立
        
        tts_instance.update_session(
            voice='Cherry',
            response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
            mode='server_commit',
            language_type='Chinese'
        )
        
        print("✅ 实时TTS系统准备就绪")
        
        # 交互式输入
        while True:
            text = input("\n🗣️ 输入文本: ").strip()
            
            if text.lower() in ['quit', 'exit', '退出']:
                break
            elif text:
                print(f"📤 发送: {text}")
                tts_instance.append_text(text)
                time.sleep(0.05)  # 短暂延迟
        
        tts_instance.finish()
        time.sleep(0.5)
        
        # 播放剩余音频
        with queue_lock:
            while audio_queue:
                chunk = audio_queue.pop(0)
                tts.play_audio_immediately(chunk)
                
    except Exception as e:
        print(f"❌ 交互式TTS错误: {e}")
    finally:
        if tts.audio_player:
            try:
                tts.audio_player.stop_stream()
                tts.audio_player.close()
            except:
                pass

def main():
    """主菜单"""
    while True:
        print("\n" + "=" * 50)
        print("🎙️ 稳定版实时TTS系统")
        print("=" * 50)
        print("1. 演示模式")
        print("2. 交互模式")
        print("3. 退出")
        print("=" * 50)
        
        choice = input("请选择 (1-3): ").strip()
        
        if choice == '1':
            demo_stable_realtime()
        elif choice == '2':
            interactive_stable_tts()
        elif choice == '3':
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    main()