@echo off
REM 知识库编译系统 - 快速开始脚本 (Windows)

echo =====================================
echo 知识库编译系统 - 快速开始
echo =====================================
echo.

REM 检查 Python
echo [1/5] 检查 Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo.

REM 检查依赖
echo [2/5] 检查依赖...
DEPENDENCIES_OK=1

python -c "import langchain" >nul 2>&1
if %errorlevel% neq 0 (
    echo [缺失] langchain
    set DEPENDENCIES_OK=0
) else (
    echo [已安装] langchain
)

python -c "import langgraph" >nul 2>&1
if %errorlevel% neq 0 (
    echo [缺失] langgraph
    set DEPENDENCIES_OK=0
) else (
    echo [已安装] langgraph
)

python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo [缺失] fastapi
    set DEPENDENCIES_OK=0
) else (
    echo [已安装] fastapi
)

python -c "import pydantic" >nul 2>&1
if %errorlevel% neq 0 (
    echo [缺失] pydantic
    set DEPENDENCIES_OK=0
) else (
    echo [已安装] pydantic
)

echo.

REM 安装依赖
if %DEPENDENCIES_OK%==0 (
    echo [3/5] 安装依赖...
    echo.
    echo 选择安装方式:
    echo 1) 使用核心依赖（推荐，快速且稳定）
    echo 2) 使用 uv 包管理器（最快）
    echo.

    set /p install_choice="请选择 [1-2] (默认: 1): "

    if "%install_choice%"=="2" (
        echo.
        echo [安装] 安装 uv 包管理器...
        pip install uv -i https://mirrors.aliyun.com/pypi/simple/

        if %errorlevel% equ 0 (
            echo [安装] 使用 uv 安装依赖...
            uv sync

            if %errorlevel% neq 0 (
                echo [回退] uv 安装失败，尝试使用核心依赖...
                pip install -r requirements_core.txt -i https://mirrors.aliyun.com/pypi/simple/
            )
        )
    ) else (
        echo.
        echo [安装] 安装核心依赖...
        pip install -r requirements_core.txt -i https://mirrors.aliyun.com/pypi/simple/
    )

    if %errorlevel% equ 0 (
        echo.
        echo [成功] 依赖安装完成！
    ) else (
        echo.
        echo [错误] 依赖安装失败，请检查错误信息
        pause
        exit /b 1
    )
) else (
    echo [3/5] 跳过依赖安装（已安装）
)

echo.

REM 创建必要的目录
echo [4/5] 创建必要的目录...
if not exist "assets\knowledge_base\raw" mkdir assets\knowledge_base\raw
if not exist "assets\knowledge_base\wiki\indexes" mkdir assets\knowledge_base\wiki\indexes
if not exist "assets\knowledge_base\wiki\summaries" mkdir assets\knowledge_base\wiki\summaries
if not exist "assets\knowledge_base\wiki\concepts" mkdir assets\knowledge_base\wiki\concepts
if not exist "assets\knowledge_base\outputs\qa" mkdir assets\knowledge_base\outputs\qa
if not exist "assets\knowledge_base\outputs\health" mkdir assets\knowledge_base\outputs\health
if not exist "logs" mkdir logs
echo [成功] 目录创建完成

echo.

REM 启动服务
echo [5/5] 启动服务...
echo.
echo ====================================
echo 访问地址:
echo    Web 界面: 在浏览器中打开 index.html
echo    API 地址: http://localhost:5000
echo.
echo 常用命令:
echo    python client.py ingest "内容" --title "标题"
echo    python client.py qa "问题"
echo    python client.py health-check
echo.
echo 日志位置: logs\
echo.
echo 按 Ctrl+C 停止服务
echo ====================================
echo.

REM 启动服务
python src\main.py -m http -p 5000

pause
