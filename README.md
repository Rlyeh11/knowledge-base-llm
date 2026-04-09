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

**项目结构：**
```
knowledge-base-system/
├── README.md                 # 主文档（从这里开始）
├── Makefile                  # 命令快捷方式
├── pyproject.toml            # 项目配置
├── requirements.txt          # 完整依赖
├── requirements_core.txt     # 核心依赖（推荐）
├── Dockerfile                # Docker 配置
├── docker-compose.yml        # Docker Compose 配置
├── .gitignore                # Git 忽略文件
├── .coze                     # Coze 配置
├── docs/                     # 📁 文档目录
│   ├── index.md              # 文档索引
│   ├── INSTALL.md            # 安装指南 ⭐
│   ├── MODEL_QUICK_START.md  # 模型配置快速开始 ⭐
│   ├── MODEL_CONFIG.md       # 模型配置详细指南
│   ├── CORS_QUICK_FIX.md     # CORS 快速修复 ⭐
│   ├── CORS_FIX.md           # CORS 详细文档
│   ├── FAQ.md                # 常见问题汇总
│   ├── DEPLOYMENT.md         # 部署指南
│   ├── DOCKER.md             # Docker 部署指南
│   ├── USAGE.md              # 使用指南
│   ├── README_KNOWLEDGE_BASE.md  # 知识库系统说明
│   └── CLEANUP_PLAN.md       # 目录整理方案
├── scripts/                  # 📁 安装和配置脚本
│   ├── install.sh            # Linux/Mac 安装脚本
│   ├── install.bat           # Windows 安装脚本
│   ├── configure_model.sh    # Linux/Mac 模型配置脚本 ⭐
│   ├── configure_model.bat   # Windows 模型配置脚本 ⭐
│   ├── quickstart.sh         # Linux/Mac 快速开始脚本
│   ├── quickstart.bat        # Windows 快速开始脚本
│   └── start.sh              # 启动脚本
├── tools/                    # 📁 测试工具
│   ├── client.py             # 命令行客户端
│   ├── test_model_config.py  # 模型配置测试脚本 ⭐
│   ├── test_model_config.bat # Windows 测试脚本
│   ├── test_cors.py          # CORS 测试脚本
│   └── test_cors.bat         # Windows 测试脚本
├── assets/                   # 📁 资源文件
│   └── knowledge_base/       # 知识库数据
├── config/                   # 📁 模型配置文件
│   ├── summary_llm_cfg.json
│   ├── concept_extract_llm_cfg.json
│   ├── qa_llm_cfg.json
│   └── health_check_llm_cfg.json
├── src/                      # 📁 源代码
│   ├── agents/               # Agent 代码
│   ├── graphs/               # 工作流编排
│   ├── tools/                # 工具定义
│   ├── storage/              # 存储初始化
│   └── main.py               # 主入口
├── scripts/                  # 📁 原有脚本
├── .venv/                    # 📁 虚拟环境
└── uv.lock                   # uv 锁文件
```

## 🚀 快速开始

### 方式 1：使用 Docker（推荐）

```bash
# 克隆仓库
git clone https://github.com/Rlyeh11/knowledge-base-llm.git
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

### 快速配置环境变量

**方式 1: 使用配置脚本（推荐）**

```bash
# Linux/Mac
./scripts/setup_env.sh

# Windows
scripts\setup_env.bat
```

**方式 2: 手动配置**

```bash
# 1. 复制环境变量模板
cp .env.example .env

# 2. 编辑 .env 文件
nano .env  # 或使用你喜欢的编辑器

# 3. 填写必需的配置值（如 API Key）
```

**方式 3: 使用配置脚本（模型）**

```bash
# 配置 DeepSeek 模型
make model-deepseek

# 配置 Kimi 模型
make model-kimi

# 配置 OpenAI 模型
make model-openai model=gpt-4

# 测试配置
make model-test
```

### 环境变量说明

项目使用 `.env` 文件管理环境变量，参考 `.env.example` 查看所有可用配置。

**主要环境变量**:

| 变量名 | 说明 | 必填 | 示例 |
|--------|------|------|------|
| `MODEL_TYPE` | 模型类型 | 是 | `openai`, `coze` |
| `MODEL_ID` | 模型 ID | 是 | `deepseek-chat` |
| `OPENAI_API_KEY` | OpenAI API Key | MODEL_TYPE=openai 时必填 | `sk-xxxx` |
| `OPENAI_BASE_URL` | API Base URL | 否 | `https://api.deepseek.com/v1` |
| `LOG_LEVEL` | 日志级别 | 否 | `INFO`, `DEBUG` |
| `MAX_WORKERS` | 最大工作进程数 | 否 | `4` |
| `PORT` | 服务端口 | 否 | `5000` |
| `STORAGE_TYPE` | 存储类型 | 否 | `local`, `s3`, `oss` |

**详细说明**:
- 完整的环境变量列表: [`.env.example`](./.env.example)
- 详细配置指南: [docs/MODEL_CONFIG.md](./docs/MODEL_CONFIG.md)

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

## ❓ 常见问题

### 1. 模型授权失败

**问题**: 本地运行时出现模型授权失败错误

**原因**: API Key 未配置或配置错误

**解决方案**:
```bash
# 方式 1: 使用配置脚本（推荐）
./configure_model.sh deepseek    # 使用 DeepSeek
./configure_model.sh openai gpt-4  # 使用 OpenAI

# 方式 2: 手动配置
# 1. 创建 .env 文件
echo "MODEL_TYPE=openai" > .env
echo "MODEL_ID=deepseek-chat" >> .env
echo "OPENAI_API_KEY=your-api-key" >> .env
echo "OPENAI_BASE_URL=https://api.deepseek.com/v1" >> .env

# 2. 更新配置文件中的 model ID
# 编辑 config/*.json 文件，将 model 字段改为你的模型 ID

# 3. 测试配置
python test_model_config.py

# 4. 重启服务
python src/main.py -m http -p 5000
```

**详细信息**: [模型配置指南](./MODEL_CONFIG.md) ⭐

### 2. LLM API 配置

**问题**: 请求超时或返回错误

**解决方案**:
- 在 `.env` 文件中配置正确的 API Key
- 检查 API 服务是否可用
- 查看 `logs/app.log` 了解详细错误信息

**详细信息**: [模型配置指南](./MODEL_CONFIG.md)

### 3. Docker 部署问题

**问题**: Docker 容器无法启动

**解决方案**:
- 检查 Docker 是否正在运行：`docker ps`
- 查看容器日志：`docker-compose logs -f knowledge-base`
- 确保端口 5000 没有被占用

**详细信息**: [Docker 部署指南](./DOCKER.md)

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
- [📚 文档索引](./docs/index.md) - 所有文档总览 ⭐
- [模型配置快速开始](./docs/MODEL_QUICK_START.md) - 模型配置快速解决 ⭐
- [安装指南](./docs/INSTALL.md) - 遇到依赖问题请看这里 ⭐
- [使用指南](./docs/USAGE.md) - 详细使用说明
- [CORS 快速修复](./docs/CORS_QUICK_FIX.md) - CORS 跨域问题快速解决 ⭐
- [常见问题 FAQ](./docs/FAQ.md) - 常见问题汇总
- [部署指南](./docs/DEPLOYMENT.md) - 多种部署方式
- [Docker 部署](./docs/DOCKER.md) - 推荐的部署方式
- [仓库地址](https://github.com/your-username/knowledge-base-system) - GitHub 仓库
