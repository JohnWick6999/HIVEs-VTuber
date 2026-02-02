import requests
import os
import tempfile
import speech_recognition as sr
from typing import Optional, Any
from config import config_manager

class VoiceAPISystem:
    """语音API系统类"""
    
    def __init__(self):
        """初始化语音API系统"""
        self.voice_config = config_manager.get_voice_api_config()
        self.recognizer = sr.Recognizer()
    
    def text_to_speech(self, text: str, output_file: str = "output.wav") -> bool:
        """文本转语音"""
        try:
            if not text:
                print("文本不能为空")
                return False
            
            tts_config = self.voice_config.get("tts", {})
            api_key = tts_config.get("api_key")
            base_url = tts_config.get("base_url")
            voice = tts_config.get("voice", "default")
            tts_engine = tts_config.get("engine", "edge")  # 默认使用Edge TTS
            
            # 确保输出目录存在
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # 优先使用Edge TTS（无需API密钥，稳定可靠）
            print("[TTS] 使用Edge TTS...")
            edge_result = self._edge_text_to_speech("", "", text, 
                                                 voice if voice != "default" else "zh-CN-YunxiNeural", 
                                                 output_file)
            if edge_result:
                return True
            print("[TTS] Edge TTS失败，尝试本地TTS...")
            
            # 最后使用本地TTS作为备选
            print("[TTS] 使用本地TTS...")
            return self._local_text_to_speech(text, output_file)
        except Exception as e:
            print(f"文本转语音失败: {e}")
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
    
    def _edge_text_to_speech(self, api_key: str, base_url: str, text: str, 
                            voice: str, output_file: str) -> bool:
        """使用Edge TTS"""
        try:
            import edge_tts
            import asyncio
            
            async def generate_speech():
                # 创建TTS实例
                tts = edge_tts.Communicate(text, voice)
                
                # 生成语音文件
                with open(output_file, "wb") as f:
                    async for chunk in tts.stream():
                        if chunk["type"] == "audio":
                            f.write(chunk["data"])
            
            # 运行异步函数
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
    
    def _qwen_realtime_tts(self, api_key: str, text: str, voice: str) -> bool:
        """使用通义千问实时流式TTS"""
        try:
            import os
            import dashscope
            from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat
            import base64
            import pyaudio
            import threading
            import time
            
            # 初始化DashScope API Key
            dashscope.api_key = api_key
            
            # 回调类
            class MyCallback(QwenTtsRealtimeCallback):
                def __init__(self):
                    super().__init__()
                    self.player = pyaudio.PyAudio().open(
                        format=pyaudio.paInt16,
                        channels=1,
                        rate=24000,
                        output=True
                    )
                    self.done = threading.Event()
                
                def on_event(self, msg):
                    if msg['type'] == 'response.audio.delta':
                        try:
                            audio_data = base64.b64decode(msg['delta'])
                            self.player.write(audio_data)
                        except Exception as e:
                            print(f"播放音频失败: {e}")
                    elif msg['type'] == 'session.finished':
                        self.done.set()
                
                def wait(self):
                    self.done.wait()
            
            # 创建回调实例
            callback = MyCallback()
            
            # 创建实时TTS实例
            tts = QwenTtsRealtime(
                model="qwen3-tts-vd-realtime-2026-01-15",
                callback=callback,
                url="wss://dashscope.aliyuncs.com/api-ws/v1/realtime"
            )
            
            # 连接WebSocket
            tts.connect()
            
            # 更新会话配置
            tts.update_session(
                voice=voice,
                response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
                mode='server_commit'
            )
            
            # 流式发送文本
            text_segments = [text[i:i+10] for i in range(0, len(text), 10)]
            for seg in text_segments:
                tts.append_text(seg)
                time.sleep(0.1)  # 模拟人打字节奏
            
            # 完成发送
            tts.finish()
            
            # 等待合成完成
            callback.wait()
            
            print("✅ 实时流式TTS合成完成")
            return True
        except ImportError as e:
            print(f"❌ 缺少依赖库: {e}")
            print("请安装: pip install -U dashscope pyaudio")
            return False
        except Exception as e:
            print(f"❌ 实时流式TTS异常: {e}")
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

# 创建全局语音API系统实例
voice_api_system = VoiceAPISystem()
