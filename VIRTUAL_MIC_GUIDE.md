# 虚拟麦克风集成使用指南

## 🎯 系统概述

本系统集成了VB-CABLE虚拟声卡，可以将TTS生成的音频实时路由到虚拟麦克风，供VTubeStudio使用。

## 📦 安装步骤

### 1. 自动安装VB-CABLE（推荐）

```bash
# 以管理员身份运行
install_vbcable.bat
```

### 2. 手动安装VB-CABLE

1. 访问官网下载: https://vb-audio.com/Cable/
2. 下载 `VBCABLE_Driver_Pack45.zip`
3. 以管理员身份运行安装程序
4. 重启计算机

### 3. 验证安装

运行配置脚本检查设备：
```bash
python simple_virtual_mic.py
```

选择选项2进行测试。

## ⚙️ 系统配置

### 音频设备设置

**Windows音频设置:**
1. 打开"控制面板" → "声音"
2. **播放**标签页: 设置"CABLE Input"为默认设备
3. **录制**标签页: 设置"CABLE Output"为默认设备

**VTubeStudio设置:**
1. 打开VTubeStudio
2. 进入"设置" → "音频设置"
3. 将麦克风输入设置为"VB-CABLE Input"
4. 调整音频增益和降噪参数

## 🚀 使用方法

### 1. 启动虚拟麦克风系统

```bash
python simple_virtual_mic.py
```

选择选项1启动虚拟麦克风。

### 2. 与TTS系统集成

```python
from simple_virtual_mic import SimpleVirtualMic
from voice_api import voice_api_system

# 启动虚拟麦克风
virtual_mic = SimpleVirtualMic()
virtual_mic.start_virtual_mic()

# 生成TTS并自动路由到虚拟麦克风
text = "你好，我是AI虚拟主播"
voice_api_system.text_to_speech(text, "temp.wav")

# 音频会自动通过虚拟麦克风输出到VTubeStudio
```

### 3. 实时监控

使用选项4监控音频电平，确保音频正常传输。

## 🎮 VTubeStudio集成

### 自动配置脚本

```python
from simple_virtual_mic import VTSTIntegration

vts_int = VTSTIntegration(virtual_mic)
vts_int.connect_to_vts()
vts_int.set_vts_audio_input()
```

### 手动配置步骤

1. 在VTubeStudio中设置麦克风输入为"VB-CABLE Input"
2. 调整音频增益（建议50-70%）
3. 启用降噪功能
4. 测试音频输入

## 📊 系统监控

### 实时状态监控

```bash
python simple_virtual_mic.py
# 选择选项4查看实时音频电平
```

### 性能指标
- **延迟**: <50ms
- **采样率**: 44.1kHz
- **位深度**: 16-bit
- **通道数**: 单声道

## 🔧 故障排除

### 常见问题

**1. 设备未找到**
```
解决: 重新安装VB-CABLE驱动，重启计算机
```

**2. 音频无声**
```
解决: 检查Windows音频设置，确认CABLE设备为默认
```

**3. VTubeStudio无法识别**
```
解决: 在VTubeStudio中手动选择VB-CABLE Input设备
```

**4. 音频断断续续**
```
解决: 调整缓冲区大小，降低音频处理负载
```

### 日志查看

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 最佳实践

### 性能优化
1. 关闭不必要的音频应用程序
2. 使用专用的USB声卡
3. 保持驱动程序更新
4. 定期重启音频服务

### 音质调优
1. 采样率保持44.1kHz
2. 启用音频增强功能
3. 调整合适的增益级别
4. 使用降噪算法

## 🔄 系统维护

### 定期检查
```bash
# 检查设备状态
python simple_virtual_mic.py
# 选择选项2进行测试
```

### 更新驱动
定期访问VB-Audio官网获取最新驱动版本。

## 💡 高级功能

### 多路音频路由
```python
# 可以同时路由多个音频源
# 实现背景音乐+语音的混合输出
```

### 自定义音频处理
```python
# 添加音频效果处理器
# 实现变声、混响等效果
```

---

**注意**: 使用前请确保已安装所有依赖库：
```bash
pip install pyaudio pyvts numpy requests
```