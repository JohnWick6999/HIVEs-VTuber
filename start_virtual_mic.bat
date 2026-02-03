@echo off
:: 虚拟麦克风一键启动脚本

echo ========================================
echo 虚拟麦克风系统启动器
echo ========================================
echo.

:: 检查Python环境
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 未找到Python环境
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

:: 检查必要依赖
echo 检查依赖库...
python -c "import pyaudio" >nul 2>&1
if %errorLevel% neq 0 (
    echo 安装必要依赖...
    pip install pyaudio numpy psutil
)

:: 启动主程序
echo 启动虚拟麦克风系统...
python virtual_mic_demo.py

pause