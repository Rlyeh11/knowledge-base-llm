@echo off
REM 模型配置脚本 (Windows)
REM 用于快速配置和测试模型

setlocal enabledelayedexpansion

echo ========================================
echo   模型配置向导 (Windows)
echo ========================================
echo.

if "%~1"=="" (
    echo 使用方法:
    echo   configure_model.bat ^<model_type^> [model_id]
    echo.
    echo 支持的模型类型:
    echo   coze     - 豆包模型（Coze 平台）
    echo   deepseek - DeepSeek 模型
    echo   kimi     - Kimi 模型（月之暗面）
    echo   openai   - OpenAI 模型
    echo   custom   - 自定义模型
    echo.
    echo 示例:
    echo   configure_model.bat deepseek
    echo   configure_model.bat openai gpt-4
    echo.
    exit /b 1
)

set MODEL_TYPE=%~1
set MODEL_ID=%~2

REM 检查模型类型
if "%MODEL_TYPE%"=="coze" (
    set DEFAULT_MODEL_ID=doubao-seed-1-8-251228
    set API_TYPE=COZE
    set PROMPT_KEY=请输入 Coze API Key:
    set PROMPT_URL=请输入 Coze Workspace ID:
) else if "%MODEL_TYPE%"=="deepseek" (
    set DEFAULT_MODEL_ID=deepseek-chat
    set API_TYPE=OPENAI
    set PROMPT_KEY=请输入 DeepSeek API Key:
    set PROMPT_URL=https://api.deepseek.com/v1
) else if "%MODEL_TYPE%"=="kimi" (
    set DEFAULT_MODEL_ID=moonshot-v1-8k
    set API_TYPE=OPENAI
    set PROMPT_KEY=请输入 Kimi API Key:
    set PROMPT_URL=https://api.moonshot.cn/v1
) else if "%MODEL_TYPE%"=="openai" (
    set DEFAULT_MODEL_ID=gpt-4
    set API_TYPE=OPENAI
    set PROMPT_KEY=请输入 OpenAI API Key:
    set PROMPT_URL=https://api.openai.com/v1
) else if "%MODEL_TYPE%"=="custom" (
    set DEFAULT_MODEL_ID=custom-model
    set API_TYPE=OPENAI
    set PROMPT_KEY=请输入 API Key:
    set PROMPT_URL=请输入 API Base URL:
) else (
    echo [错误] 不支持的模型类型: %MODEL_TYPE%
    echo.
    echo 支持的类型: coze, deepseek, kimi, openai, custom
    exit /b 1
)

REM 使用自定义或默认模型 ID
if "%MODEL_ID%"=="" (
    set MODEL_ID=%DEFAULT_MODEL_ID%
    echo [使用] 默认模型 ID: %MODEL_ID%
) else (
    echo [使用] 自定义模型 ID: %MODEL_ID%
)

echo.
echo ========================================
echo   配置 %MODEL_TYPE% 模型
echo ========================================
echo.

REM 输入 API Key
set /p API_KEY="%PROMPT_KEY%"
if "%API_KEY%"=="" (
    echo [错误] API Key 不能为空
    exit /b 1
)

REM 输入额外配置（仅 Coze）
if "%API_TYPE%"=="COZE" (
    set /p WORKSPACE_ID="%PROMPT_URL%"
    if "%WORKSPACE_ID%"=="" (
        echo [错误] Workspace ID 不能为空
        exit /b 1
    )
    set BASE_URL=
) else (
    set BASE_URL=%PROMPT_URL%
)

REM 创建 .env 文件
echo.
echo [保存] 保存配置到 .env 文件...

(
    echo # ========================================
    echo # 模型配置
    echo # ========================================
    echo MODEL_TYPE=%API_TYPE%
    echo MODEL_ID=%MODEL_ID%
    echo.
    echo # API 配置
) > .env

if "%API_TYPE%"=="OPENAI" (
    (
        echo OPENAI_API_KEY=%API_KEY%
        echo OPENAI_BASE_URL=%BASE_URL%
    ) >> .env
) else (
    (
        echo COZE_API_KEY=%API_KEY%
        echo COZE_WORKSPACE_ID=%WORKSPACE_ID%
    ) >> .env
)

(
    echo.
    echo # ========================================
    echo # 其他配置
    echo # ========================================
    echo LOG_LEVEL=INFO
    echo MAX_WORKERS=4
) >> .env

echo [成功] 配置已保存到 .env 文件

REM 更新配置文件
echo.
echo [更新] 更新模型配置文件...

set CONFIG_FILES=config\summary_llm_cfg.json config\concept_extract_llm_cfg.json config\qa_llm_cfg.json config\health_check_llm_cfg.json

for %%f in (%CONFIG_FILES%) do (
    if exist "%%f" (
        REM 使用 PowerShell 替换模型 ID
        powershell -Command "(Get-Content '%%f') -replace '\"model\": \"[^\"]*\"', '\"model\": \"%MODEL_ID%\"' | Set-Content '%%f'"
        echo [成功] %%f
    ) else (
        echo [警告] %%f (不存在)
    )
)

REM 创建 .gitignore
if not exist .gitignore (
    echo.
    echo [创建] 创建 .gitignore 文件...
    (
        echo # 环境变量文件（包含敏感信息）
        echo .env
        echo.
        echo # Python
        echo __pycache__/
        echo *.py[cod]
        echo *$py.class
        echo *.so
        echo .Python
        echo build/
        echo develop-eggs/
        echo dist/
        echo downloads/
        echo eggs/
        echo .eggs/
        echo lib/
        echo lib64/
        echo parts/
        echo sdist/
        echo var/
        echo wheels/
        echo *.egg-info/
        echo .installed.cfg
        echo *.egg
        echo.
        echo # 日志
        echo logs/
        echo *.log
        echo.
        echo # IDE
        echo .vscode/
        echo .idea/
        echo *.swp
        echo *.swo
        echo *~
        echo.
        echo # 系统文件
        echo .DS_Store
        echo Thumbs.db
        echo.
        echo # 备份
        echo backup/
        echo *.backup
    ) > .gitignore
    echo [成功] .gitignore 已创建
)

REM 显示配置摘要
echo.
echo ========================================
echo   配置完成
echo ========================================
echo.
echo 配置摘要:
echo   模型类型: %MODEL_TYPE%
echo   模型 ID: %MODEL_ID%
echo   API 类型: %API_TYPE%
echo.
echo 配置文件:
echo   .env ^(环境变量^)
for %%f in (%CONFIG_FILES%) do (
    if exist "%%f" (
        echo   %%f
    )
)
echo.
echo 下一步:
echo   1. 重启服务:
echo      python src\main.py -m http -p 5000
echo.
echo   2. 测试配置:
echo      python client.py qa "测试连接"
echo.
echo   3. 查看日志:
echo      type logs\app.log
echo.
echo ========================================

endlocal
