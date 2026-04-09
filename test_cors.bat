@echo off
REM CORS 测试脚本 (Windows)

echo ============================================
echo CORS 配置测试工具 (Windows)
echo ============================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查 requests 库
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo [安装] 安装 requests 库...
    pip install requests
)

REM 运行测试
python test_cors.py

pause
