# 🚀 模型配置快速开始

## 🎯 快速解决模型授权失败

### 问题描述
本地运行时出现 **模型授权失败** 错误。

### 3 步快速修复

#### 步骤 1: 运行配置脚本

**Linux/Mac:**
```bash
# 使用 DeepSeek 模型（推荐）
chmod +x scripts/configure_model.sh
./scripts/configure_model.sh deepseek

# 或使用其他模型
./scripts/configure_model.sh openai gpt-4
./scripts/configure_model.sh kimi
./scripts/configure_model.sh coze
```

**Windows:**
```cmd
scripts\configure_model.bat deepseek

# 或使用其他模型
scripts\configure_model.bat openai gpt-4
scripts\configure_model.bat kimi
scripts\configure_model.bat coze
```

#### 步骤 2: 测试配置

**Linux/Mac:**
```bash
python tools/test_model_config.py
```

**Windows:**
```cmd
tools\test_model_config.bat
```

预期输出：
```
🎉 所有测试通过！模型配置正确。
```

#### 步骤 3: 重启服务

```bash
python src/main.py -m http -p 5000
```

---

## 📋 支持的模型

### DeepSeek（推荐 ⭐）
- **免费额度**: 新用户有免费额度
- **性价比高**: 价格便宜，性能优秀
- **配置方式**:
  ```bash
  ./configure_model.sh deepseek
  ```
- **API Key**: [获取地址](https://platform.deepseek.com/api-keys)
- **文档**: [DeepSeek API](https://platform.deepseek.com/api-docs/)

### Kimi（月之暗面）
- **免费额度**: 新用户有免费额度
- **中文优化**: 适合中文场景
- **配置方式**:
  ```bash
  ./configure_model.sh kimi
  ```
- **API Key**: [获取地址](https://platform.moonshot.cn/console/api-keys)
- **文档**: [Kimi API](https://platform.moonshot.cn/docs)

### OpenAI
- **全球领先**: 最强大的模型
- **需要付费**: 按使用量计费
- **配置方式**:
  ```bash
  ./configure_model.sh openai gpt-4
  ```
- **API Key**: [获取地址](https://platform.openai.com/api-keys)
- **文档**: [OpenAI API](https://platform.openai.com/docs)

### 豆包（Coze）
- **字节跳动**: 国产优秀模型
- **中文优化**: 适合中文场景
- **配置方式**:
  ```bash
  ./configure_model.sh coze
  ```
- **API Key**: [获取地址](https://www.coze.cn/open)

---

## 🔧 手动配置（可选）

如果配置脚本不适用，可以手动配置：

### 1. 创建 .env 文件

```bash
# 创建 .env 文件
cat > .env << EOF
MODEL_TYPE=openai
MODEL_ID=deepseek-chat
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.deepseek.com/v1
LOG_LEVEL=INFO
EOF
```

### 2. 更新配置文件

编辑以下文件中的 `model` 字段：
- `config/summary_llm_cfg.json`
- `config/concept_extract_llm_cfg.json`
- `config/qa_llm_cfg.json`
- `config/health_check_llm_cfg.json`

将 `model` 字段改为你的模型 ID，例如：
```json
{
  "config": {
    "model": "deepseek-chat",
    ...
  }
}
```

### 3. 测试配置

```bash
python test_model_config.py
```

---

## ⚠️ 常见问题

### Q1: 配置后仍然报授权失败

**解决方案**:
1. 检查 API Key 是否正确
2. 检查 API Key 是否有足够的权限
3. 检查网络连接
4. 查看日志：`tail -f logs/app.log`

### Q2: 不想配置脚本，只想快速测试

**解决方案**:
使用环境变量方式：
```bash
# 临时设置环境变量
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://api.deepseek.com/v1"

# 启动服务
python src/main.py -m http -p 5000
```

### Q3: 如何更换模型？

**解决方案**:
1. 重新运行配置脚本：
   ```bash
   ./configure_model.sh new-model-type
   ```
2. 或手动编辑 `.env` 文件和配置文件
3. 重启服务

### Q4: API Key 泄露怎么办？

**解决方案**:
1. 立即在 API 平台撤销旧的 API Key
2. 生成新的 API Key
3. 更新 `.env` 文件
4. 确保 `.env` 在 `.gitignore` 中

---

## 🔐 安全提示

### 1. 不要提交 .env 文件到 Git

```bash
# 检查 .gitignore
cat .gitignore | grep .env

# 如果没有，添加
echo ".env" >> .gitignore
```

### 2. 保护 API Key

- 不要分享 API Key
- 定期更换 API Key
- 使用最小权限原则
- 在生产环境使用密钥管理服务

### 3. 检查已提交的敏感信息

```bash
# 检查 Git 历史中是否包含敏感信息
git log --all --full-history --source -- "*env*"

# 如果发现，使用 BFG 或 git-filter-repo 清除
```

---

## 📚 更多信息

- **详细文档**: [MODEL_CONFIG.md](./MODEL_CONFIG.md)
- **常见问题**: [FAQ.md](./FAQ.md)
- **API 文档**:
  - [DeepSeek](https://platform.deepseek.com/api-docs/)
  - [Kimi](https://platform.moonshot.cn/docs)
  - [OpenAI](https://platform.openai.com/docs)

---

## 🎉 完成

配置完成后，你应该可以正常使用系统了！

**测试命令**:
```bash
# 测试问答功能
python tools/client.py qa "测试问题"

# 测试摄取功能
python tools/client.py ingest "# 测试文档\n\n这是测试内容" --title "测试"

# 查看日志
tail -f logs/app.log
```

---

**推荐模型**: DeepSeek（免费额度、性价比高）⭐

**快速开始**:
```bash
./scripts/configure_model.sh deepseek
python tools/test_model_config.py
python src/main.py -m http -p 5000
```
