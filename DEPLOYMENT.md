# 🚀 部署指南

本文档提供知识库编译系统的多种部署方式，适用于不同的使用场景和环境。

## 📋 部署方式概览

| 部署方式 | 推荐程度 | 适用场景 | 复杂度 | 性能 |
|---------|---------|---------|--------|------|
| Docker | ⭐⭐⭐⭐⭐ | 生产环境、快速部署 | 低 | 高 |
| 本地安装 | ⭐⭐⭐⭐ | 开发环境、个人使用 | 中 | 中 |
| uv 包管理器 | ⭐⭐⭐⭐ | 开发环境、快速迭代 | 低 | 高 |
| 云平台 | ⭐⭐⭐⭐⭐ | 多用户、高可用 | 高 | 高 |

## 🐳 方式 1：Docker 部署（推荐）

### 优点
- 环境隔离，避免依赖冲突
- 跨平台支持（Linux/Mac/Windows）
- 易于维护和升级
- 快速部署

### 快速开始

```bash
# 使用 Docker Compose（最简单）
docker-compose up -d

# 访问服务
curl http://localhost:5000/health
```

### 详细文档
参见 [DOCKER.md](./DOCKER.md)

## 💻 方式 2：本地安装

### 优点
- 完全控制环境
- 适合开发和调试
- 无需额外的容器运行时

### 快速开始

#### Linux/Mac

```bash
# 方式 1：使用快速开始脚本
./quickstart.sh

# 方式 2：使用安装脚本
./install.sh

# 方式 3：手动安装
pip install -r requirements_core.txt
python src/main.py -m http -p 5000
```

#### Windows

```bash
# 方式 1：使用快速开始脚本
quickstart.bat

# 方式 2：使用安装脚本
install.bat

# 方式 3：手动安装
pip install -r requirements_core.txt
python src\main.py -m http -p 5000
```

### 详细文档
参见 [INSTALL.md](./INSTALL.md)

## ⚡ 方式 3：使用 uv 包管理器（最快）

### 优点
- 最快的依赖安装速度
- 自动处理依赖冲突
- 更好的锁文件支持

### 快速开始

```bash
# 安装 uv
pip install uv

# 安装依赖
uv sync

# 启动服务
uv run python src/main.py -m http -p 5000
```

## ☁️ 方式 4：云平台部署

### 推荐平台

#### 1. Railway

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录
railway login

# 初始化项目
railway init

# 部署
railway up
```

#### 2. Render

创建 `render.yaml`:

```yaml
services:
  - type: web
    name: knowledge-base
    env: python
    buildCommand: pip install -r requirements_core.txt
    startCommand: python src/main.py -m http -p 5000
    envVars:
      - key: PORT
        value: 5000
```

#### 3. Vercel

```bash
# 安装 Vercel CLI
npm install -g vercel

# 部署
vercel
```

#### 4. AWS / GCP / Azure

使用相应的云服务：
- AWS: Elastic Beanstalk, ECS, EKS
- GCP: App Engine, Cloud Run
- Azure: App Service, Container Instances

### 详细文档
各平台的具体配置请参考官方文档。

## 📊 部署对比

### 资源需求

| 部署方式 | CPU | 内存 | 磁盘 | 网络 |
|---------|-----|------|------|------|
| Docker | 1核+ | 512MB+ | 1GB+ | 标准 |
| 本地安装 | 取决于配置 | 取决于配置 | 1GB+ | 不适用 |
| uv | 1核+ | 256MB+ | 500MB+ | 不适用 |
| 云平台 | 1核+ | 512MB+ | 1GB+ | 标准 |

### 启动时间

| 部署方式 | 首次启动 | 后续启动 |
|---------|---------|---------|
| Docker | ~30s | ~5s |
| 本地安装 | ~5s | ~3s |
| uv | ~10s | ~2s |
| 云平台 | ~1-2min | ~30s |

## 🔧 配置管理

### 环境变量

创建 `.env` 文件:

```bash
# LLM 配置
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.example.com/v1

# 服务配置
LOG_LEVEL=INFO
MAX_WORKERS=4
PORT=5000

# 存储配置
STORAGE_TYPE=local
STORAGE_PATH=assets/knowledge_base

# 可选：数据库配置
DATABASE_URL=postgresql://user:pass@localhost:5432/knowledge_base
```

### 配置文件

系统配置文件位于 `config/` 目录：

```
config/
├── summary_llm_cfg.json
├── concept_extract_llm_cfg.json
├── qa_llm_cfg.json
└── health_check_llm_cfg.json
```

## 🏥 健康检查

### 服务健康检查

```bash
# HTTP 端点
curl http://localhost:5000/health

# 响应示例
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-12-01T10:00:00Z"
}
```

### 依赖健康检查

```bash
# Python 依赖
python -c "import langchain, langgraph, fastapi, pydantic"

# 数据库连接
python -c "import sqlalchemy; engine = sqlalchemy.create_engine('your-database-url'); engine.connect()"
```

## 📈 监控和日志

### 日志位置

- 应用日志：`/app/work/logs/bypass/app.log`
- 错误日志：`/app/work/logs/bypass/error.log`
- 访问日志：`/app/work/logs/bypass/access.log`

### 监控工具

- **Prometheus + Grafana**: 系统监控
- **ELK Stack**: 日志分析
- **Sentry**: 错误追踪

## 🔄 更新和升级

### 更新依赖

```bash
# 使用 pip
pip install --upgrade -r requirements_core.txt

# 使用 uv
uv lock --upgrade
uv sync
```

### 更新代码

```bash
# 拉取最新代码
git pull origin main

# 重新安装依赖
pip install -r requirements_core.txt

# 重启服务
docker-compose restart
```

## 🔒 安全建议

### 生产环境

1. **使用 HTTPS**: 配置 SSL/TLS 证书
2. **环境变量保护**: 使用安全的密钥管理服务
3. **访问控制**: 实现身份验证和授权
4. **定期更新**: 及时更新依赖和安全补丁
5. **备份策略**: 定期备份数据

### 配置示例

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🆘 故障排查

### 常见问题

#### 1. 端口被占用

```bash
# 检查端口占用
lsof -i :5000

# 使用其他端口
python src/main.py -m http -p 5001
```

#### 2. 依赖安装失败

```bash
# 使用国内镜像
pip install -r requirements_core.txt -i https://mirrors.aliyun.com/pypi/simple/

# 使用 uv
pip install uv
uv sync
```

#### 3. 权限问题

```bash
# Linux/Mac
chmod +x scripts/*.sh
chmod -R 755 assets

# Windows
# 以管理员身份运行命令提示符
```

#### 4. 内存不足

```bash
# 增加内存限制
export MAX_WORKERS=2
export MEMORY_LIMIT=1G
```

## 📞 获取帮助

- **文档**: [INSTALL.md](./INSTALL.md), [DOCKER.md](./DOCKER.md), [USAGE.md](./USAGE.md)
- **GitHub Issues**: 提交问题到仓库
- **日志**: 查看 `/app/work/logs/bypass/app.log`

---

**推荐部署方式**: Docker（生产环境）或 本地安装（开发环境）

**快速开始**: 运行 `./quickstart.sh`（Linux/Mac）或 `quickstart.bat`（Windows）
