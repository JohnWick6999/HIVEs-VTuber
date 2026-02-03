@echo off
:: VB-CABLE虚拟声卡一键安装脚本
:: 需要以管理员身份运行

echo ==================================================
echo VB-CABLE虚拟声卡一键安装程序
echo ==================================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 错误: 需要管理员权限来安装驱动程序
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo [1/4] 创建临时目录...
set TEMP_DIR=%TEMP%\vbcable_install
mkdir "%TEMP_DIR%" 2>nul

echo [2/4] 下载VB-CABLE驱动...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack45.zip' -OutFile '%TEMP_DIR%\VBCABLE.zip'}"

if not exist "%TEMP_DIR%\VBCABLE.zip" (
    echo 错误: 下载失败
    pause
    exit /b 1
)

echo [3/4] 解压驱动文件...
powershell -Command "& {Expand-Archive -Path '%TEMP_DIR%\VBCABLE.zip' -DestinationPath '%TEMP_DIR%' -Force}"

echo [4/4] 安装驱动程序...
"%TEMP_DIR%\VBCABLE_Setup_x64.exe" /S

if %errorLevel% equ 0 (
    echo.
    echo ==================================================
    echo ✅ VB-CABLE安装成功！
    echo ==================================================
    echo 请重启计算机以使驱动生效
    echo 重启后可以运行 configure_audio.py 进行配置
    echo.
) else (
    echo.
    echo ==================================================
    echo ❌ 安装失败，请检查错误信息
    echo ==================================================
)

echo 清理临时文件...
rmdir /s /q "%TEMP_DIR%" 2>nul

pause