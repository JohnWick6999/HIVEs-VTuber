import pyvts
import asyncio
import os
import time
from voice_api import voice_api_system

class VTSIntegration:
    """VTubeStudio集成类，用于控制口型和其他参数"""
    
    def __init__(self):
        """初始化VTubeStudio集成"""
        # 创建VTS实例，传入插件信息
        plugin_info = {
            "plugin_name": "LLM_VTB_Integration",
            "developer": "AI Assistant",
            "authentication_token_path": "./vts_token.txt"
        }
        self.vts = pyvts.vts(plugin_info=plugin_info)
        self.is_connected = False
    
    async def connect(self):
        """连接到VTubeStudio"""
        try:
            print("🔄 正在连接到VTubeStudio API (localhost:8001)...")
            await self.vts.connect()
            self.is_connected = True
            print("✅ 成功连接到VTubeStudio")
            return True
        except Exception as e:
            print(f"❌ 连接VTubeStudio失败: {e}")
            print("💡 请确保：")
            print("   1. VTubeStudio正在运行")
            print("   2. API服务器已在设置中启用")
            print("   3. 端口8001已开放")
            self.is_connected = False
            return False
    
    async def disconnect(self):
        """断开与VTubeStudio的连接"""
        try:
            if self.is_connected:
                await self.vts.disconnect()
                self.is_connected = False
                print("✅ 成功断开与VTubeStudio的连接")
        except Exception as e:
            print(f"❌ 断开VTubeStudio连接失败: {e}")
    
    async def load_model(self, model_id):
        """加载指定的Live2D模型"""
        try:
            if not self.is_connected:
                await self.connect()
            
            response = await self.vts.request("Live2DModelLoadRequest", {
                "modelID": model_id
            })
            print(f"✅ 加载模型 {model_id}: {response}")
            return response
        except Exception as e:
            print(f"❌ 加载模型失败: {e}")
            return None
    
    async def set_expressions(self, expressions):
        """设置表情参数"""
        try:
            if not self.is_connected:
                await self.connect()
            
            response = await self.vts.request("ExpressionControlRequest", {
                "expressions": expressions
            })
            return response
        except Exception as e:
            print(f"❌ 设置表情失败: {e}")
            return None
    
    async def set_articulators(self, articulators):
        """设置口型参数"""
        try:
            if not self.is_connected:
                await self.connect()
            
            response = await self.vts.request("ArtMeshControlRequest", {
                "artMeshStates": articulators
            })
            return response
        except Exception as e:
            print(f"❌ 设置口型失败: {e}")
            return None
    
    def text_to_speech_with_lip_sync(self, text, output_file="output.wav", voice_style="傲娇萝莉"):
        """文本转语音并同步口型 - 直接播放模式（支持可爱音色）"""
        try:
            print(f"🤖 虚拟主播 ({voice_style}): {text}")
            print("🔊 正在生成并播放语音...")
            
            # 使用稳定版实时TTS系统
            from stable_real_time_tts import StableRealTimeTTS
            from cute_voices import apply_cute_voice_settings
            
            tts_system = StableRealTimeTTS()
            
            # 应用可爱的音色设置
            voice_settings = apply_cute_voice_settings(tts_system, voice_style)
            
            # 直接播放单条文本
            success = tts_system.stable_realtime_tts([text])
            
            if success:
                # 更智能的等待时间计算
                import time
                # 基于文本长度和音色特点计算等待时间
                base_duration = len(text) / 2.5  # 基础估算
                # 根据音色调整（傲娇音色可能语速较慢）
                if voice_style == "傲娇萝莉":
                    adjusted_duration = base_duration * 1.2
                elif voice_style == "天然呆萌":
                    adjusted_duration = base_duration * 1.3
                else:
                    adjusted_duration = base_duration * 1.1
                
                print(f"⏳ 等待音频播放完成 ({adjusted_duration:.1f}秒)...")
                time.sleep(adjusted_duration + 0.3)  # 额外等待确保播放完成
                print("✅ 语音播放完成")
                return True
            else:
                print("❌ 语音播放失败")
                return False
                
        except Exception as e:
            print(f"❌ 语音同步失败: {e}")
            return False
    
    def _play_audio_to_virtual_cable(self, audio_file):
        """播放音频到VB-CABLE虚拟声卡（作为虚拟麦克风）"""
        try:
            import pyaudio
            import wave
            import subprocess
            import tempfile
            
            # 检查文件格式
            if audio_file.endswith('.mp3'):
                # 使用ffmpeg或系统工具转换MP3为WAV
                print("🔄 转换MP3为WAV格式...")
                wav_file = tempfile.mktemp(suffix='.wav')
                try:
                    # 尝试使用ffmpeg转换
                    subprocess.run([
                        'ffmpeg', '-i', audio_file, '-ac', '2', '-ar', '44100', '-f', 'wav', wav_file
                    ], check=True, capture_output=True)
                except Exception:
                    # 如果ffmpeg不可用，尝试使用Edge TTS直接生成WAV
                    print("⚠️ ffmpeg不可用，尝试使用Edge TTS直接生成WAV...")
                    return False
                audio_file = wav_file
            
            # 打开音频文件
            try:
                wf = wave.open(audio_file, 'rb')
            except Exception as e:
                print(f"❌ 无法打开音频文件: {e}")
                # 尝试使用系统播放器播放
                try:
                    import os
                    os.startfile(audio_file)
                    print("✅ 使用系统播放器播放音频")
                    return True
                except Exception as e2:
                    print(f"❌ 系统播放失败: {e2}")
                    return False
            
            # 初始化PyAudio
            p = pyaudio.PyAudio()
            
            # 查找VB-CABLE输出设备（作为虚拟麦克风输入）
            cable_device_index = None
            print("🔍 查找虚拟声卡设备...")
            
            # 打印所有可用设备
            print("📋 可用音频设备:")
            for i in range(p.get_device_count()):
                dev_info = p.get_device_info_by_index(i)
                print(f"  [{i}] {dev_info['name']} - {dev_info['hostApi']}")
                # 更宽松的匹配条件，查找输入设备
                if any(keyword in dev_info['name'] for keyword in ['CABLE', 'Virtual', '虚拟']):
                    # 检查是否为输入设备
                    if dev_info['maxInputChannels'] > 0:
                        cable_device_index = i
                        print(f"  ✅ 找到虚拟麦克风: {dev_info['name']}")
                        break
            
            # 如果没有找到输入设备，查找输出设备
            if cable_device_index is None:
                for i in range(p.get_device_count()):
                    dev_info = p.get_device_info_by_index(i)
                    if any(keyword in dev_info['name'] for keyword in ['CABLE', 'Virtual', '虚拟']):
                        if dev_info['maxOutputChannels'] > 0:
                            cable_device_index = i
                            print(f"  ✅ 找到虚拟声卡输出: {dev_info['name']}")
                            break
            
            if cable_device_index is None:
                print("❌ 未找到虚拟声卡")
                # 即使没有找到虚拟声卡，也尝试使用默认设备
                print("⚠️ 尝试使用默认音频设备...")
                cable_device_index = p.get_default_output_device_info()['index']
                print(f"  使用默认设备: {p.get_device_info_by_index(cable_device_index)['name']}")
            
            # 打开流（处理通道数错误）
            try:
                stream = p.open(
                    format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=cable_device_index
                )
            except Exception as e:
                print(f"⚠️ 无法使用原始通道数: {e}")
                # 尝试使用单通道
                print("🔄 尝试使用单通道...")
                stream = p.open(
                    format=p.get_format_from_width(wf.getsampwidth()),
                    channels=1,
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=cable_device_index
                )
            
            # 播放音频
            chunk = 1024
            data = wf.readframes(chunk)
            print("🔊 开始播放音频到虚拟声卡...")
            while data:
                stream.write(data)
                data = wf.readframes(chunk)
            
            # 关闭流
            stream.stop_stream()
            stream.close()
            wf.close()
            p.terminate()
            
            print("✅ 音频播放到虚拟声卡成功")
            return True
        except Exception as e:
            print(f"❌ 播放音频到虚拟声卡失败: {e}")
            # 尝试使用系统播放器播放
            try:
                import os
                os.startfile(audio_file)
                print("✅ 使用系统播放器播放音频")
                return True
            except Exception as e2:
                print(f"❌ 系统播放失败: {e2}")
                return False

