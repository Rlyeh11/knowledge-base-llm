#!/bin/bash

# 知识库编译系统 - 快速开始脚本

echo "🚀 知识库编译系统 - 快速开始"
echo "====================================="
echo ""

# 检查操作系统
OS="unknown"
case "$OSTYPE" in
  linux-gnu*) OS="linux" ;;
  darwin*)   OS="mac" ;;
  cygwin*)   OS="windows" ;;
  msys*)     OS="windows" ;;
  win32*)    OS="windows" ;;
  *)         OS="unknown" ;;
esac

echo "📌 检测到操作系统: $OS"
echo ""

# 检查 Python
echo "📌 检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✅ $PYTHON_VERSION"
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    PYTHON_VERSION=$(python --version 2>&1)
    echo "✅ $PYTHON_VERSION"
else
    echo "❌ 未找到 Python，请先安装 Python 3.8+"
    echo "📥 下载地址: https://www.python.org/downloads/"
    exit 1
fi

echo ""

# 检查依赖
echo "📌 检查依赖..."
DEPENDENCIES_OK=true

check_dependency() {
    if $PYTHON_CMD -c "import $1" 2>/dev/null; then
        echo "✅ $1 已安装"
    else
        echo "❌ $1 未安装"
        DEPENDENCIES_OK=false
    fi
}

check_dependency "langchain"
check_dependency "langgraph"
check_dependency "fastapi"
check_dependency "pydantic"

echo ""

if [ "$DEPENDENCIES_OK" = false ]; then
    echo "📦 检测到缺少依赖，正在安装..."
    echo ""

    # 选择安装方式
    echo "选择安装方式："
    echo "1) 使用核心依赖（推荐，快速且稳定）"
    echo "2) 使用 uv 包管理器（最快）"
    echo ""
    read -p "请选择 [1-2] (默认: 1): " install_choice

    case $install_choice in
        2|"2"|"uv"|"2)"|"2 ")
            echo ""
            echo "📦 安装 uv 包管理器..."
            pip install uv -i https://mirrors.aliyun.com/pypi/simple/

            if [ $? -eq 0 ]; then
                echo "📦 使用 uv 安装依赖..."
                uv sync

                if [ $? -ne 0 ]; then
                    echo "❌ uv 安装失败，尝试使用核心依赖..."
                    pip install -r requirements_core.txt -i https://mirrors.aliyun.com/pypi/simple/
                fi
            fi
            ;;
        *)
            echo ""
            echo "📦 安装核心依赖..."
            pip install -r requirements_core.txt -i https://mirrors.aliyun.com/pypi/simple/
            ;;
    esac

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ 依赖安装完成！"
    else
        echo ""
        echo "❌ 依赖安装失败，请检查错误信息"
        exit 1
    fi
else
    echo "✅ 所有依赖已安装"
fi

echo ""

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p assets/knowledge_base/{raw,wiki/{indexes,summaries,concepts},outputs/{qa,health}}
mkdir -p logs
echo "✅ 目录创建完成"

echo ""

# 启动服务
echo "🚀 启动服务..."
echo ""

# 检查端口是否被占用
PORT=5000
if command -v lsof &> /dev/null; then
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  端口 $PORT 已被占用"
        read -p "是否使用端口 5001? (y/n): " use_new_port
        if [[ $use_new_port == "y" ]]; then
            PORT=5001
        else
            echo "❌ 取消启动"
            exit 1
        fi
    fi
fi

echo "🌐 启动 HTTP 服务 (端口: $PORT)..."
echo ""
echo "====================================="
echo "📖 访问地址:"
echo "   Web 界面: 在浏览器中打开 index.html"
echo "   API 地址: http://localhost:$PORT"
echo ""
echo "📚 常用命令:"
echo "   python client.py ingest \"内容\" --title \"标题\""
echo "   python client.py qa \"问题\""
echo "   python client.py health-check"
echo ""
echo "📝 日志位置: logs/"
echo ""
echo "按 Ctrl+C 停止服务"
echo "====================================="
echo ""

# 启动服务
$PYTHON_CMD src/main.py -m http -p $PORT
