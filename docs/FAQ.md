# 📚 常见问题 FAQ (Frequently Asked Questions)

本文档汇总了知识库编译系统的常见问题和解决方案。

## 目录

1. [安装与部署](#安装与部署)
2. [运行与使用](#运行与使用)
3. [CORS 跨域问题](#cors-跨域问题)
4. [LLM 配置](#llm-配置)
5. [性能与优化](#性能与优化)
6. [故障排查](#故障排查)

---

## 安装与部署

### Q1: 安装依赖时报错 `Failed to build pygobject`

**A**: 这是因为 `pygobject` 需要系统的 C 编译环境。解决方案：

```bash
# 使用核心依赖（推荐）
pip install -r requirements_core.txt

# 或使用安装脚本
./install.sh  # Linux/Mac
install.bat  # Windows
```

**详细文档**: [INSTALL.md](./INSTALL.md)

### Q2: Docker 容器无法启动

**A**: 检查以下几点：

```bash
# 1. 检查 Docker 是否运行
docker ps

# 2. 查看容器日志
docker-compose logs -f knowledge-base

# 3. 检查端口占用
lsof -i :5000

# 4. 重新构建镜像
docker-compose build --no-cache
docker-compose up -d
```

**详细文档**: [DOCKER.md](./DOCKER.md)

### Q3: Windows 环境安装失败

**A**: Windows 环境下建议使用以下方式：

```bash
# 方式 1: 使用安装脚本
install.bat

# 方式 2: 使用核心依赖
pip install -r requirements_core.txt

# 方式 3: 使用 uv
pip install uv
uv sync
```

### Q4: 权限不足错误

**A**: Linux/Mac 环境下：

```bash
# 设置正确的权限
chmod +x install.sh
chmod +x quickstart.sh
chmod -R 755 assets

# 或使用 sudo
sudo python src/main.py -m http -p 5000
```

---

## 运行与使用

### Q5: 如何启动服务？

**A**: 三种启动方式：

```bash
# 方式 1: 使用命令行
python src/main.py -m http -p 5000

# 方式 2: 使用脚本
bash scripts/http_run.sh -m http -p 5000

# 方式 3: 使用 Docker
docker-compose up -d
```

### Q6: 如何停止服务？

**A**:

```bash
# 命令行启动的：按 Ctrl+C

# Docker 启动的：
docker-compose stop

# 或完全停止并删除
docker-compose down
```

### Q7: 如何查看日志？

**A**:

```bash
# 应用日志
tail -f logs/app.log

# 错误日志
tail -f logs/error.log

# Docker 日志
docker-compose logs -f knowledge-base
```

### Q8: 如何更换端口？

**A**:

```bash
# 命令行方式
python src/main.py -m http -p 5001

# 修改脚本中的端口
# 编辑 scripts/http_run.sh，修改 PORT=5001

# Docker 方式
# 修改 docker-compose.yml 中的端口映射
ports:
  - "5001:5000"
```

---

## CORS 跨域问题

### Q9: 浏览器报 CORS 错误

**A**: 这是最常见的问题，解决方案：

**快速修复**:
```bash
# 重启服务即可（已内置 CORS 配置）
python src/main.py -m http -p 5000
```

**验证修复**:
```bash
python test_cors.py
```

**详细文档**:
- [CORS 快速修复](./CORS_QUICK_FIX.md) - 3 步快速解决 ⭐
- [CORS 详细文档](./CORS_FIX.md) - 完整说明

### Q10: OPTIONS 请求返回 405

**A**: 这表明 CORS 中间件未正确配置。解决方案：

1. 确认 `src/main.py` 包含：
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. 重启服务

3. 清除浏览器缓存

---

## LLM 配置

### Q11: 如何配置 LLM API Key？

**A**: 创建 `.env` 文件：

```bash
# LLM 配置
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.example.com/v1

# 或使用环境变量
export OPENAI_API_KEY="your-api-key"
```

### Q12: 支持哪些 LLM？

**A**: 支持以下模型：

- 豆包 (Seed, Doubao)
- DeepSeek
- Kimi
- OpenAI GPT 系列
- 其他兼容 OpenAI API 的模型

### Q13: 请求超时怎么办？

**A**: 检查以下几点：

1. API Key 是否正确
2. API 服务是否可用
3. 网络连接是否正常
4. 查看日志：`tail -f logs/app.log`

```bash
# 增加超时时间（修改 src/main.py）
TIMEOUT_SECONDS = 900  # 15分钟
```

### Q14: 如何更换 LLM 模型？

**A**: 编辑配置文件：

```
config/
├── summary_llm_cfg.json         # 修改此文件
├── concept_extract_llm_cfg.json # 修改此文件
├── qa_llm_cfg.json              # 修改此文件
└── health_check_llm_cfg.json    # 修改此文件
```

修改 `model` 字段为你的模型 ID。

---

## 性能与优化

### Q15: 响应速度慢怎么办？

**A**: 优化建议：

1. **使用更快的模型**: 选择响应速度更快的 LLM
2. **增加并发**:
```bash
export MAX_WORKERS=4
```
3. **使用缓存**: 系统已内置提示词缓存
4. **优化网络**: 确保网络连接稳定

### Q16: 内存占用过高？

**A**:

```bash
# 减少工作进程数
export MAX_WORKERS=2

# 使用 Docker 资源限制
# 在 docker-compose.yml 中添加
deploy:
  resources:
    limits:
      memory: 1G
```

### Q17: 如何监控性能？

**A**:

```bash
# 查看系统资源
htop

# 查看服务日志
tail -f logs/app.log

# 使用 Docker Stats
docker stats knowledge-base
```

---

## 故障排查

### Q18: 服务启动失败

**A**: 检查清单：

```bash
# 1. 检查 Python 版本
python --version  # 需要 3.8+

# 2. 检查依赖
pip list | grep -E "langchain|langgraph|fastapi"

# 3. 检查端口
lsof -i :5000

# 4. 查看日志
cat logs/app.log | tail -50
```

### Q19: 请求返回 500 错误

**A**:

```bash
# 查看错误日志
tail -f logs/error.log

# 查看应用日志
tail -f logs/app.log

# 检查配置文件
cat config/*.json
```

### Q20: 数据丢失怎么办？

**A**:

```bash
# 检查备份
ls -la backup/

# 恢复备份
tar -xzf backup-20241201.tar.gz

# 从 Docker 卷恢复
docker run --rm -v knowledge-base_postgres_data:/data \
  -v $(pwd):/backup alpine \
  tar xzf /backup/postgres-backup.tar.gz -C /
```

### Q21: 如何重置系统？

**A**:

```bash
# 备份数据
tar -czf backup-reset-$(date +%Y%m%d).tar.gz assets/

# 清理数据
rm -rf assets/knowledge_base/*

# 重启服务
python src/main.py -m http -p 5000
```

---

## 获取帮助

### 文档

- [README.md](./README.md) - 项目概览
- [INSTALL.md](./INSTALL.md) - 安装指南
- [USAGE.md](./USAGE.md) - 使用指南
- [DEPLOYMENT.md](./DEPLOYMENT.md) - 部署指南
- [CORS_QUICK_FIX.md](./CORS_QUICK_FIX.md) - CORS 快速修复
- [DOCKER.md](./DOCKER.md) - Docker 部署

### 工具

- `test_cors.py` - CORS 测试工具
- `Makefile` - 命令快捷方式
- `install.sh/install.bat` - 安装脚本
- `quickstart.sh/quickstart.bat` - 快速开始

### 联系方式

- 提交 Issue: [GitHub Issues](https://github.com/your-username/knowledge-base-system/issues)
- 功能建议: [Feature Request](https://github.com/your-username/knowledge-base-system/issues/new?labels=enhancement)

---

**最后更新**: 2024-12-01
