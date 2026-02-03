import requests
import os
import tempfile
import speech_recognition as sr
from typing import Optional, Any
# 使用绝对导入来避免冲突
from config import config_manager

class VoiceAPISystem:
    """语音API系统类"""
    
    def __init__(self):
        """初始化语音API系统"""
        # 重新加载配置，确保获取最新配置
        config_manager.config = config_manager._load_config()
        self.voice_config = config_manager.get_voice_api_config()
        print(f"📋 加载的语音配置: {self.voice_config}")
        self.recognizer = sr.Recognizer()
    
    def text_to_speech(self, text: str, output_file: str = "output.wav", engine: str = None) -> bool:
        """文本转语音"""
        try:
            if not text:
                print("文本不能为空")
                return False
            
            tts_config = self.voice_config.get("tts", {})
            api_key = tts_config.get("api_key")
            base_url = tts_config.get("base_url")
            voice = tts_config.get("voice", "default")
            # 使用指定的引擎或配置中的引擎，默认使用qwen（通义千问）
            tts_engine = engine or tts_config.get("engine", "qwen")
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # 根据选择的引擎使用不同的TTS服务
            print(f"[TTS] 使用{tts_engine} TTS...")
            
            if tts_engine == "qwen":
                # 优先使用通义千问TTS
                # 即使没有API密钥，也尝试使用本地TTS作为备选
                if api_key:
                    return self._qwen_text_to_speech(api_key, text, 
                                                  voice if voice != "default" else "default", 
                                                  output_file)
                else:
                    print("[TTS] 通义千问API密钥未配置，使用本地TTS...")
                    return self._local_text_to_speech(text, output_file)
            elif tts_engine == "local":
                # 使用本地TTS
                return self._local_text_to_speech(text, output_file)
            elif tts_engine == "azure" and api_key and base_url:
                # 使用Azure TTS
                return self._azure_text_to_speech(api_key, base_url, text, 
                                               voice if voice != "default" else "zh-CN-YunxiNeural", 
                                               output_file)
            elif tts_engine == "moonshot" and api_key and base_url:
                # 使用Moonshot TTS
                return self._moonshot_text_to_speech(api_key, base_url, text, 
                                                   voice if voice != "default" else "zh-CN-YunxiNeural", 
                                                   output_file)
            elif tts_engine == "edge":
                # 使用Edge TTS（暂时放在后面）
                print("[TTS] 使用Edge TTS...")
                return self._edge_text_to_speech("", "", text, 
                                             voice if voice != "default" else "zh-CN-YunxiNeural", 
                                             output_file)
            else:
                # 默认使用本地TTS（替代Edge TTS）
                print(f"[TTS] 引擎 {tts_engine} 配置不完整，使用本地TTS...")
                return self._local_text_to_speech(text, output_file)
        except Exception as e:
            print(f"文本转语音失败: {e}")
            return False
    
    def real_time_tts_and_play(self, text: str, voice: str = None) -> bool:
        """实时TTS并直接播放，不生成文件"""
        try:
            tts_config = self.voice_config.get("tts", {})
            api_key = tts_config.get("api_key")
            # 使用指定的音色或配置中的音色
            tts_voice = voice or tts_config.get("voice", "default")
            tts_engine = tts_config.get("engine", "qwen")
            
            print(f"[TTS] 实时语音生成: {text[:30]}{'...' if len(text) > 30 else ''}")
            
            if tts_engine == "qwen" and api_key:
                return self._qwen_real_time_tts_and_play(api_key, text, tts_voice)
            elif tts_engine == "edge":
                return self._edge_real_time_tts_and_play(text, tts_voice)
            else:
                print(f"[TTS] 引擎 {tts_engine} 不支持实时播放，使用传统方式...")
                # 回退到传统的文件生成方式
                temp_file = f"temp_tts_{int(time.time())}.wav"
                success = self.text_to_speech(text, temp_file)
                if success:
                    # 播放临时文件
                    try:
                        import os
                        os.startfile(temp_file)
                        # 等待播放完成后删除文件
                        import time
                        time.sleep(len(text) / 3)  # 粗略估算播放时间
                        if os.path.exists(temp_file):
                            os.remove(temp_file)
                    except Exception as e:
                        print(f"播放临时文件失败: {e}")
                return success
                
        except Exception as e:
            print(f"实时TTS播放失败: {e}")
            return False
    
    def speech_to_text(self, audio_file: str = None) -> str:
        """语音转文本"""
        try:
            asr_config = self.voice_config.get("asr", {})
            api_key = asr_config.get("api_key")
            base_url = asr_config.get("base_url")
            
            # 如果没有配置API，使用本地ASR
            if not api_key or not base_url:
                return self._local_speech_to_text(audio_file)
            
            # 根据不同的API提供商选择不同的调用方式
            if "azure" in base_url.lower():
                return self._azure_speech_to_text(api_key, base_url, audio_file)
            else:
                # 默认使用本地ASR
                return self._local_speech_to_text(audio_file)
        except Exception as e:
            print(f"语音转文本失败: {e}")
            return ""
    
    def _local_text_to_speech(self, text: str, output_file: str) -> bool:
        """本地文本转语音"""
        try:
            import pyttsx3
            
            # 初始化TTS引擎
            engine = pyttsx3.init()
            
            # 设置语速
            engine.setProperty('rate', 150)
            
            # 保存到文件
            engine.save_to_file(text, output_file)
            engine.runAndWait()
            
            return True
        except ImportError:
            print("pyttsx3库未安装")
            return False
        except Exception as e:
            print(f"本地TTS失败: {e}")
            return False
    
    async def _edge_text_to_speech_async(self, api_key: str, base_url: str, text: str, 
                                         voice: str, output_file: str) -> bool:
        """异步使用Edge TTS"""
        try:
            import edge_tts
            
            # 创建TTS实例
            tts = edge_tts.Communicate(text, voice)
            
            # 生成语音文件
            with open(output_file, "wb") as f:
                async for chunk in tts.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
            return True
        except ImportError:
            print("edge_tts库未安装")
            return False
        except Exception as e:
            print(f"Edge TTS失败: {e}")
            return False
    
    def _edge_text_to_speech(self, api_key: str, base_url: str, text: str, 
                            voice: str, output_file: str) -> bool:
        """使用Edge TTS"""
        try:
            import asyncio
            
            # 检查是否在运行的事件循环中
            try:
                loop = asyncio.get_running_loop()
                # 如果在运行的事件循环中，使用create_task并直接返回
                # 注意：这里我们使用同步方式，避免嵌套事件循环
                import edge_tts
                
                # 同步版本的Edge TTS调用
                tts = edge_tts.Communicate(text, voice)
                
                # 生成语音文件
                with open(output_file, "wb") as f:
                    # 手动迭代异步生成器
                    import asyncio
                    async def write_audio():
                        async for chunk in tts.stream():
                            if chunk["type"] == "audio":
                                f.write(chunk["data"])
                    
                    # 使用现有的事件循环
                    loop.run_until_complete(write_audio())
                return True
            except RuntimeError:
                # 如果没有运行的事件循环，使用asyncio.run
                import edge_tts
                
                async def generate_speech():
                    tts = edge_tts.Communicate(text, voice)
                    with open(output_file, "wb") as f:
                        async for chunk in tts.stream():
                            if chunk["type"] == "audio":
                                f.write(chunk["data"])
                
                asyncio.run(generate_speech())
                return True
        except ImportError:
            print("edge_tts库未安装")
            return False
        except Exception as e:
            print(f"Edge TTS失败: {e}")
            return False
    
    def test_voice_preset(self, text: str, voice_preset: str, output_file: str = "test_voice.mp3") -> bool:
        """测试特定语音预设的TTS功能"""
        print(f"[TTS] 测试语音预设: {voice_preset}")
        return self._edge_text_to_speech("", "", text, voice_preset, output_file)
    
    def _azure_text_to_speech(self, api_key: str, base_url: str, text: str, 
                             voice: str, output_file: str) -> bool:
        """使用Azure TTS"""
        try:
            headers = {
                "Ocp-Apim-Subscription-Key": api_key,
                "Content-Type": "application/ssml+xml",
                "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm"
            }
            
            # 构建SSML
            ssml = f"""
            <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'>
                <voice name='{voice}'>{text}</voice>
            </speak>
            """
            
            # 发送请求
            response = requests.post(
                f"{base_url}/cognitiveservices/v1",
                headers=headers,
                data=ssml.encode('utf-8'),
                timeout=30
            )
            
            # 保存响应
            if response.status_code == 200:
                with open(output_file, "wb") as f:
                    f.write(response.content)
                return True
            else:
                print(f"Azure TTS失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"Azure TTS失败: {e}")
            return False
    
    def _moonshot_text_to_speech(self, api_key: str, base_url: str, text: str, 
                               voice: str, output_file: str) -> bool:
        """使用Moonshot（KIMI）TTS"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": "moonshot-tts-1",
                "input": text,
                "voice": voice if voice != "default" else "zh-CN-YunxiNeural",
                "parameters": {
                    "audio_format": "mp3",
                    "speed": 1.0,
                    "pitch": 1.0,
                    "volume": 1.0
                }
            }
            
            # 发送请求
            response = requests.post(
                f"{base_url}/v1/tts",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # 保存响应
            if response.status_code == 200:
                with open(output_file, "wb") as f:
                    f.write(response.content)
                return True
            else:
                print(f"Moonshot TTS失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                # Moonshot TTS失败时，自动使用本地TTS作为备选
                print("自动切换到本地TTS...")
                return self._local_text_to_speech(text, output_file)
        except Exception as e:
            print(f"Moonshot TTS失败: {e}")
            # 异常时使用本地TTS
            print("自动切换到本地TTS...")
            return self._local_text_to_speech(text, output_file)
    
    def _qwen_voice_enrollment(self, api_key: str, audio_file: str, preferred_name: str = "my_voice") -> str:
        """使用通义千问声音复刻API创建专属音色"""
        try:
            import base64
            import pathlib
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # 读取音频文件并编码为base64
            b64 = base64.b64encode(pathlib.Path(audio_file).read_bytes()).decode()
            
            payload = {
                "model": "qwen-voice-enrollment",  # 固定值
                "input": {
                    "action": "create",
                    "target_model": "qwen3-tts-vd-realtime-2026-01-15",
                    "preferred_name": preferred_name,
                    "audio": {"data": f"data:audio/mpeg;base64,{b64}"},
                    "voice_prompt": "使用音频文件中的声音特征创建专属音色",
                    "preview_text": "你好，这是预览文本，用于测试音色效果。"
                }
            }
            
            # 正确的北京地域URL
            url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
            
            # 发送请求
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                voice_name = result["output"]["voice"]
                print(f"✅ 成功创建专属音色: {voice_name}")
                return voice_name
            else:
                print(f"❌ 声音复刻失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return None
        except Exception as e:
            print(f"❌ 声音复刻异常: {e}")
            return None
    
    def _qwen_text_to_speech(self, api_key: str, text: str, voice: str, output_file: str) -> bool:
        """使用通义千问实时流式TTS（WebSocket-based）- 修复版"""
        try:
            import os
            import base64
            import threading
            import time
            import dashscope
            from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
            
            # 初始化DashScope API Key
            dashscope.api_key = api_key
            
            # 全局变量用于存储TTS实例
            qwen_tts_realtime: QwenTtsRealtime = None
            
            # 回调类，严格按照官方文档实现
            class MyCallback(QwenTtsRealtimeCallback):
                def __init__(self, output_file):
                    super().__init__()
                    self.output_file = output_file
                    self.audio_data = b''
                    self.complete_event = threading.Event()
                    self.first_audio_received = False
                    self.session_id = None
                
                def on_open(self) -> None:
                    print('📞 WebSocket连接已打开')
                
                def on_close(self, close_status_code, close_msg) -> None:
                    print(f'📞 WebSocket连接已关闭: 代码={close_status_code}, 消息={close_msg}')
                    # 确保在连接关闭时保存音频数据
                    print(f'📊 准备保存音频数据，大小: {len(self.audio_data)} bytes')
                    if self.audio_data and len(self.audio_data) > 0:
                        try:
                            print(f'💾 正在保存到文件: {self.output_file}')
                            # 确保输出目录存在
                            output_dir = os.path.dirname(self.output_file)
                            if output_dir:
                                os.makedirs(output_dir, exist_ok=True)
                            
                            # 保存为PCM格式
                            with open(self.output_file, 'wb') as f:
                                f.write(self.audio_data)
                            print(f'✅ 音频已保存到: {self.output_file}')
                            print(f'📊 音频数据大小: {len(self.audio_data)} bytes')
                            # 检查文件是否真的创建成功
                            if os.path.exists(self.output_file):
                                actual_size = os.path.getsize(self.output_file)
                                print(f'🔍 实际文件大小: {actual_size} bytes')
                                # 转换PCM到WAV格式以便播放
                                self._convert_pcm_to_wav()
                            else:
                                print('❌ 文件未创建成功')
                        except Exception as e:
                            print(f'❌ 保存音频文件失败: {e}')
                            import traceback
                            traceback.print_exc()
                    else:
                        print('⚠️ 没有收到音频数据')
                    self.complete_event.set()
                
                def on_event(self, response) -> None:
                    try:
                        if isinstance(response, str):
                            import json
                            response = json.loads(response)
                        
                        event_type = response.get('type')
                        
                        if event_type == 'session.created':
                            self.session_id = response.get('session', {}).get('id')
                            print(f'🔄 会话已创建: {self.session_id}')
                        
                        elif event_type == 'session.updated':
                            print('🔄 会话配置已更新')
                        
                        elif event_type == 'response.audio.delta':
                            # 处理音频数据
                            audio_b64 = response.get('delta')
                            if audio_b64:
                                if not self.first_audio_received:
                                    self.first_audio_received = True
                                    print('🎧 收到首包音频数据')
                                audio_bytes = base64.b64decode(audio_b64)
                                self.audio_data += audio_bytes
                                print(f'   🔊 收到音频数据: {len(audio_bytes)} bytes (累计: {len(self.audio_data)} bytes)')
                        
                        elif event_type == 'response.done':
                            response_id = response.get('response', {}).get('id', 'unknown')
                            print(f'🔄 响应 {response_id} 已完成')
                        
                        elif event_type == 'session.finished':
                            print('🔄 会话已结束')
                            print(f'📊 最终音频数据大小: {len(self.audio_data)} bytes')
                            # 确保设置完成事件
                            self.complete_event.set()
                            
                        elif event_type == 'error':
                            error_msg = response.get('error', {}).get('message', '未知错误')
                            print(f'❌ 服务端错误: {error_msg}')
                            # 错误时也要设置完成事件
                            self.complete_event.set()
                            
                    except Exception as e:
                        print(f'❌ 处理事件失败: {e}')
                        import traceback
                        traceback.print_exc()
                        # 异常时也要设置完成事件
                        self.complete_event.set()
                
                def wait_for_finished(self):
                    self.complete_event.wait()
                
                def _convert_pcm_to_wav(self):
                    """将PCM数据转换为WAV格式"""
                    try:
                        import wave
                        pcm_file = self.output_file
                        # 正确处理文件扩展名
                        if pcm_file.endswith('.wav'):
                            wav_file = pcm_file.replace('.wav', '_converted.wav')
                        else:
                            wav_file = pcm_file + '.wav'
                        
                        # 读取PCM数据
                        with open(pcm_file, 'rb') as f:
                            pcm_data = f.read()
                        
                        # 写入WAV文件
                        with wave.open(wav_file, 'wb') as wav_f:
                            wav_f.setnchannels(1)  # 单声道
                            wav_f.setsampwidth(2)  # 16位
                            wav_f.setframerate(24000)  # 24kHz
                            wav_f.writeframes(pcm_data)
                        
                        print(f'🎵 音频格式转换完成: {wav_file}')
                    except Exception as e:
                        print(f'⚠️ 音频格式转换失败: {e}')
            
            # 创建回调实例
            callback = MyCallback(output_file)
            
            # 创建实时TTS实例 - 使用官方推荐的最新稳定版
            qwen_tts_realtime = QwenTtsRealtime(
                model='qwen3-tts-flash-realtime-2025-11-27',  # 官方推荐的最新稳定版
                callback=callback,
                # 北京地域URL
                url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
            )
            
            print('🔄 正在连接到通义千问TTS服务...')
            qwen_tts_realtime.connect()
            
            # 更新会话配置 - 严格按照官方文档参数
            tts_voice = voice if voice != "default" else "Cherry"  # Cherry是默认女声
            print(f'🔄 正在配置会话: 音色={tts_voice}')
            
            qwen_tts_realtime.update_session(
                voice=tts_voice,
                response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
                mode='server_commit',  # server_commit模式
                language_type="Chinese"  # 指定中文
            )
            
            # 流式发送文本 - 更合理的分块策略
            print('🔄 正在流式发送文本...')
            # 按句子分割文本，每个句子作为一个chunk
            sentences = self._split_text_to_sentences(text)
            
            for sentence in sentences:
                if sentence.strip():
                    print(f'📤 发送文本: {sentence}')
                    qwen_tts_realtime.append_text(sentence)
                    time.sleep(0.1)  # 给服务器处理时间
            
            # 完成发送
            print('🔄 文本发送完成，等待合成...')
            qwen_tts_realtime.finish()
            
            # 等待合成完成
            print('⏳ 等待合成完成...')
            callback.wait_for_finished()
            print('✅ 等待完成')
            
            # 检查回调中的音频数据
            print(f'📊 回调中音频数据大小: {len(callback.audio_data)} bytes')
            
            # 手动保存音频文件（如果on_close没有被调用）
            if callback.audio_data and len(callback.audio_data) > 0:
                try:
                    print(f'💾 手动保存音频文件: {output_file}')
                    # 确保输出目录存在
                    output_dir = os.path.dirname(output_file)
                    if output_dir:
                        os.makedirs(output_dir, exist_ok=True)
                    
                    # 保存为PCM格式
                    with open(output_file, 'wb') as f:
                        f.write(callback.audio_data)
                    print(f'✅ 手动保存成功: {output_file}')
                    callback._convert_pcm_to_wav()
                except Exception as e:
                    print(f'❌ 手动保存失败: {e}')
                    import traceback
                    traceback.print_exc()
            
            print('✅ 通义千问实时流式TTS合成完成')
            
            # 检查文件是否创建成功
            final_output = output_file if output_file.endswith('.wav') else output_file.replace('.pcm', '.wav')
            if os.path.exists(final_output) and os.path.getsize(final_output) > 0:
                print(f'📁 音频文件大小: {os.path.getsize(final_output)} bytes')
                # 输出性能指标
                if hasattr(qwen_tts_realtime, 'get_session_id'):
                    try:
                        session_id = qwen_tts_realtime.get_session_id()
                        first_delay = qwen_tts_realtime.get_first_audio_delay()
                        print(f'[📊 性能指标] 会话ID: {session_id}, 首包延迟: {first_delay}ms')
                    except:
                        pass
                return True
            else:
                print('❌ 音频文件创建失败')
                return False
                
        except ImportError as e:
            print(f"❌ 缺少依赖库: {e}")
            print("请安装: pip install -U dashscope")
            # 导入失败时使用本地TTS作为备选
            print("🔄 导入失败，使用本地TTS作为备选...")
            return self._local_text_to_speech(text, output_file)
        except Exception as e:
            print(f"❌ 通义千问TTS异常: {e}")
            import traceback
            traceback.print_exc()
            # 异常时使用本地TTS作为备选
            print("🔄 异常，使用本地TTS作为备选...")
            return self._local_text_to_speech(text, output_file)
    
    def _split_text_to_sentences(self, text: str) -> list:
        """将文本按句子分割"""
        import re
        # 按标点符号分割，保留标点
        sentences = re.split(r'([。！？.!?])', text)
        # 重新组合句子和标点
        result = []
        for i in range(0, len(sentences)-1, 2):
            if i+1 < len(sentences):
                sentence = sentences[i] + sentences[i+1]
                if sentence.strip():
                    result.append(sentence.strip())
        # 处理最后一个可能的句子
        if len(sentences) % 2 == 1 and sentences[-1].strip():
            result.append(sentences[-1].strip())
        return result if result else [text]
    
    def _qwen_realtime_tts(self, api_key: str, text: str, voice: str) -> bool:
        """使用通义千问实时流式TTS - 修复版"""
        try:
            import os
            import base64
            import threading
            import time
            import dashscope
            from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
            
            # 初始化DashScope API Key
            dashscope.api_key = api_key
            
            # 回调类 - 修复版
            class MyCallback(QwenTtsRealtimeCallback):
                def __init__(self):
                    super().__init__()
                    self.audio_player = None
                    self.done = threading.Event()
                    self.audio_queue = []
                    self.playing = False
                
                def on_open(self) -> None:
                    print('📞 实时TTS WebSocket连接已打开')
                    # 初始化音频播放器
                    try:
                        import pyaudio
                        self.audio_player = pyaudio.PyAudio().open(
                            format=pyaudio.paInt16,
                            channels=1,
                            rate=24000,
                            output=True,
                            frames_per_buffer=1024
                        )
                        print('🔊 音频播放器初始化成功')
                    except Exception as e:
                        print(f'⚠️ 音频播放器初始化失败: {e}')
                
                def on_close(self, close_status_code, close_msg) -> None:
                    print(f'📞 实时TTS WebSocket连接已关闭: {close_msg}')
                    self.playing = False
                    if self.audio_player:
                        try:
                            self.audio_player.stop_stream()
                            self.audio_player.close()
                        except:
                            pass
                    self.done.set()
                
                def on_event(self, response) -> None:
                    try:
                        if isinstance(response, str):
                            import json
                            response = json.loads(response)
                        
                        event_type = response.get('type')
                        
                        if event_type == 'response.audio.delta':
                            # 处理音频数据并实时播放
                            audio_b64 = response.get('delta')
                            if audio_b64 and self.audio_player:
                                try:
                                    audio_data = base64.b64decode(audio_b64)
                                    self.audio_player.write(audio_data)
                                    if not self.playing:
                                        self.playing = True
                                        print('🔊 开始实时播放音频...')
                                except Exception as e:
                                    print(f'⚠️ 音频播放失败: {e}')
                        
                        elif event_type == 'session.finished':
                            print('🔄 实时TTS会话已结束')
                            self.done.set()
                        
                        elif event_type == 'error':
                            error_msg = response.get('error', {}).get('message', '未知错误')
                            print(f'❌ 实时TTS错误: {error_msg}')
                            self.done.set()
                            
                    except Exception as e:
                        print(f'❌ 处理实时TTS事件失败: {e}')
                
                def wait(self):
                    self.done.wait()
            
            # 创建回调实例
            callback = MyCallback()
            
            # 创建实时TTS实例
            tts = QwenTtsRealtime(
                model='qwen3-tts-flash-realtime-2025-11-27',  # 官方推荐的最新稳定版
                callback=callback,
                url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
            )
            
            print('🔄 连接到实时TTS服务...')
            tts.connect()
            
            # 更新会话配置
            tts.update_session(
                voice=voice if voice != "default" else "Cherry",
                response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
                mode='server_commit',
                language_type="Chinese"
            )
            
            print('🔄 开始流式发送文本...')
            # 按句子分割发送
            sentences = self._split_text_to_sentences(text)
            for sentence in sentences:
                if sentence.strip():
                    print(f'📤 发送: {sentence}')
                    tts.append_text(sentence)
                    time.sleep(0.1)
            
            print('🔄 文本发送完成，等待合成...')
            tts.finish()
            
            # 等待合成和播放完成
            callback.wait()
            
            print("✅ 实时流式TTS合成播放完成")
            return True
            
        except ImportError as e:
            print(f"❌ 缺少依赖库: {e}")
            print("请安装: pip install -U dashscope pyaudio")
            return False
        except Exception as e:
            print(f"❌ 实时流式TTS异常: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _local_speech_to_text(self, audio_file: str = None) -> str:
        """本地语音转文本"""
        try:
            if audio_file:
                # 检查文件是否存在
                if not os.path.exists(audio_file):
                    print(f"音频文件不存在: {audio_file}")
                    return ""
                
                # 从文件识别
                with sr.AudioFile(audio_file) as source:
                    audio = self.recognizer.record(source)
            else:
                # 从麦克风识别
                with sr.Microphone() as source:
                    print("请说话...")
                    audio = self.recognizer.listen(source)
            
            # 使用Google Web Speech API
            text = self.recognizer.recognize_google(audio, language="zh-CN")
            return text
        except sr.UnknownValueError:
            print("无法识别语音")
            return ""
        except sr.RequestError as e:
            print(f"语音识别服务请求失败: {e}")
            return ""
        except Exception as e:
            print(f"本地ASR失败: {e}")
            return ""
    
    def _azure_speech_to_text(self, api_key: str, base_url: str, audio_file: str) -> str:
        """使用Azure ASR"""
        try:
            # 检查文件是否存在
            if not os.path.exists(audio_file):
                print(f"音频文件不存在: {audio_file}")
                return ""
            
            headers = {
                "Ocp-Apim-Subscription-Key": api_key,
                "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000"
            }
            
            # 读取音频文件
            with open(audio_file, "rb") as f:
                audio_data = f.read()
            
            # 发送请求
            response = requests.post(
                f"{base_url}/speech/recognition/conversation/cognitiveservices/v1",
                headers=headers,
                data=audio_data,
                params={"language": "zh-CN"},
                timeout=30
            )
            
            # 解析响应
            if response.status_code == 200:
                result = response.json()
                return result.get("DisplayText", "")
            else:
                print(f"Azure ASR失败: {response.status_code}")
                return ""
        except Exception as e:
            print(f"Azure ASR失败: {e}")
            return ""

    def _qwen_real_time_tts_and_play(self, api_key: str, text: str, voice: str) -> bool:
        """通义千问实时TTS并直接播放"""
        try:
            import dashscope
            from dashscope.audio.tts_v2 import SpeechSynthesizer
            import pyaudio
            import queue
            import threading
            
            # 配置API密钥
            dashscope.api_key = api_key
            
            # 音频播放队列
            audio_queue = queue.Queue()
            playback_finished = threading.Event()
            
            def audio_callback(frame):
                """音频数据回调"""
                try:
                    if frame is not None:
                        # 检查frame是否有data属性
                        if hasattr(frame, 'data'):
                            audio_queue.put(frame.data)
                        else:
                            # 如果没有data属性，直接放入队列
                            audio_queue.put(frame)
                except Exception as e:
                    print(f"音频回调处理错误: {e}")
            
            def playback_worker():
                """音频播放工作线程"""
                try:
                    p = pyaudio.PyAudio()
                    stream = p.open(
                        format=pyaudio.paInt16,
                        channels=1,
                        rate=22050,
                        output=True,
                        frames_per_buffer=1024
                    )
                    
                    while not playback_finished.is_set() or not audio_queue.empty():
                        try:
                            frame = audio_queue.get(timeout=0.1)
                            if frame:
                                stream.write(frame)
                        except queue.Empty:
                            continue
                    
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                except Exception as e:
                    print(f"音频播放错误: {e}")
            
            # 启动播放线程
            playback_thread = threading.Thread(target=playback_worker, daemon=True)
            playback_thread.start()
            
            # 创建语音合成器
            synthesizer = SpeechSynthesizer(
                model='qwen3-tts-flash-realtime-2025-11-27',
                voice=voice,
                format='pcm_22050',
                callback=audio_callback
            )
            
            # 发送文本
            synthesizer.streaming_call(text)
            synthesizer.streaming_complete()
            
            # 等待播放完成
            playback_finished.set()
            playback_thread.join(timeout=5)
            
            print("✅ 实时TTS播放完成")
            return True
            
        except ImportError:
            print("缺少必要的库，请安装: pip install dashscope pyaudio")
            return False
        except Exception as e:
            print(f"实时TTS播放失败: {e}")
            return False
    
    def get_qwen_voices(self):
        """获取通义千问支持的音色列表"""
        try:
            import dashscope
            from dashscope.audio.tts_v2 import SpeechSynthesizer
            
            # 使用配置中的API密钥
            tts_config = self.voice_config.get("tts", {})
            api_key = tts_config.get("api_key")
            
            if not api_key:
                print("通义千问API密钥未配置")
                return []
            
            dashscope.api_key = api_key
            
            # 获取音色列表
            synthesizer = SpeechSynthesizer()
            voices = synthesizer.list_voices()
            
            print("✅ 获取到通义千问音色列表:")
            for voice in voices:
                print(f"- {voice.name}: {voice.description}")
            
            return voices
        except Exception as e:
            print(f"获取音色列表失败: {e}")
            return []
    
    def create_cute_loli_voice(self, preferred_name: str = "cute_loli") -> str:
        """创建可爱傲娇萝莉音音色"""
        try:
            # 注意：由于需要音频样本，这里我们使用通义千问的预设音色
            # 实际上，通义千问提供了多个适合的女声音色
            # 我们选择一个最适合可爱傲娇萝莉音的预设音色
            
            print("🎀 创建可爱傲娇萝莉音...")
            print("💡 注意：使用通义千问预设音色，无需上传音频样本")
            
            # 推荐的可爱萝莉音色
            cute_loli_voice = "Cherry"
            
            print(f"✅ 可爱傲娇萝莉音创建成功！")
            print(f"🎵 使用的音色: {cute_loli_voice}")
            print(f"💖 音色特点: 甜美、可爱、带有一点傲娇感的萝莉音")
            
            # 更新配置文件中的音色设置
            config_manager.config["voice_api"]["tts"]["voice"] = cute_loli_voice
            config_manager._save_config()
            print("🔄 配置文件已更新")
            
            return cute_loli_voice
        except Exception as e:
            print(f"创建可爱傲娇萝莉音失败: {e}")
            return None
    
    def _edge_real_time_tts_and_play(self, text: str, voice: str) -> bool:
        """Edge TTS实时播放"""
        try:
            import edge_tts
            import asyncio
            import pyaudio
            import queue
            import threading
            
            # 音频播放队列
            audio_queue = queue.Queue()
            playback_finished = threading.Event()
            
            def playback_worker():
                """音频播放工作线程"""
                try:
                    p = pyaudio.PyAudio()
                    stream = p.open(
                        format=pyaudio.paInt16,
                        channels=1,
                        rate=24000,
                        output=True,
                        frames_per_buffer=1024
                    )
                    
                    while not playback_finished.is_set() or not audio_queue.empty():
                        try:
                            audio_data = audio_queue.get(timeout=0.1)
                            if audio_data:
                                stream.write(audio_data)
                        except queue.Empty:
                            continue
                    
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                except Exception as e:
                    print(f"音频播放错误: {e}")
            
            # 启动播放线程
            playback_thread = threading.Thread(target=playback_worker, daemon=True)
            playback_thread.start()
            
            async def generate_and_play():
                """生成并播放音频"""
                try:
                    communicate = edge_tts.Communicate(text, voice)
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            audio_queue.put(chunk["data"])
                except Exception as e:
                    print(f"Edge TTS生成失败: {e}")
            
            # 运行异步任务
            asyncio.run(generate_and_play())
            
            # 等待播放完成
            playback_finished.set()
            playback_thread.join(timeout=5)
            
            print("✅ Edge TTS播放完成")
            return True
            
        except ImportError:
            print("缺少必要的库，请安装: pip install edge-tts pyaudio")
            return False
        except Exception as e:
            print(f"Edge TTS播放失败: {e}")
            return False

# 创建全局语音API系统实例
voice_api_system = VoiceAPISystem()
