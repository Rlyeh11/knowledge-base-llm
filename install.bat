@echo off
REM 知识库编译系统 - 依赖安装脚本 (Windows)

echo =====================================
echo 知识库编译系统 - 依赖安装脚本
echo =====================================
echo.

REM 检查 Python
echo [1/3] 检查 Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo.

REM 检查 pip
echo [2/3] 检查 pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 pip，正在安装...
    python -m ensurepip --upgrade
)
echo.

REM 安装依赖
echo [3/3] 安装依赖...
echo.
echo 选择安装方式：
echo 1) 使用核心依赖（推荐，快速且稳定）
echo 2) 使用 uv 包管理器（最快，推荐）
echo 3) 使用完整依赖（包含桌面环境支持）
echo.

set /p choice="请选择 [1-3]: "

if "%choice%"=="1" (
    echo.
    echo [安装] 使用核心依赖安装...
    echo.
    
    pip install -r requirements_core.txt -i https://mirrors.aliyun.com/pypi/simple/
    
    if %errorlevel% equ 0 (
        echo [成功] 核心依赖安装成功！
    ) else (
        echo [失败] 核心依赖安装失败
        pause
        exit /b 1
    )
) else if "%choice%"=="2" (
    echo.
    echo [安装] 安装 uv 包管理器...
    pip install uv -i https://mirrors.aliyun.com/pypi/simple/
    
    if %errorlevel% neq 0 (
        echo [失败] uv 安装失败
        pause
        exit /b 1
    )
    
    echo.
    echo [安装] 使用 uv 安装依赖...
    uv sync
    
    if %errorlevel% equ 0 (
        echo [成功] 依赖安装成功！
    ) else (
        echo [失败] 依赖安装失败
        pause
        exit /b 1
    )
) else if "%choice%"=="3" (
    echo.
    echo [警告] 完整依赖包含桌面环境支持，需要额外的系统库
    echo [安装] 安装完整依赖...
    echo.
    
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
    
    if %errorlevel% equ 0 (
        echo [成功] 完整依赖安装成功！
    ) else (
        echo [失败] 完整依赖安装失败，建议使用选项1或2
        pause
        exit /b 1
    )
) else (
    echo [错误] 无效选择
    pause
    exit /b 1
)

echo.
echo =====================================
echo [完成] 安装完成！
echo =====================================
echo.

echo [验证] 验证核心依赖...
python -c "import langchain, langgraph, fastapi, pydantic" 2>nul
if %errorlevel% equ 0 (
    echo [成功] 核心依赖验证成功
) else (
    echo [失败] 核心依赖验证失败
    pause
    exit /b 1
)

echo.
echo =====================================
echo 启动服务
echo =====================================
echo.
echo 现在可以启动服务了：
echo    python src\main.py -m http -p 5000
echo.
echo 更多信息：
echo    - 安装指南: INSTALL.md
echo    - 使用指南: USAGE.md
echo.

pause
