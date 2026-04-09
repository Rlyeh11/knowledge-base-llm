# 🚀 知识库编译系统 - 本地部署指南

## 依赖问题解决方案

### 问题说明
如果在安装依赖时遇到 `pygobject==3.48.2` 构建失败，这是因为这个包需要系统的C编译器和GObject库支持。对于知识库系统来说，这个包不是必需的，我们可以使用精简版的依赖。

### 解决方案

#### 方案1：使用核心依赖（推荐）

```bash
# 使用核心依赖文件
pip install -r requirements_core.txt
```

#### 方案2：使用 uv 包管理器（推荐）

```bash
# 安装 uv
pip install uv

# 使用 uv 安装依赖（更快，更可靠）
uv sync
```

#### 方案3：修改原始依赖

如果你想使用原始的 requirements.txt，可以移除这些不必要的包：

```bash
# 创建精简版依赖
cat requirements.txt | grep -v "pygobject\|dbus-python\|pycairo" > requirements_minimal.txt
pip install -r requirements_minimal.txt
```

### 快速安装脚本

```bash
#!/bin/bash

echo "🚀 开始安装知识库编译系统依赖..."

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "📌 Python 版本: $python_version"

# 方案1：使用核心依赖
echo "📦 安装核心依赖..."
pip install -r requirements_core.txt

# 方案2：安装 uv（可选但推荐）
if command -v uv &> /dev/null; then
    echo "✅ uv 已安装"
else
    echo "📦 安装 uv 包管理器..."
    pip install uv
fi

echo "✅ 依赖安装完成！"
echo ""
echo "🎯 现在可以运行服务了："
echo "   python src/main.py -m http -p 5000"
```

### 依赖对比

| 包名 | 用途 | 知识库需要 | 原因 |
|------|------|-----------|------|
| langchain, langgraph | 核心框架 | ✅ | 必需 |
| fastapi, uvicorn | Web服务 | ✅ | 必需 |
| pydantic | 数据验证 | ✅ | 必需 |
| pygobject | Linux桌面绑定 | ❌ | 仅用于Linux GUI应用 |
| dbus-python | D-Bus通信 | ❌ | 仅用于Linux桌面应用 |
| pycairo | 2D图形绘制 | ❌ | 仅用于图形界面 |
| opencv-python | 图像处理 | ⚠️ | 可选，仅用于图像处理 |

### 系统要求

**最低要求：**
- Python 3.8+
- pip 或 uv 包管理器
- 2GB+ 可用内存

**推荐配置：**
- Python 3.12+
- uv 包管理器（更快的依赖安装）
- 4GB+ 可用内存

### 安装验证

```bash
# 验证核心依赖
python -c "import langchain, langgraph, fastapi, pydantic"
echo "✅ 核心依赖验证成功"

# 启动服务
python src/main.py -m http -p 5000
```

### Docker 部署（推荐）

如果本地环境配置复杂，推荐使用 Docker：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装核心依赖
COPY requirements_core.txt .
RUN pip install --no-cache-dir -r requirements_core.txt

COPY . .

# 暴露端口
EXPOSE 5000

# 启动服务
CMD ["python", "src/main.py", "-m", "http", "-p", "5000"]
```

使用方法：
```bash
docker build -t knowledge-base .
docker run -p 5000:5000 -v $(pwd)/assets:/app/assets knowledge-base
```

### 常见问题

#### Q: pip install 速度慢怎么办？
A: 使用国内镜像源：
```bash
pip install -r requirements_core.txt -i https://mirrors.aliyun.com/pypi/simple/
```

#### Q: 某些依赖安装失败怎么办？
A: 使用 uv 包管理器，它能更好地处理依赖冲突：
```bash
pip install uv
uv sync
```

#### Q: Windows 环境下如何安装？
A: Windows 环境下通常不需要 pygobject，直接使用核心依赖即可：
```bash
pip install -r requirements_core.txt
```

#### Q: macOS 环境下如何安装？
A: macOS 环境下使用 Homebrew 安装必要的系统库：
```bash
brew install cairo gobject-introspection
pip install -r requirements_core.txt
```

### 仓库信息

**当前仓库 URL：**
```
https://github.com/your-username/knowledge-base-system
```

**项目结构：**
```
knowledge-base-system/
├── requirements_core.txt          # 核心依赖（推荐）
├── requirements.txt               # 完整依赖（可选）
├── pyproject.toml                # 项目配置
├── start.sh                      # 启动脚本
├── client.py                     # 命令行客户端
├── index.html                    # Web界面
├── USAGE.md                      # 使用指南
└── src/                          # 源代码
```

### 下一步

依赖安装完成后，请参考 [USAGE.md](./USAGE.md) 了解如何使用系统。

**快速启动：**
```bash
# 启动服务
python src/main.py -m http -p 5000

# 使用客户端
python client.py ingest "测试内容" --title "测试"

# 使用Web界面
# 在浏览器中打开 index.html
```

### 获取帮助

如果遇到其他问题，请：
1. 检查 [USAGE.md](./USAGE.md) 中的常见问题
2. 查看服务日志：`/app/work/logs/bypass/app.log`
3. 提交 Issue 到仓库

---
**注意：** 建议使用 `requirements_core.txt` 进行依赖安装，这样可以避免桌面环境相关的依赖问题，确保在各种操作系统上都能正常运行。
