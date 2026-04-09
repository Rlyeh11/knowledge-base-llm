@echo off
REM 环境变量配置脚本 (Windows)
REM 从 .env.example 创建 .env 文件

echo ========================================
echo   环境变量配置向导 (Windows)
echo ========================================
echo.

REM 检查 .env.example 是否存在
if not exist ".env.example" (
    echo [错误] 找不到 .env.example 文件
    echo.
    pause
    exit /b 1
)

REM 检查 .env 文件是否已存在
if exist ".env" (
    echo [警告] .env 文件已存在
    echo.

    set /p overwrite="是否覆盖现有 .env 文件？(y/n): "
    if /i not "%overwrite%"=="y" (
        echo 已取消操作
        pause
        exit /b 0
    )

    REM 备份现有文件
    for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
    set backup_file=.env.backup.%datetime:~0,14%
    echo [备份] 备份现有文件到: %backup_file%
    copy .env %backup_file% >nul
)

REM 复制模板
echo.
echo [创建] 从 .env.example 创建 .env 文件...
copy .env.example .env >nul

echo.
echo ========================================
echo   配置完成
echo ========================================
echo.
echo 下一步:
echo   1. 编辑 .env 文件
echo      notepad .env
echo.
echo   2. 填写必需的配置值（API Key 等）
echo.
echo   3. 测试配置
echo      python tools\test_model_config.py
echo.
echo   4. 启动服务
echo      python src\main.py -m http -p 5000
echo.
echo 参考文档:
echo   - docs\MODEL_CONFIG.md
echo   - docs\FAQ.md
echo.
echo ========================================

pause
