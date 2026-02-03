#!/usr/bin/env python3
# 简化版虚拟麦克风配置器

import os
import pyaudio
import threading
import time
import numpy as np

class SimpleVirtualMic:
    """简化版虚拟麦克风"""
    
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.virtual_input_idx = None
        self.virtual_output_idx = None
        self.is_active = False
        
    def find_virtual_devices(self):
        """查找虚拟音频设备"""
        print("🔍 搜索虚拟音频设备...")
        
        devices = []
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            device_name = device_info['name'].lower()
            
            # 查找包含"cable"或"vb"的设备
            if 'cable' in device_name or 'vb' in device_name:
                devices.append({
                    'index': i,
                    'name': device_info['name'],
                    'channels_in': device_info['maxInputChannels'],
                    'channels_out': device_info['maxOutputChannels']
                })
                print(f"发现设备: {device_info['name']} (索引: {i})")
        
        # 分离输入和输出设备
        input_devices = [d for d in devices if d['channels_in'] > 0]
        output_devices = [d for d in devices if d['channels_out'] > 0]
        
        if input_devices:
            self.virtual_input_idx = input_devices[0]['index']
            print(f"✅ 虚拟输入设备: {input_devices[0]['name']}")
        
        if output_devices:
            self.virtual_output_idx = output_devices[0]['index']
            print(f"✅ 虚拟输出设备: {output_devices[0]['name']}")
        
        return len(devices) > 0
    
    def create_virtual_audio_stream(self):
        """创建虚拟音频流"""
        if not self.virtual_input_idx or not self.virtual_output_idx:
            print("❌ 未找到虚拟音频设备")
            return False
        
        try:
            # 创建双向音频流
            self.input_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                input_device_index=self.virtual_input_idx,
                frames_per_buffer=1024
            )
            
            self.output_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                output=True,
                output_device_index=self.virtual_output_idx,
                frames_per_buffer=1024
            )
            
            print("✅ 虚拟音频流创建成功")
            return True
            
        except Exception as e:
            print(f"❌ 音频流创建失败: {e}")
            return False
    
    def route_audio(self):
        """路由音频数据"""
        print("🔄 开始音频路由...")
        self.is_active = True
        
        while self.is_active:
            try:
                # 从虚拟输入读取数据
                data = self.input_stream.read(1024, exception_on_overflow=False)
                
                # 写入到虚拟输出
                self.output_stream.write(data)
                
            except Exception as e:
                print(f"⚠️ 音频路由错误: {e}")
                time.sleep(0.01)
    
    def start_virtual_mic(self):
        """启动虚拟麦克风"""
        if not self.find_virtual_devices():
            print("❌ 请先安装VB-CABLE虚拟声卡")
            return False
        
        if not self.create_virtual_audio_stream():
            return False
        
        # 启动路由线程
        self.routing_thread = threading.Thread(target=self.route_audio)
        self.routing_thread.daemon = True
        self.routing_thread.start()
        
        print("✅ 虚拟麦克风已启动")
        print("在VTubeStudio中请选择VB-CABLE作为麦克风输入")
        return True
    
    def stop_virtual_mic(self):
        """停止虚拟麦克风"""
        print("🛑 停止虚拟麦克风...")
        self.is_active = False
        
        if hasattr(self, 'input_stream'):
            self.input_stream.stop_stream()
            self.input_stream.close()
        
        if hasattr(self, 'output_stream'):
            self.output_stream.stop_stream()
            self.output_stream.close()
        
        self.audio.terminate()
        print("✅ 虚拟麦克风已停止")
    
    def test_audio_loopback(self):
        """测试音频回环"""
        print("🧪 测试音频回环...")
        
        if not self.virtual_input_idx:
            print("❌ 未找到虚拟输入设备")
            return False
        
        try:
            # 创建测试流
            test_stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                input_device_index=self.virtual_input_idx,
                frames_per_buffer=1024
            )
            
            print("开始录制测试音频...")
            frames = []
            
            # 录制3秒
            for i in range(0, int(44100 / 1024 * 3)):
                data = test_stream.read(1024)
                frames.append(data)
            
            # 保存测试文件
            import wave
            wf = wave.open('virtual_mic_test.wav', 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            test_stream.close()
            
            file_size = os.path.getsize('virtual_mic_test.wav')
            print(f"✅ 测试完成，文件大小: {file_size} bytes")
            return True
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False

class VTSTIntegration:
    """与VTubeStudio集成"""
    
    def __init__(self, virtual_mic):
        self.virtual_mic = virtual_mic
        self.vts_connected = False
    
    def connect_to_vts(self):
        """连接到VTubeStudio"""
        try:
            # 检查VTubeStudio是否运行
            import psutil
            vts_running = False
            
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and 'vtuber' in proc.info['name'].lower():
                    vts_running = True
                    break
            
            if not vts_running:
                print("⚠️  VTubeStudio未运行，请先启动VTubeStudio")
                return False
            
            print("✅ 检测到VTubeStudio正在运行")
            print("📢 请在VTubeStudio中手动设置:")
            print("   1. 打开VTubeStudio设置")
            print("   2. 进入音频设置")
            print("   3. 将麦克风输入设置为: VB-CABLE Input")
            print("   4. 调整音频增益和降噪设置")
            
            self.vts_connected = True
            return True
            
        except ImportError:
            print("⚠️  未安装psutil库，跳过VTubeStudio检测")
            print("📢 请手动在VTubeStudio中设置音频输入为VB-CABLE Input")
            self.vts_connected = True
            return True
        except Exception as e:
            print(f"❌ VTubeStudio连接检查失败: {e}")
            return False
    
    def set_vts_audio_input(self):
        """设置VTS音频输入"""
        if not self.vts_connected:
            print("❌ 请先连接VTubeStudio")
            return False
        
        try:
            # 这里需要根据VTS API设置音频输入设备
            # 暂时只打印提示信息
            print("📢 请在VTubeStudio中手动设置:")
            print("   1. 打开VTubeStudio设置")
            print("   2. 进入音频设置")
            print("   3. 将麦克风输入设置为: VB-CABLE Input")
            print("   4. 调整音频增益和降噪设置")
            
            return True
            
        except Exception as e:
            print(f"❌ 设置VTS音频输入失败: {e}")
            return False
    
    def monitor_audio_levels(self):
        """监控音频电平"""
        print("📊 开始监控音频电平...")
        
        if not self.virtual_mic.virtual_input_idx:
            print("❌ 未找到虚拟输入设备")
            return
        
        try:
            stream = self.virtual_mic.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                input_device_index=self.virtual_mic.virtual_input_idx,
                frames_per_buffer=1024
            )
            
            while True:
                try:
                    data = stream.read(1024, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.int16)
                    volume = np.abs(audio_data).mean()
                    
                    # 简单的音量指示器
                    bar_length = int(volume / 100)
                    bar = "█" * min(bar_length, 20) + "░" * (20 - min(bar_length, 20))
                    print(f"\r音量: [{bar}] {volume:.0f}", end="", flush=True)
                    
                    time.sleep(0.1)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"\n监控错误: {e}")
                    break
            
            stream.close()
            print("\n监控已停止")
            
        except Exception as e:
            print(f"❌ 音频监控启动失败: {e}")

def main():
    """主程序"""
    print("🎙️ 简化版虚拟麦克风配置器")
    print("=" * 40)
    
    # 创建虚拟麦克风实例
    virtual_mic = SimpleVirtualMic()
    vts_integration = VTSTIntegration(virtual_mic)
    
    while True:
        print("\n请选择功能:")
        print("1. 启动虚拟麦克风")
        print("2. 测试音频回环")
        print("3. 连接VTubeStudio")
        print("4. 监控音频电平")
        print("5. 停止虚拟麦克风")
        print("6. 退出")
        
        choice = input("\n请输入选择 (1-6): ").strip()
        
        if choice == '1':
            virtual_mic.start_virtual_mic()
        elif choice == '2':
            virtual_mic.test_audio_loopback()
        elif choice == '3':
            vts_integration.connect_to_vts()
            vts_integration.set_vts_audio_input()
        elif choice == '4':
            vts_integration.monitor_audio_levels()
        elif choice == '5':
            virtual_mic.stop_virtual_mic()
        elif choice == '6':
            if virtual_mic.is_active:
                virtual_mic.stop_virtual_mic()
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    main()