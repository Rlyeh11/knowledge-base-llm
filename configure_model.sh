#!/bin/bash

# 模型配置脚本
# 用于快速配置和测试模型

echo "========================================"
echo "  模型配置向导"
echo "========================================"
echo ""

# 检查是否提供了参数
if [ $# -eq 0 ]; then
    echo "使用方法:"
    echo "  ./configure_model.sh <model_type> [model_id]"
    echo ""
    echo "支持的模型类型:"
    echo "  coze     - 豆包模型（Coze 平台）"
    echo "  deepseek - DeepSeek 模型"
    echo "  kimi     - Kimi 模型（月之暗面）"
    echo "  openai   - OpenAI 模型"
    echo "  custom   - 自定义模型"
    echo ""
    echo "示例:"
    echo "  ./configure_model.sh deepseek"
    echo "  ./configure_model.sh openai gpt-4"
    echo ""
    exit 1
fi

MODEL_TYPE=$1
MODEL_ID=$2

# 模型配置映射
declare -A MODEL_CONFIGS

# Coze 配置
MODEL_CONFIGS[coze]="doubao-seed-1-8-251228|COZE|请输入 Coze API Key:|请输入 Coze Workspace ID:"

# DeepSeek 配置
MODEL_CONFIGS[deepseek]="deepseek-chat|OPENAI|请输入 DeepSeek API Key:|https://api.deepseek.com/v1"

# Kimi 配置
MODEL_CONFIGS[kimi]="moonshot-v1-8k|OPENAI|请输入 Kimi API Key:|https://api.moonshot.cn/v1"

# OpenAI 配置
MODEL_CONFIGS[openai]="gpt-4|OPENAI|请输入 OpenAI API Key:|https://api.openai.com/v1"

# 自定义配置
MODEL_CONFIGS[custom]="custom-model|OPENAI|请输入 API Key:|请输入 API Base URL:"

# 检查模型类型是否支持
if [ -z "${MODEL_CONFIGS[$MODEL_TYPE]}" ]; then
    echo "❌ 不支持的模型类型: $MODEL_TYPE"
    echo ""
    echo "支持的类型: coze, deepseek, kimi, openai, custom"
    exit 1
fi

# 解析配置
IFS='|' read -r DEFAULT_MODEL_ID API_TYPE PROMPT_KEY PROMPT_URL <<< "${MODEL_CONFIGS[$MODEL_TYPE]}"

# 如果没有提供 MODEL_ID，使用默认值
if [ -z "$MODEL_ID" ]; then
    MODEL_ID=$DEFAULT_MODEL_ID
    echo "📝 使用默认模型 ID: $MODEL_ID"
else
    echo "📝 使用自定义模型 ID: $MODEL_ID"
fi

echo ""
echo "========================================"
echo "  配置 $MODEL_TYPE 模型"
echo "========================================"
echo ""

# 输入 API Key
read -p "$PROMPT_KEY" API_KEY
if [ -z "$API_KEY" ]; then
    echo "❌ API Key 不能为空"
    exit 1
fi

# 输入 Workspace ID（仅 Coze）
if [ "$API_TYPE" == "COZE" ]; then
    read -p "$PROMPT_URL" WORKSPACE_ID
    if [ -z "$WORKSPACE_ID" ]; then
        echo "❌ Workspace ID 不能为空"
        exit 1
    fi
    BASE_URL=""
else
    BASE_URL=$PROMPT_URL
fi

# 创建或更新 .env 文件
echo ""
echo "💾 保存配置到 .env 文件..."

cat > .env << EOF
# ========================================
# 模型配置
# ========================================
MODEL_TYPE=$API_TYPE
MODEL_ID=$MODEL_ID

# API 配置
EOF

if [ "$API_TYPE" == "OPENAI" ]; then
    cat >> .env << EOF
OPENAI_API_KEY=$API_KEY
OPENAI_BASE_URL=$BASE_URL
EOF
else
    cat >> .env << EOF
COZE_API_KEY=$API_KEY
COZE_WORKSPACE_ID=$WORKSPACE_ID
EOF
fi

cat >> .env << EOF

# ========================================
# 其他配置
# ========================================
LOG_LEVEL=INFO
MAX_WORKERS=4
EOF

echo "✅ 配置已保存到 .env 文件"

# 更新配置文件
echo ""
echo "🔄 更新模型配置文件..."

CONFIG_FILES=(
    "config/summary_llm_cfg.json"
    "config/concept_extract_llm_cfg.json"
    "config/qa_llm_cfg.json"
    "config/health_check_llm_cfg.json"
)

for config_file in "${CONFIG_FILES[@]}"; do
    if [ -f "$config_file" ]; then
        # 使用 sed 替换模型 ID
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/\"model\": \"[^\"]*\"/\"model\": \"$MODEL_ID\"/g" "$config_file"
        else
            # Linux
            sed -i "s/\"model\": \"[^\"]*\"/\"model\": \"$MODEL_ID\"/g" "$config_file"
        fi
        echo "  ✅ $config_file"
    else
        echo "  ⚠️  $config_file (不存在)"
    fi
done

# 创建 .gitignore（如果不存在）
if [ ! -f .gitignore ]; then
    echo ""
    echo "📝 创建 .gitignore 文件..."
    cat > .gitignore << EOF
# 环境变量文件（包含敏感信息）
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 日志
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 系统文件
.DS_Store
Thumbs.db

# 备份
backup/
*.backup
EOF
    echo "✅ .gitignore 已创建"
fi

# 显示配置摘要
echo ""
echo "========================================"
echo "  配置完成"
echo "========================================"
echo ""
echo "📋 配置摘要:"
echo "  模型类型: $MODEL_TYPE"
echo "  模型 ID: $MODEL_ID"
echo "  API 类型: $API_TYPE"
echo ""
echo "📁 配置文件:"
echo "  .env (环境变量)"
for config_file in "${CONFIG_FILES[@]}"; do
    if [ -f "$config_file" ]; then
        echo "  $config_file"
    fi
done
echo ""
echo "🚀 下一步:"
echo "  1. 重启服务:"
echo "     python src/main.py -m http -p 5000"
echo ""
echo "  2. 测试配置:"
echo "     python client.py qa \"测试连接\""
echo ""
echo "  3. 查看日志:"
echo "     tail -f logs/app.log"
echo ""
echo "========================================"
