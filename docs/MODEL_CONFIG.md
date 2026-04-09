# 🤖 模型配置指南

## 🚨 问题描述

本地运行时出现 **模型授权失败** 错误，需要配置自己的模型。

## 📋 支持的模型

系统支持以下模型：

### 1. 豆包（字节跳动）
- doubao-seed-1-8-251228
- doubao-pro-32k
- doubao-pro-128k
- 其他豆包系列模型

### 2. DeepSeek
- deepseek-chat
- deepseek-coder
- 其他 DeepSeek 模型

### 3. Kimi（月之暗面）
- moonshot-v1-8k
- moonshot-v1-32k
- moonshot-v1-128k
- 其他 Kimi 模型

### 4. OpenAI（兼容）
- gpt-4
- gpt-4-turbo
- gpt-3.5-turbo
- 其他 OpenAI 兼容模型

### 5. 自定义模型
任何兼容 OpenAI API 格式的模型服务

---

## 🔧 配置步骤

### 步骤 1: 创建环境变量文件

在项目根目录创建 `.env` 文件：

```bash
# 在项目根目录创建
touch .env
```

### 步骤 2: 配置模型参数

编辑 `.env` 文件，添加以下配置：

```bash
# ========================================
# 模型配置
# ========================================

# 模型类型：coze | openai | custom
MODEL_TYPE=coze

# 模型 ID（根据你的模型类型填写）
MODEL_ID=doubao-seed-1-8-251228

# API Key（必填）
OPENAI_API_KEY=your-api-key-here

# API Base URL（可选，默认使用模型默认地址）
OPENAI_BASE_URL=https://api.example.com/v1

# ========================================
# Coze 平台配置（如果使用 Coze 模型）
# ========================================

# Coze API Key（如果使用 Coze 平台）
COZE_API_KEY=your-coze-api-key

# Coze 工作空间 ID（如果使用 Coze 平台）
COZE_WORKSPACE_ID=your-workspace-id

# Coze Bot ID（如果使用 Coze Bot）
COZE_BOT_ID=your-bot-id

# ========================================
# 其他配置
# ========================================

# 日志级别：DEBUG | INFO | WARNING | ERROR
LOG_LEVEL=INFO

# 最大工作进程数
MAX_WORKERS=4
```

---

## 🎯 不同模型的配置方法

### 1. 使用豆包模型

**配置文件**:
```bash
MODEL_TYPE=coze
MODEL_ID=doubao-seed-1-8-251228
COZE_API_KEY=your-coze-api-key
COZE_WORKSPACE_ID=your-workspace-id
```

**修改配置文件**:
编辑 `config/*.json` 文件，将 `model` 字段改为：
```json
{
  "config": {
    "model": "doubao-seed-1-8-251228",
    ...
  }
}
```

### 2. 使用 DeepSeek 模型

**配置文件**:
```bash
MODEL_TYPE=openai
MODEL_ID=deepseek-chat
OPENAI_API_KEY=your-deepseek-api-key
OPENAI_BASE_URL=https://api.deepseek.com/v1
```

**修改配置文件**:
```json
{
  "config": {
    "model": "deepseek-chat",
    ...
  }
}
```

### 3. 使用 Kimi 模型

**配置文件**:
```bash
MODEL_TYPE=openai
MODEL_ID=moonshot-v1-8k
OPENAI_API_KEY=your-kimi-api-key
OPENAI_BASE_URL=https://api.moonshot.cn/v1
```

**修改配置文件**:
```json
{
  "config": {
    "model": "moonshot-v1-8k",
    ...
  }
}
```

### 4. 使用 OpenAI 模型

**配置文件**:
```bash
MODEL_TYPE=openai
MODEL_ID=gpt-4
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
```

**修改配置文件**:
```json
{
  "config": {
    "model": "gpt-4",
    ...
  }
}
```

### 5. 使用自定义模型（OpenAI 兼容）

**配置文件**:
```bash
MODEL_TYPE=openai
MODEL_ID=your-custom-model
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://your-api-endpoint.com/v1
```

**修改配置文件**:
```json
{
  "config": {
    "model": "your-custom-model",
    ...
  }
}
```

---

## 📝 需要修改的配置文件

系统使用 4 个配置文件，每个对应一个功能：

### 1. summary_llm_cfg.json - 摘要生成

**路径**: `config/summary_llm_cfg.json`

**修改内容**:
```json
{
  "config": {
    "model": "your-model-id",  // 修改这里
    "temperature": 0.3,
    "top_p": 0.9,
    "max_completion_tokens": 4000,
    "thinking": "disabled"
  },
  "tools": [],
  "sp": "# 角色定义\n你是知识库编译流程中的摘要生成专家...",
  "up": "请为以下文档生成结构化摘要：\n\n{{content}}"
}
```

### 2. concept_extract_llm_cfg.json - 概念抽取

**路径**: `config/concept_extract_llm_cfg.json`

