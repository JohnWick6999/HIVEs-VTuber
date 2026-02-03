#!/usr/bin/env python3
# 虚拟麦克风管理系统 - 自动安装和配置VB-CABLE

import os
import sys
import subprocess
import time
import requests
import zipfile
import shutil
from pathlib import Path

class VirtualMicrophoneManager:
    """虚拟麦克风管理器"""
    
    def __init__(self):
        self.download_dir = Path("virtual_mic_drivers")
        self.vbcable_installed = False
        self.vtubestudio_configured = False
        
    def check_admin_privileges(self):
        """检查管理员权限"""
        try:
            # Windows检查
            if os.name == 'nt':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                # Unix/Linux检查
                return os.geteuid() == 0
        except:
            return False
    
    def download_vbcable_driver(self):
        """下载VB-CABLE驱动"""
        print("📥 开始下载VB-CABLE虚拟声卡驱动...")
        
        # 创建下载目录
        self.download_dir.mkdir(exist_ok=True)
        
        # VB-CABLE下载链接
        download_url = "https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack45.zip"
        zip_path = self.download_dir / "VBCABLE_Driver_Pack45.zip"
        
        try:
            print(f"正在下载: {download_url}")
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 保存文件
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ 下载完成: {zip_path}")
            return zip_path
            
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            return None
    
    def extract_driver(self, zip_path):
        """解压驱动文件"""
        print("📦 解压驱动文件...")
        
        try:
            extract_dir = self.download_dir / "vbcable_extracted"
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            print(f"✅ 解压完成: {extract_dir}")
            return extract_dir
            
        except Exception as e:
            print(f"❌ 解压失败: {e}")
            return None
    
    def install_vbcable_windows(self, driver_path):
        """在Windows上安装VB-CABLE"""
        print("🔧 开始安装VB-CABLE驱动...")
        
        if not self.check_admin_privileges():
            print("⚠️  需要管理员权限来安装驱动")
            print("请以管理员身份运行此脚本")
            return False
        
        try:
            # 查找安装程序
            setup_exe = None
            for file in driver_path.iterdir():
                if file.name.startswith("VBCABLE_Setup") and file.suffix == ".exe":
                    setup_exe = file
                    break
            
            if not setup_exe:
                print("❌ 未找到安装程序")
                return False
            
            print(f"找到安装程序: {setup_exe}")
            
            # 执行安装
            print("正在运行安装程序...")
            result = subprocess.run(
                [str(setup_exe), "/S"],  # 静默安装
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print("✅ VB-CABLE安装成功")
                print("⚠️  请重启计算机以使驱动生效")
                self.vbcable_installed = True
                return True
            else:
                print(f"❌ 安装失败: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 安装过程出错: {e}")
            return False
    
    def configure_audio_devices(self):
        """配置音频设备"""
        print("⚙️  配置虚拟音频设备...")
        
        try:
            import pyaudio
            
            # 列出所有音频设备
            p = pyaudio.PyAudio()
            print("\n可用的音频设备:")
            
            input_devices = []
            output_devices = []
            
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                device_name = device_info['name']
                
                # 输入设备
                if device_info["maxInputChannels"] > 0:
                    input_devices.append((i, device_name))
                    print(f"🎤 输入设备 {i}: {device_name}")
                
                # 输出设备
                if device_info["maxOutputChannels"] > 0:
                    output_devices.append((i, device_name))
                    print(f"🔊 输出设备 {i}: {device_name}")
            
            p.terminate()
            
            # 查找VB-CABLE设备
            vbcable_input = None
            vbcable_output = None
            
            for idx, name in input_devices:
                if "cable" in name.lower() or "vb" in name.lower():
                    vbcable_input = (idx, name)
                    break
            
            for idx, name in output_devices:
                if "cable" in name.lower() or "vb" in name.lower():
                    vbcable_output = (idx, name)
                    break
            
            if vbcable_input and vbcable_output:
                print(f"\n✅ 找到VB-CABLE设备:")
                print(f"   输入: {vbcable_input[1]} (索引: {vbcable_input[0]})")
                print(f"   输出: {vbcable_output[1]} (索引: {vbcable_output[0]})")
                return vbcable_input, vbcable_output
            else:
                print("❌ 未找到VB-CABLE虚拟设备")
                return None, None
                
        except Exception as e:
            print(f"❌ 音频设备检测失败: {e}")
            return None, None
    
    def test_virtual_microphone(self, input_device_idx):
        """测试虚拟麦克风"""
        print("🧪 测试虚拟麦克风功能...")
        
        try:
            import pyaudio
            import wave
            
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            RECORD_SECONDS = 3
            
            p = pyaudio.PyAudio()
            
            # 打开输入流
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=input_device_idx,
                frames_per_buffer=CHUNK
            )
            
            print(f"开始录制 {RECORD_SECONDS} 秒测试音频...")
            frames = []
            
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            
            print("录制完成")
            
            # 保存测试文件
            test_file = "virtual_mic_test.wav"
            wf = wave.open(test_file, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            file_size = os.path.getsize(test_file)
            print(f"✅ 测试文件已保存: {test_file} ({file_size} bytes)")
            
            return True
            
        except Exception as e:
            print(f"❌ 虚拟麦克风测试失败: {e}")
            return False
    
    def integrate_with_vtubestudio(self, input_device_idx):
        """与VTubeStudio集成"""
        print("🎮 配置VTubeStudio集成...")
        
        try:
            # 创建VTubeStudio配置文件
            config = {
                "virtual_mic": {
                    "device_index": input_device_idx,
                    "device_name": "VB-CABLE Input",
                    "sample_rate": 44100,
                    "channels": 1
                },
                "tts_settings": {
                    "auto_route": True,
                    "buffer_size": 1024,
                    "latency": "low"
                }
            }
            
            # 保存配置
            import json
            config_file = "vtubestudio_virtual_mic_config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ VTubeStudio配置已保存: {config_file}")
            self.vtubestudio_configured = True
            return True
            
        except Exception as e:
            print(f"❌ VTubeStudio集成配置失败: {e}")
            return False
    
    def create_audio_router(self):
        """创建音频路由工具"""
        print("🔗 创建音频路由工具...")
        
        router_code = '''
#!/usr/bin/env python3
# 音频路由工具 - 将TTS音频路由到虚拟麦克风

import pyaudio
import threading
import queue
import time

class AudioRouter:
    def __init__(self, input_device_idx, output_device_idx):
        self.input_idx = input_device_idx
        self.output_idx = output_device_idx
        self.audio = pyaudio.PyAudio()
        self.running = False
        
    def route_audio(self):
        """路由音频从输出到输入"""
        try:
            # 输入流（虚拟麦克风）
            input_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                input_device_index=self.input_idx,
                frames_per_buffer=1024
            )
            
            # 输出流（系统音频）
            output_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                output=True,
                output_device_index=self.output_idx,
                frames_per_buffer=1024
            )
            
            print("🔄 音频路由已启动")
            self.running = True
            
            while self.running:
                try:
                    # 读取输入音频并转发到输出
                    data = input_stream.read(1024, exception_on_overflow=False)
                    output_stream.write(data)
                except Exception as e:
                    print(f"音频路由错误: {e}")
                    time.sleep(0.01)
            
            input_stream.stop_stream()
            input_stream.close()
            output_stream.stop_stream()
            output_stream.close()
            
        except Exception as e:
            print(f"音频路由启动失败: {e}")
    
    def start_routing(self):
        """启动音频路由"""
        router_thread = threading.Thread(target=self.route_audio)
        router_thread.daemon = True
        router_thread.start()
        return router_thread
    
    def stop_routing(self):
        """停止音频路由"""
        self.running = False

# 使用示例
if __name__ == "__main__":
    # 这里需要填入实际的设备索引
    router = AudioRouter(input_device_idx=1, output_device_idx=0)
    router.start_routing()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        router.stop_routing()
        print("音频路由已停止")
'''
        
        with open("audio_router.py", "w", encoding="utf-8") as f:
            f.write(router_code)
        
        print("✅ 音频路由工具已创建: audio_router.py")
    
    def setup_complete_system(self):
        """设置完整系统"""
        print("🚀 开始设置虚拟麦克风完整系统...")
        print("=" * 50)
        
        # 1. 下载驱动
        zip_path = self.download_vbcable_driver()
        if not zip_path:
            return False
        
        # 2. 解压驱动
        driver_path = self.extract_driver(zip_path)
        if not driver_path:
            return False
        
        # 3. 安装驱动
        if os.name == 'nt':
            success = self.install_vbcable_windows(driver_path)
        else:
            print("⚠️  当前仅支持Windows系统")
            return False
        
        if not success:
            return False
        
        print("\n" + "=" * 50)
        print("✅ 虚拟麦克风系统安装完成！")
        print("请按以下步骤完成配置：")
        print("1. 重启计算机")
        print("2. 运行 configure_virtual_mic.py 进行设备配置")
        print("3. 在VTubeStudio中选择VB-CABLE作为麦克风输入")
        print("=" * 50)
        
        return True

def main():
    """主函数"""
    print("🎙️ 虚拟麦克风自动安装系统")
    print("=" * 40)
    
    manager = VirtualMicrophoneManager()
    
    print("选择操作:")
    print("1. 安装VB-CABLE虚拟声卡")
    print("2. 配置现有音频设备")
    print("3. 测试虚拟麦克风")
    print("4. 与VTubeStudio集成")
    print("5. 退出")
    
    choice = input("\n请选择 (1-5): ").strip()
    
    if choice == '1':
        manager.setup_complete_system()
    elif choice == '2':
        input_dev, output_dev = manager.configure_audio_devices()
        if input_dev and output_dev:
            print("设备配置完成")
    elif choice == '3':
        input_dev, _ = manager.configure_audio_devices()
        if input_dev:
            manager.test_virtual_microphone(input_dev[0])
    elif choice == '4':
        input_dev, _ = manager.configure_audio_devices()
        if input_dev:
            manager.integrate_with_vtubestudio(input_dev[0])
    elif choice == '5':
        print("再见！")
    else:
        print("无效选择")

if __name__ == "__main__":
    main()