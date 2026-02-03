@echo off
cls
title VTB现成方案一键启动
color 0A

echo ========================================
echo    VTB角色动作控制 - 现成方案
echo ========================================
echo.
echo 正在检查和安装依赖...
echo.

:: 检查并安装pyvts
pip show pyvts >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装pyvts库...
    pip install pyvts
    if %errorlevel% neq 0 (
        echo 安装失败，请手动运行: pip install pyvts
        pause
        exit /b 1
    )
    echo pyvts安装完成!
) else (
    echo pyvts已安装
)

echo.
echo 请确保:
echo 1. VTube Studio正在运行
echo 2. API功能已启用(端口8001)
echo 3. 已在VTB中设置热键
echo.
pause

:: 运行控制程序
cd /d D:\Project_LLM_VTB\src\backend
python ready_vtb_control.py

echo.
echo 程序已退出
pause