**修改内容**:
```json
{
  "config": {
    "model": "your-model-id",  // 修改这里
    "temperature": 0.2,
    "top_p": 0.9,
    "max_completion_tokens": 2000,
    "thinking": "disabled"
  },
  "tools": [],
  "sp": "# 角色定义\n你是概念抽取专家...",
  "up": "从以下摘要中抽取核心概念：\n\n{{summary}}"
}
```

### 3. qa_llm_cfg.json - 问答

**路径**: `config/qa_llm_cfg.json`

**修改内容**:
```json
{
  "config": {
    "model": "your-model-id",  // 修改这里
    "temperature": 0.5,
    "top_p": 0.9,
    "max_completion_tokens": 3000,
    "thinking": "disabled"
  },
  "tools": [],
  "sp": "# 角色定义\n你是问答助手...",
  "up": "基于知识库回答以下问题：\n\n问题：{{question}}\n\n相关内容：\n{{context}}"
}
```

### 4. health_check_llm_cfg.json - 健康检查

**路径**: `config/health_check_llm_cfg.json`

**修改内容**:
```json
{
  "config": {
    "model": "your-model-id",  // 修改这里
    "temperature": 0.1,
    "top_p": 0.9,
    "max_completion_tokens": 3000,
    "thinking": "disabled"
  },
  "tools": [],
  "sp": "# 角色定义\n你是知识库健康检查专家...",
  "up": "检查以下知识库：\n\n{{knowledge_base}}"
}
```

---

## 🔄 快速替换脚本

创建一个脚本快速替换所有配置文件中的模型 ID：

```bash
#!/bin/bash
# replace_model.sh

NEW_MODEL_ID="$1"

if [ -z "$NEW_MODEL_ID" ]; then
    echo "使用方法: ./replace_model.sh <new-model-id>"
    echo "示例: ./replace_model.sh gpt-4"
    exit 1
fi

echo "替换模型 ID 为: $NEW_MODEL_ID"

# 替换所有配置文件
find config -name "*.json" -exec sed -i "s/\"model\": \"[^\"]*\"/\"model\": \"$NEW_MODEL_ID\"/g" {} \;

echo "✅ 替换完成！"
echo ""
echo "修改的文件："
find config -name "*.json"
```

**使用方法**:
```bash
chmod +x replace_model.sh
./replace_model.sh gpt-4
```

---

## 🧪 测试配置

### 1. 验证环境变量

```bash
# 检查 .env 文件是否存在
ls -la .env

# 查看环境变量（确保不会泄露敏感信息）
cat .env | grep -v "API_KEY\|SECRET\|TOKEN"
```

### 2. 测试模型连接

```bash
# 启动服务
python src/main.py -m http -p 5000

# 在另一个终端测试
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "qa",
    "question": "测试连接"
  }'
```

### 3. 查看日志

```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
tail -f logs/error.log
```

---

## ⚠️ 常见问题

### Q1: 仍然显示授权失败

**解决方案**:
1. 检查 API Key 是否正确
2. 检查 API Key 是否有足够的权限
3. 检查网络连接
4. 检查 API 服务是否可用
5. 查看日志获取详细错误信息

### Q2: 模型不存在

**解决方案**:
1. 确认模型 ID 是否正确
2. 检查模型是否在平台上可用
3. 检查 API 版本是否支持该模型

### Q3: 请求超时

**解决方案**:
1. 检查网络连接
2. 增加 `max_completion_tokens` 配置
3. 修改超时配置（在 `src/main.py` 中）：
```python
TIMEOUT_SECONDS = 1800  # 30分钟
```

### Q4: 速率限制

**解决方案**:
1. 检查 API 套餐的速率限制
2. 添加请求间隔
3. 使用更高级别的 API 套餐

---

## 🔐 安全建议

1. **不要提交敏感信息到 Git**:
   ```bash
   # 在 .gitignore 中添加
   echo ".env" >> .gitignore
   ```

2. **使用环境变量**:
   ```bash
   # 在运行时设置环境变量
   export OPENAI_API_KEY="your-api-key"
   python src/main.py -m http -p 5000
   ```

3. **使用密钥管理服务**:
   - AWS Secrets Manager
   - HashiCorp Vault
   - Azure Key Vault

---

## 📚 参考文档

- [豆包 API 文档](https://www.volcengine.com/docs/82379)
- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [Kimi API 文档](https://platform.moonshot.cn/docs)
- [OpenAI API 文档](https://platform.openai.com/docs)

---

## 🎯 快速开始模板

### DeepSeek 配置模板

创建 `.env` 文件：
```bash
MODEL_TYPE=openai
MODEL_ID=deepseek-chat
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
LOG_LEVEL=INFO
```

批量替换模型 ID：
```bash
./replace_model.sh deepseek-chat
```

启动服务：
```bash
python src/main.py -m http -p 5000
```

---

**配置完成后，重启服务即可生效！**
