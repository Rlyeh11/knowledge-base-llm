#!/bin/bash

echo "🚀 启动知识库编译系统..."
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python 3.8+"
    exit 1
fi

# 检查端口占用
PORT=5000
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  端口 $PORT 已被占用，尝试使用端口 8000..."
    PORT=8000
fi

echo "📡 服务将在 http://localhost:$PORT 启动"
echo "💡 按 Ctrl+C 停止服务"
echo ""

# 启动服务
python3 src/main.py -m http -p $PORT
