# 📚 知识库编译系统

基于 LLM 的个人知识库管理系统，实现资料的摄取、编译、问答和健康检查。

## ✨ 核心特性

- **📥 智能摄取**: 支持 Markdown、HTML、纯文本内容的自动摄取
- **🤖 自动编译**: LLM 自动生成摘要、抽取核心概念
- **🔗 智能链接**: 统一使用 Markdown 链接格式，可点击跳转
- **❓ 智能问答**: 基于知识库内容回答问题，保留来源引用
- **🏥 健康检查**: 自动检测概念冲突、完整性问题、孤岛文件
- **📊 可视化**: 提供友好的 Web 界面和命令行工具

## 🚀 快速开始

### 1. 启动服务

```bash
# 方式一：使用启动脚本
./start.sh

# 方式二：直接运行
python src/main.py -m http -p 5000
```

服务将在 `http://localhost:5000` 启动。

### 2. 使用命令行客户端

```bash
# 摄取内容
python client.py ingest "你的内容" --title "标题"

# 提问
python client.py ask "你的问题"

# 健康检查
python client.py health --mode full
```

### 3. 使用 Web 界面

在浏览器中打开 `index.html` 文件，即可使用可视化界面。

### 4. 使用 API

```python
import requests

# 摄取内容
response = requests.post(
    "http://localhost:5000/run",
    json={
        "content": "你的内容...",
        "content_type": "markdown",
        "mode": "ingest"
    }
)

# 问答
response = requests.post(
    "http://localhost:5000/run",
    json={
        "question": "你的问题",
        "mode": "qa"
    }
)
```

## 📖 详细文档

- **[使用指南](./USAGE.md)**: 完整的 API 文档和使用示例
- **[项目架构](./AGENTS.md)**: 工作流架构和节点说明

## 🏗️ 项目结构

```
.
├── assets/knowledge_base/   # 知识库数据
│   ├── raw/articles/        # 原始内容
│   ├── wiki/                # 编译产物
│   │   ├── indexes/         # 索引文件
│   │   ├── summaries/       # 摘要
│   │   └── concepts/        # 概念条目
│   └── outputs/             # 输出文件
│       ├── qa/              # 问答记录
│       └── health/          # 健康检查报告
├── config/                  # LLM 配置文件
├── src/                     # 源代码
│   ├── graphs/              # 工作流定义
│   │   ├── graph.py         # 主工作流
│   │   ├── state.py         # 状态定义
│   │   └── nodes/           # 节点实现
│   └── main.py              # 服务入口
├── client.py                # 命令行客户端
├── start.sh                 # 启动脚本
├── index.html               # Web 界面
└── USAGE.md                 # 使用指南
```

## 🎯 工作流模式

### 1. 摄取模式

```json
{
  "content": "你的内容...",
  "content_type": "markdown",
  "title": "文档标题",
  "mode": "ingest"
}
```

**流程**: 摄取内容 → 生成摘要 → 抽取概念 → 更新索引

### 2. 问答模式

```json
{
  "question": "你的问题",
  "mode": "qa"
}
```

**流程**: 检索知识库 → 生成答案 → 保存问答记录

### 3. 健康检查模式

```json
{
  "mode": "health_check",
  "health_check_mode": "full"
}
```

**流程**: 扫描概念文件 → 检查一致性/完整性/孤岛 → 生成报告

## 🔧 技术栈

- **框架**: LangGraph + FastAPI
- **LLM**: 支持多种大语言模型（豆包、DeepSeek、Kimi等）
- **存储**: 本地文件系统
- **前端**: 纯 HTML + JavaScript

## 📊 API 端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/run` | POST | 执行工作流 |
| `/stream_run` | POST | 流式执行 |
| `/cancel/{run_id}` | POST | 取消执行 |
| `/node_run/{node_id}` | POST | 执行单个节点 |
| `/v1/chat/completions` | POST | OpenAI 兼容接口 |
| `/health` | GET | 健康检查 |
| `/graph_parameter` | GET | 获取参数定义 |

## 🔍 使用示例

### 摄取技术文档

```python
import requests

response = requests.post(
    "http://localhost:5000/run",
    json={
        "content": """
# Python 最佳实践

## 代码风格
- 使用 PEP 8 规范
- 编写清晰的注释

## 性能优化
- 避免不必要的循环
- 使用列表推导式
        """,
        "content_type": "markdown",
        "title": "Python 最佳实践",
        "mode": "ingest"
    }
)

print(f"✅ 摄取成功！文件: {response.json()['raw_file_path']}")
```

### 智能问答

```python
import requests

response = requests.post(
    "http://localhost:5000/run",
    json={
        "question": "如何提高 Python 代码性能？",
        "mode": "qa"
    }
)

print(f"💡 答案: {response.json()['answer']}")
```

## ⚠️ 注意事项

1. **端口占用**: 默认使用 5000 端口，如被占用会自动尝试 8000
2. **文件权限**: 确保 `assets` 目录有写权限
3. **超时设置**: 默认超时 15 分钟，可在 `src/main.py` 中修改
4. **数据持久化**: 所有数据保存在本地，注意备份

## 🚨 故障排查

### 服务无法启动

```bash
# 检查端口占用
lsof -i :5000

# 使用其他端口
python src/main.py -m http -p 8000
```

### API 调用失败

```bash
# 检查服务状态
curl http://localhost:5000/health

# 查看服务日志
tail -f /app/work/logs/bypass/app.log
```

## 📝 开发指南

### 添加新的节点

1. 在 `src/graphs/nodes/` 中创建节点文件
2. 在 `src/graphs/state.py` 中定义输入输出
3. 在 `src/graphs/graph.py` 中添加节点到工作流
4. 更新 `AGENTS.md` 文档

### 修改 LLM 配置

编辑 `config/` 目录下的 JSON 配置文件：
- `summary_llm_cfg.json`: 摘要生成配置
- `concept_extract_llm_cfg.json`: 概念抽取配置
- `qa_llm_cfg.json`: 问答配置
- `health_check_llm_cfg.json`: 健康检查配置

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

本项目基于 Karpathy 的 "LLM Knowledge Bases" 方法论开发。
