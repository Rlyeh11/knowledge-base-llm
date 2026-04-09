# 环境变量配置快速开始

本文档介绍如何快速配置知识库编译系统的环境变量。

## 🚀 快速配置（3 步完成）

### 步骤 1: 复制环境变量模板

```bash
cp .env.example .env
```

### 步骤 2: 编辑 .env 文件

```bash
nano .env  # 或使用你喜欢的编辑器
```

**必需配置**（至少填写以下内容）:

```bash
# 模型类型 (openai | coze)
MODEL_TYPE=openai

# 模型 ID
MODEL_ID=deepseek-chat

# OpenAI API Key (MODEL_TYPE=openai 时必填)
OPENAI_API_KEY=sk-your-real-api-key-here
```

### 步骤 3: 验证配置

```bash
make env-check
```

或

```bash
python tests/test_env.py
```

## 🔧 使用配置脚本

### Linux/Mac 用户

```bash
./scripts/setup_env.sh
```

脚本会:
1. 检查是否已有 `.env` 文件
2. 复制 `.env.example` 到 `.env`
3. 引导您输入 API Key
4. 选择默认模型
5. 验证配置

### Windows 用户

```cmd
scripts\setup_env.bat
```

## 📋 模型配置

### 配置 DeepSeek（推荐）

```bash
make model-deepseek
```

然后输入您的 DeepSeek API Key。

### 配置 Kimi

```bash
make model-kimi
```

然后输入您的 Kimi API Key。

### 配置 OpenAI

```bash
make model-openai model=gpt-4
```

然后输入您的 OpenAI API Key。

### 快速配置（DeepSeek 默认）

```bash
make model-setup
```

## 🧪 测试配置

### 检查环境变量

```bash
make env-check
```

### 测试模型连接

```bash
make model-test
```

## 📚 详细配置说明

### 主要环境变量

| 变量名 | 必填 | 说明 | 示例值 |
|--------|------|------|--------|
| `MODEL_TYPE` | 是 | 模型类型 | `openai`, `coze` |
| `MODEL_ID` | 是 | 模型 ID | `deepseek-chat`, `gpt-4` |
| `OPENAI_API_KEY` | MODEL_TYPE=openai 时必填 | OpenAI API Key | `sk-xxxx` |
| `OPENAI_BASE_URL` | 否 | API Base URL | `https://api.deepseek.com/v1` |
| `COZE_API_KEY` | MODEL_TYPE=coze 时必填 | Coze API Key | `pat-xxxx` |

### 可选配置

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `LOG_LEVEL` | `INFO` | 日志级别: DEBUG, INFO, WARNING, ERROR |
| `MAX_WORKERS` | `4` | 最大工作进程数 |
| `PORT` | `5000` | 服务端口 |
| `STORAGE_TYPE` | `local` | 存储类型: local, s3, oss |
| `STORAGE_PATH` | `assets/knowledge_base` | 本地存储路径 |

## 🔐 安全建议

1. **不要提交 .env 文件到 Git**
   - `.env` 已添加到 `.gitignore`
   - 仅提交 `.env.example` 作为模板

2. **使用不同的 API Key**
   - 开发环境: 使用限制额度的 Key
   - 生产环境: 使用专用 Key

3. **定期轮换 API Key**
   - 定期更换 API Key
   - 使用 Key 管理服务

## 🐛 常见问题

### Q: 环境变量不生效？

**A**: 检查以下几点:
1. 确认已创建 `.env` 文件
2. 确认 `.env` 文件在项目根目录
3. 运行 `make env-check` 验证配置

### Q: 模型测试失败？

**A**: 检查以下几点:
1. API Key 是否正确
2. API Base URL 是否正确
3. 网络连接是否正常
4. 模型 ID 是否支持

### Q: 如何切换模型？

**A**: 两种方式:
1. 直接编辑 `.env` 文件，修改 `MODEL_TYPE` 和 `MODEL_ID`
2. 使用配置脚本: `make model-deepseek` 或 `make model-kimi`

## 📖 更多文档

- [完整环境变量列表](../.env.example)
- [模型配置指南](MODEL_CONFIG.md)
- [部署指南](DEPLOYMENT.md)
- [故障排查](TROUBLESHOOTING.md)
