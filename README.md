# 📚 知识库编译系统

一个基于 LLM 的个人知识库管理系统，实现资料的摄取、编译、问答和健康检查。基于 Karpathy 的"LLM Knowledge Bases"方法论设计。

## ✨ 特性

- **🔄 自动编译**：支持 Markdown、HTML、纯文本内容的自动摄取和编译
- **🤖 LLM 驱动**：自动生成摘要、抽取核心概念、智能问答
- **🔗 统一链接**：使用 Markdown 链接格式，支持跨文档引用
- **🏥 健康检查**：自动检测知识库一致性和完整性
- **📊 多模式支持**：摄取、问答、健康检查三种工作模式
- **🚀 多种部署方式**：支持本地部署、Docker 容器化部署

## 🏗️ 技术栈

- **核心框架**：LangGraph + FastAPI
- **编程语言**：Python 3.12+
- **大模型**：支持豆包/DeepSeek/Kimi 等多种 LLM
- **编码规范**：PEP 8，类型注解

## 📦 仓库信息

**仓库 URL：**
```
https://github.com/your-username/knowledge-base-system
```

**项目结构：**
```
knowledge-base-system/
├── requirements_core.txt      # 核心依赖（推荐）
├── requirements.txt           # 完整依赖
├── pyproject.toml             # 项目配置
├── Dockerfile                 # Docker 配置
├── docker-compose.yml         # Docker Compose 配置
├── install.sh                 # Linux/Mac 安装脚本
├── install.bat                # Windows 安装脚本
├── start.sh                   # 启动脚本
├── client.py                  # 命令行客户端
├── index.html                 # Web 界面
├── INSTALL.md                 # 安装指南 ⭐
├── USAGE.md                   # 使用指南
├── DOCKER.md                  # Docker 部署指南
├── AGENTS.md                  # 项目结构索引
└── src/                       # 源代码
    ├── agents/                # Agent 代码
    ├── graphs/                # 工作流编排
    ├── tools/                 # 工具定义
    ├── storage/               # 存储初始化
    └── main.py                # 主入口
```

## 🚀 快速开始

### 方式 1：使用 Docker（推荐）

```bash
# 克隆仓库
git clone https://github.com/your-username/knowledge-base-system.git
cd knowledge-base-system

# 使用 Docker Compose 启动
docker-compose up -d

# 访问服务
curl http://localhost:5000/health
```

### 方式 2：本地安装

#### Linux/Mac

```bash
# 使用安装脚本（推荐）
./install.sh

# 或手动安装核心依赖
pip install -r requirements_core.txt
```

#### Windows

```bash
# 使用安装脚本（推荐）
install.bat

# 或手动安装核心依赖
pip install -r requirements_core.txt
```

### 方式 3：使用 uv 包管理器（最快）

```bash
# 安装 uv
pip install uv

# 安装依赖
uv sync

# 启动服务
python src/main.py -m http -p 5000
```

## 📖 使用方法

### 1. 启动服务

```bash
# 启动 HTTP 服务
python src/main.py -m http -p 5000

# 或使用脚本
bash scripts/http_run.sh -m http -p 5000
```

### 2. 摄取内容

```bash
# 摄取 Markdown 内容
python client.py ingest "# 我的文档\n\n这是内容..." --title "我的文档" --type markdown

# 摄取文件
python client.py ingest-file --path documents/article.md --type markdown
```

### 3. 问答

```bash
# 问答
python client.py qa "什么是知识库编译？"

# 查看问答历史
python client.py qa-history
```

### 4. 健康检查

```bash
# 完整检查
python client.py health-check --mode full

# 仅检查一致性
python client.py health-check --mode consistency
```

### 5. Web 界面

在浏览器中打开 `index.html`，使用图形界面进行操作。

## 📚 文档

- **[INSTALL.md](./INSTALL.md)** - 详细安装指南，包含依赖问题解决方案
- **[USAGE.md](./USAGE.md)** - 完整使用指南
- **[DOCKER.md](./DOCKER.md)** - Docker 部署指南
- **[AGENTS.md](./AGENTS.md)** - 项目结构索引

## 🔧 配置

### 环境变量

```bash
# LLM 配置
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://api.example.com/v1"

# 服务配置
export LOG_LEVEL="INFO"
export MAX_WORKERS=4
export PORT=5000

# 存储配置
export STORAGE_TYPE="local"  # local | s3 | oss
export STORAGE_PATH="assets/knowledge_base"
```

### 配置文件

所有 LLM 配置文件位于 `config/` 目录：

```
config/
├── summary_llm_cfg.json         # 摘要生成
├── concept_extract_llm_cfg.json # 概念抽取
├── qa_llm_cfg.json              # 问答
└── health_check_llm_cfg.json    # 健康检查
```

## 🏥 健康检查

系统支持多种健康检查模式：

- **full**：完整检查（一致性、完整性、孤岛）
- **consistency**：仅检查概念定义冲突
- **completeness**：识别缺少定义/例子的概念
- **orphan**：发现孤立的概念条目

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- 基于 Andrej Karpathy 的 "LLM Knowledge Bases" 方法论
- 使用 LangGraph 框架构建工作流
- 感谢所有贡献者

## 📞 联系方式

- 问题反馈：提交 GitHub Issue
- 功能建议：提交 Feature Request

---

**快速链接：**
- [安装指南](./INSTALL.md) - 遇到依赖问题请看这里 ⭐
- [使用指南](./USAGE.md) - 详细使用说明
- [Docker 部署](./DOCKER.md) - 推荐的部署方式
- [仓库地址](https://github.com/your-username/knowledge-base-system) - GitHub 仓库
