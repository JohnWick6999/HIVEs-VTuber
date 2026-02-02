@echo off
chcp 65001 >nul

rem 启动AI Vtuber Tool后端服务
echo 正在启动AI Vtuber Tool后端服务...

rem 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

rem 切换到后端目录
cd /d "%~dp0\src\backend"

rem 安装依赖
echo 正在安装依赖...
pip install -r requirements.txt

rem 启动后端服务
echo 正在启动后端服务...
python main.py

pause
