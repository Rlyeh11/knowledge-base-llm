#!/bin/bash

# 知识库编译系统 - 依赖安装脚本

echo "🚀 知识库编译系统 - 依赖安装脚本"
echo "====================================="
echo ""

# 检查 Python 版本
echo "📌 检查 Python 版本..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    python3 --version
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    python --version
else
    echo "❌ 未找到 Python，请先安装 Python 3.8+"
    exit 1
fi

echo ""

# 检查 pip
echo "📌 检查 pip..."
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到 pip，正在安装..."
    $PYTHON_CMD -m ensurepip --upgrade
fi

echo ""
echo "🎯 选择安装方式："
echo "1) 使用核心依赖（推荐，快速且稳定）"
echo "2) 使用 uv 包管理器（最快，推荐）"
echo "3) 使用完整依赖（包含桌面环境支持）"
echo ""
read -p "请选择 [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "📦 使用核心依赖安装..."
        
        # 使用国内镜像加速
        pip install -r requirements_core.txt -i https://mirrors.aliyun.com/pypi/simple/
        
        if [ $? -eq 0 ]; then
            echo "✅ 核心依赖安装成功！"
        else
            echo "❌ 核心依赖安装失败"
            exit 1
        fi
        ;;
    2)
        echo ""
        echo "📦 安装 uv 包管理器..."
        pip install uv -i https://mirrors.aliyun.com/pypi/simple/
        
        if [ $? -ne 0 ]; then
            echo "❌ uv 安装失败"
            exit 1
        fi
        
        echo ""
        echo "📦 使用 uv 安装依赖..."
        uv sync
        
        if [ $? -eq 0 ]; then
            echo "✅ 依赖安装成功！"
        else
            echo "❌ 依赖安装失败"
            exit 1
        fi
        ;;
    3)
        echo ""
        echo "⚠️  完整依赖包含桌面环境支持，需要 C 编译器和系统库"
        echo "📦 安装完整依赖..."
        
        # 检测操作系统
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            echo "📌 检测到 Linux 系统"
            echo "💡 提示：如果遇到 pygobject 编译错误，请先安装系统依赖："
            echo "   Ubuntu/Debian: sudo apt-get install libgirepository1.0-dev libcairo2-dev"
            echo "   CentOS/RHEL: sudo yum install gobject-introspection-devel cairo-devel"
            echo ""
            read -p "是否继续？ (y/n): " confirm
            if [[ $confirm != "y" ]]; then
                echo "❌ 已取消安装"
                exit 1
            fi
        fi
        
        pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
        
        if [ $? -eq 0 ]; then
            echo "✅ 完整依赖安装成功！"
        else
            echo "❌ 完整依赖安装失败，建议使用选项1或2"
            exit 1
        fi
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "🎉 安装完成！"
echo ""
echo "📋 验证安装："

# 验证核心依赖
$PYTHON_CMD -c "import langchain, langgraph, fastapi, pydantic" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ 核心依赖验证成功"
else
    echo "❌ 核心依赖验证失败"
    exit 1
fi

echo ""
echo "🚀 现在可以启动服务了："
echo "   python src/main.py -m http -p 5000"
echo ""
echo "📖 更多信息请查看："
echo "   - 安装指南: INSTALL.md"
echo "   - 使用指南: USAGE.md"
