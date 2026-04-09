#!/bin/bash

# 环境变量配置脚本
# 从 .env.example 创建 .env 文件

echo "========================================"
echo "  环境变量配置向导"
echo "========================================"
echo ""

# 检查 .env.example 是否存在
if [ ! -f ".env.example" ]; then
    echo "❌ 错误: 找不到 .env.example 文件"
    echo ""
    exit 1
fi

# 检查 .env 文件是否已存在
if [ -f ".env" ]; then
    echo "⚠️  警告: .env 文件已存在"
    echo ""
    read -p "是否覆盖现有 .env 文件？(y/n): " overwrite

    if [ "$overwrite" != "y" ] && [ "$overwrite" != "Y" ]; then
        echo "已取消操作"
        exit 0
    fi

    # 备份现有文件
    backup_file=".env.backup.$(date +%Y%m%d_%H%M%S)"
    echo "💾 备份现有文件到: $backup_file"
    cp .env "$backup_file"
fi

# 询问配置方式
echo ""
echo "请选择配置方式:"
echo "1) 交互式配置（推荐）"
echo "2) 使用 .env.example 模板"
echo "3) 使用预设配置"
echo ""
read -p "请选择 [1-3] (默认: 1): " config_mode

case $config_mode in
    2|"2")
        echo ""
        echo "📝 使用 .env.example 模板..."
        cp .env.example .env
        echo "✅ 已创建 .env 文件"
        echo ""
        echo "⚠️  请编辑 .env 文件，填入你的实际配置值"
        echo ""
        exit 0
        ;;
    3|"3")
        echo ""
        echo "📝 使用预设配置..."
        ;;
    *)
        config_mode=1
        ;;
esac

# 交互式配置
if [ "$config_mode" == "1" ]; then
    echo ""
    echo "========================================"
    echo "  交互式配置"
    echo "========================================"
    echo ""

    # 复制模板
    cp .env.example .env

    # 询问模型类型
    echo "🤖 模型配置"
    echo "请选择模型类型:"
    echo "1) DeepSeek (推荐，免费额度)"
    echo "2) Kimi (月之暗面)"
    echo "3) OpenAI (官方)"
    echo "4) 豆包 (Coze)"
    echo "5) 自定义"
    echo ""
    read -p "请选择 [1-5]: " model_choice

    case $model_choice in
        1|"1")
            MODEL_TYPE=openai
            MODEL_ID=deepseek-chat
            OPENAI_BASE_URL=https://api.deepseek.com/v1
            echo "📝 已选择: DeepSeek"
            ;;
        2|"2")
            MODEL_TYPE=openai
            MODEL_ID=moonshot-v1-8k
            OPENAI_BASE_URL=https://api.moonshot.cn/v1
            echo "📝 已选择: Kimi"
            ;;
        3|"3")
            MODEL_TYPE=openai
            MODEL_ID=gpt-4
            OPENAI_BASE_URL=https://api.openai.com/v1
            echo "📝 已选择: OpenAI"
            ;;
        4|"4")
            MODEL_TYPE=coze
            MODEL_ID=doubao-seed-1-8-251228
            echo "📝 已选择: 豆包"
            ;;
        *)
            MODEL_TYPE=custom
            MODEL_ID=custom-model
            OPENAI_BASE_URL=https://api.example.com/v1
            echo "📝 已选择: 自定义"
            ;;
    esac

    # 输入 API Key
    echo ""
    read -p "请输入 API Key: " api_key
    if [ -z "$api_key" ]; then
        echo "⚠️  警告: API Key 未设置，请在 .env 文件中手动配置"
    fi

    # 更新 .env 文件
    if [ "$MODEL_TYPE" == "openai" ]; then
        sed -i "s/^MODEL_TYPE=.*/MODEL_TYPE=$MODEL_TYPE/" .env
        sed -i "s/^MODEL_ID=.*/MODEL_ID=$MODEL_ID/" .env
        sed -i "s|^OPENAI_BASE_URL=.*|OPENAI_BASE_URL=$OPENAI_BASE_URL|" .env

        if [ -n "$api_key" ]; then
            sed -i "s|^OPENAI_API_KEY=.*|OPENAI_API_KEY=$api_key|" .env
        fi
    elif [ "$MODEL_TYPE" == "coze" ]; then
        sed -i "s/^MODEL_TYPE=.*/MODEL_TYPE=$MODEL_TYPE/" .env
        sed -i "s/^MODEL_ID=.*/MODEL_ID=$MODEL_ID/" .env

        if [ -n "$api_key" ]; then
            sed -i "s|^COZE_API_KEY=.*|COZE_API_KEY=$api_key|" .env
        fi

        echo ""
        read -p "请输入 Coze Workspace ID: " workspace_id
        if [ -n "$workspace_id" ]; then
            sed -i "s|^COZE_WORKSPACE_ID=.*|COZE_WORKSPACE_ID=$workspace_id|" .env
        fi
    fi

    echo ""
    echo "✅ 基础配置已完成"
fi

echo ""
echo "========================================"
echo "  配置完成"
echo "========================================"
echo ""
echo "📝 下一步:"
echo "  1. 检查并编辑 .env 文件"
echo "     nano .env  或  vim .env"
echo ""
echo "  2. 填写必需的配置值（API Key 等）"
echo ""
echo "  3. 测试配置"
echo "     python tools/test_model_config.py"
echo ""
echo "  4. 启动服务"
echo "     python src/main.py -m http -p 5000"
echo ""
echo "📚 参考文档:"
echo "  - docs/MODEL_CONFIG.md"
echo "  - docs/FAQ.md"
echo ""
echo "========================================"