# 创建全局VTS集成实例
vts_integration = VTSIntegration()

async def test_vts_integration():
    """测试VTS集成功能"""
    print("🔍 测试VTS集成功能...")
    
    # 连接到VTubeStudio
    connected = await vts_integration.connect()
    if not connected:
        print("❌ 连接VTubeStudio失败，测试结束")
        return
    
    # 测试文本转语音并同步口型
    test_text = "你好，我是一个虚拟主播，正在测试口型同步功能。"
    success = vts_integration.text_to_speech_with_lip_sync(test_text, "test_vts.wav")
    if success:
        print("✅ 语音同步测试成功")
    else:
        print("❌ 语音同步测试失败")
    
    # 断开连接
    await vts_integration.disconnect()

def test_voice_only():
    """仅测试语音生成和虚拟声卡播放功能"""
    print("🔍 测试语音生成和虚拟声卡播放功能...")
    
    # 测试文本转语音并同步口型
    test_text = "你好，我是一个虚拟主播，正在测试口型同步功能。"
    success = vts_integration.text_to_speech_with_lip_sync(test_text, "test_voice.wav")
    if success:
        print("✅ 语音生成和虚拟声卡播放测试成功")
    else:
        print("❌ 语音生成和虚拟声卡播放测试失败")

if __name__ == "__main__":
    # 先测试仅语音功能
    test_voice_only()
    # 然后测试完整的VTS集成
    asyncio.run(test_vts_integration())
