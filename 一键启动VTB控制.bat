@echo off
cls
echo ========================================
echo    VTB角色动作控制器 - 一键启动
echo ========================================
echo.
echo 正在启动控制器...
echo 请确保:
echo 1. VTube Studio已在运行
echo 2. API端口8001已启用
echo 3. 准备在弹出窗口中授权连接
echo.
pause
cd /d D:\Project_LLM_VTB\src\backend
python simple_vtb_control.py
echo.
echo 程序已退出
pause