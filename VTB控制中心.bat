@echo off
cls
title VTB综合控制中心
color 0A

echo ========================================
echo     VTB角色综合控制中心
echo ========================================
echo.
echo 功能选择:
echo 1. 基础动作控制 (simple_vtb_control.py)
echo 2. 面部追踪控制 (vtb_face_tracker.py)  
echo 3. 综合控制面板 (vtb_control_panel.py)
echo 4. 自动测试诊断 (vtb_debug_test.py)
echo 5. 退出
echo.
echo 请确保:
echo • VTube Studio正在运行
echo • API功能已启用(端口8001)
echo • 已在VTB中设置相应热键
echo ========================================
echo.

:menu
set /p choice=请选择功能 (1-5): 

if "%choice%"=="1" (
    echo 启动基础动作控制...
    cd /d D:\Project_LLM_VTB\src\backend
    python simple_vtb_control.py
    goto menu
)

if "%choice%"=="2" (
    echo 启动面部追踪控制...
    cd /d D:\Project_LLM_VTB\src\backend
    python vtb_face_tracker.py
    goto menu
)

if "%choice%"=="3" (
    echo 启动综合控制面板...
    cd /d D:\Project_LLM_VTB\src\backend
    python vtb_control_panel.py
    goto menu
)

if "%choice%"=="4" (
    echo 启动自动测试诊断...
    cd /d D:\Project_LLM_VTB\src\backend
    python vtb_debug_test.py
    goto menu
)

if "%choice%"=="5" (
    echo 感谢使用VTB控制中心!
    exit
)

echo 无效选择，请重新输入
goto menu