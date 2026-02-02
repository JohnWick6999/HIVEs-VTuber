@echo off
chcp 65001 >nul

rem 启动AI Vtuber Tool前端应用
echo 正在启动AI Vtuber Tool前端应用...

rem 检查dotnet是否安装
dotnet --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到dotnet，请先安装dotnet 8.0或更高版本
    pause
    exit /b 1
)

rem 切换到前端目录
cd /d "%~dp0\src\frontend"

rem 构建前端应用
echo 正在构建前端应用...
dotnet build

if %errorlevel% neq 0 (
    echo 错误: 前端构建失败
    pause
    exit /b 1
)

rem 运行前端应用
echo 正在运行前端应用...
dotnet run

pause
