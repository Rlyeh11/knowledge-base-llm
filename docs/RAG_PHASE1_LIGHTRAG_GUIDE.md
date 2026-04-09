# RAG 阶段 1 使用指南（LightRAG 版本）

## 📋 概述

本指南介绍如何使用基于 LightRAG 的 RAG 功能，快速实现智能问答。

---

## 🚀 快速开始（3 步）

### 步骤 1: 安装依赖

```bash
# 安装 LightRAG
pip install lightrag

# 或使用 uv
uv add lightrag

# 可选：安装 FAISS 加速
pip install faiss-cpu
```

### 步骤 2: 配置 LightRAG

创建配置文件 `config/lightrag_config.json`:

```json
{
  "embedding": {
    "model_name": "BAAI/bge-small-zh-v1.5",
    "device": "cpu",
    "batch_size": 32
  },
  "vector_store": {
    "type": "faiss",
    "dimension": 512,
    "metric": "cosine"
  },
  "retrieval": {
    "top_k": 10,
    "min_similarity": 0.5
  }
}
```

### 步骤 3: 启动服务

```bash
# 启动服务
make run

# 测试问答
make qa question="什么是知识库系统？"
```

完成！LightRAG 会自动：
- ✅ 下载嵌入模型（首次运行）
- ✅ 构建向量索引
- ✅ 执行语义检索
- ✅ 生成智能答案

---

## ⚙️ 配置说明

### 嵌入模型配置

```json
{
  "embedding": {
    "model_name": "BAAI/bge-small-zh-v1.5",
    "device": "cpu",
    "batch_size": 32
  }
}
```

**推荐模型**:

| 模型 | 大小 | 速度 | 准确性 | 推荐场景 |
|------|------|------|--------|---------|
| BAAI/bge-small-zh-v1.5 | 400MB | 快 | 高 | 默认推荐 |
| BAAI/bge-base-zh-v1.5 | 1.2GB | 中 | 很高 | 高精度需求 |
| BAAI/bge-large-zh-v1.5 | 3.9GB | 慢 | 极高 | 追求极致精度 |

### 向量存储配置

```json
{
  "vector_store": {
    "type": "faiss",
    "dimension": 512,
    "metric": "cosine"
  }
}
```

**存储类型**:

- `faiss`: 本地向量存储（默认，推荐）
- `chromadb`: ChromaDB 向量数据库
- `qdrant`: Qdrant 向量数据库

### 检索配置

```json
{
  "retrieval": {
    "top_k": 10,
    "min_similarity": 0.5
  }
}
```

**参数说明**:

- `top_k`: 返回的文档数量（5-20）
- `min_similarity`: 最小相似度阈值（0.3-0.7）

---

## 📖 使用示例

### 示例 1: 基本使用

```python
from src.services.rag_integration_service import RAGIntegrationService
import asyncio

# 初始化服务
rag = RAGIntegrationService()

# 摄取文档
asyncio.run(rag.ingest_document(
    doc_id="doc_1",
    content="Python 是一门编程语言，由 Guido van Rossum 创建。",
    metadata={"title": "Python介绍", "type": "tech"}
))

# 检索相关文档
results = asyncio.run(rag.retrieve("Python是什么？"))
print(f"找到 {len(results)} 个相关文档")

# 问答
answer = asyncio.run(rag.query("Python是谁创建的？"))
print(f"答案: {answer}")
```

### 示例 2: 批量摄取

```python
import asyncio
from src.services.rag_integration_service import RAGIntegrationService

# 初始化服务
rag = RAGIntegrationService()

# 准备文档
documents = [
    {"id": "doc_1", "content": "文档1的内容", "metadata": {"title": "文档1"}},
    {"id": "doc_2", "content": "文档2的内容", "metadata": {"title": "文档2"}},
    {"id": "doc_3", "content": "文档3的内容", "metadata": {"title": "文档3"}},
]

# 批量摄取
async def batch_ingest():
    tasks = [
        rag.ingest_document(
            doc_id=doc["id"],
            content=doc["content"],
            metadata=doc["metadata"]
        )
        for doc in documents
    ]
    await asyncio.gather(*tasks)

asyncio.run(batch_ingest())
print("批量摄取完成")
```

### 示例 3: 不同检索模式

```python
import asyncio
from src.services.rag_integration_service import RAGIntegrationService

rag = RAGIntegrationService()

# LightRAG 支持多种检索模式
modes = {
    "naive": "简单检索",
    "local": "本地上下文检索",
    "global": "全局知识检索",
    "hybrid": "混合检索（推荐）"
}

question = "如何使用知识库系统？"

for mode, desc in modes.items():
    answer = asyncio.run(rag.query(question, mode=mode))
    print(f"\n【{desc}】")
    print(answer)
```

### 示例 4: 通过 API 使用

```bash
# 提问
curl -X POST http://localhost:5000/api/qa \
  -H "Content-Type: application/json" \
  -d '{"question": "什么是知识库系统？"}'

# 响应示例
{
  "success": true,
  "answer": "知识库系统是一个基于LLM的个人知识管理...",
  "qa_file_path": "assets/knowledge_base/outputs/qa/qa_xxx.md",
  "qa_sources": ["doc_1", "doc_2", "doc_3"]
}
```

---

## 🔧 高级功能

### 1. 图增强检索（Graph RAG）

LightRAG 内置图数据库功能，可以构建知识图谱：

```python
# LightRAG 会自动构建知识图谱
# 包括实体、关系、属性等

# 查询时会利用图谱信息进行推理
answer = asyncio.run(rag.query("Python和Java有什么区别？", mode="hybrid"))
```

### 2. 多轮对话

```python
# LightRAG 支持多轮对话上下文
conversation_history = []

# 第一轮
answer1 = asyncio.run(rag.query("什么是Python？"))
conversation_history.append(("什么是Python？", answer1))

# 第二轮（利用上下文）
answer2 = asyncio.run(rag.query("它有哪些特点？"))
conversation_history.append(("它有哪些特点？", answer2))

# 第三轮（继续上下文）
answer3 = asyncio.run(rag.query("适合做什么？"))
conversation_history.append(("适合做什么？", answer3))
```

### 3. 自定义元数据

```python
# 摄取时添加丰富的元数据
asyncio.run(rag.ingest_document(
    doc_id="doc_tech_1",
    content="文档内容...",
    metadata={
        "title": "技术文档",
        "author": "张三",
        "date": "2025-04-09",
        "tags": ["技术", "Python", "编程"],
        "category": "教程"
    }
))

# 检索时可以利用元数据过滤
results = asyncio.run(rag.retrieve("Python教程"))
for doc in results:
    print(f"标题: {doc['metadata']['title']}")
    print(f"作者: {doc['metadata']['author']}")
    print(f"标签: {doc['metadata']['tags']}")
```

### 4. 性能监控

```python
# 获取统计信息
stats = rag.get_stats()
print(f"总文档数: {stats['total_documents']}")
print(f"嵌入模型: {stats['embedding_model']}")
print(f"向量存储: {stats['vector_store']}")

# 可以结合日志进行性能分析
import time

start = time.time()
answer = asyncio.run(rag.query("测试问题"))
elapsed = time.time() - start

print(f"响应时间: {elapsed:.2f}秒")
```

---

## 🧪 测试和验证

### 1. 功能测试

```bash
# 运行测试
python tests/test_lightrag_integration.py

# 或使用 Makefile
make test-rag
```

### 2. 性能测试

```python
import asyncio
import time
from src.services.rag_integration_service import RAGIntegrationService

rag = RAGIntegrationService()

# 测试问题
questions = [
    "什么是知识库系统？",
    "如何使用这个系统？",
    "系统支持哪些功能？",
    "知识库如何组织？"
]

# 性能测试
results = []
for question in questions:
    start = time.time()
    answer = asyncio.run(rag.query(question))
    elapsed = time.time() - start

    results.append({
        "question": question,
        "response_time": elapsed,
        "answer_length": len(answer)
    })

# 打印结果
for result in results:
    print(f"问题: {result['question']}")
    print(f"响应时间: {result['response_time']:.2f}秒")
    print(f"答案长度: {result['answer_length']}字符")
    print("-" * 50)
```

### 3. 准确性测试

```python
# 准备测试问题和预期答案
test_cases = [
    {
        "question": "什么是知识库系统？",
        "keywords": ["LLM", "知识管理", "摄取", "问答"]
    },
    {
        "question": "如何使用这个系统？",
        "keywords": ["摄取", "问答", "健康检查"]
    }
]

# 测试准确性
for test_case in test_cases:
    question = test_case["question"]
    keywords = test_case["keywords"]

    answer = asyncio.run(rag.query(question))

    # 检查关键词是否在答案中
    found_keywords = [kw for kw in keywords if kw in answer]
    accuracy = len(found_keywords) / len(keywords)

    print(f"问题: {question}")
    print(f"找到关键词: {found_keywords}")
    print(f"准确性: {accuracy:.2%}")
    print("-" * 50)
```

---

## 🐛 故障排查

### 问题 1: 模型下载失败

**症状**: 提示无法下载嵌入模型

**解决方案**:

```bash
# 1. 使用镜像源
export HF_ENDPOINT=https://hf-mirror.com

# 2. 手动下载模型
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-zh-v1.5')"

# 3. 检查网络
ping huggingface.co
```

### 问题 2: 检索结果不准确

**症状**: 返回的文档不相关

**解决方案**:

1. 调整 `top_k` 参数
2. 调整 `min_similarity` 阈值
3. 尝试不同的检索模式
4. 检查文档内容质量

### 问题 3: 响应速度慢

**症状**: 问答响应时间过长

**解决方案**:

1. 使用更小的嵌入模型
2. 减少 `top_k` 数量
3. 启用 GPU 加速
4. 使用 FAISS 索引优化

### 问题 4: 内存不足

**症状**: 提示内存溢出

**解决方案**:

```json
{
  "embedding": {
    "batch_size": 16  // 减少批处理大小
  }
}
```

---

## 📊 性能优化

### 1. 使用 GPU 加速

```json
{
  "embedding": {
    "device": "cuda"
  }
}
```

### 2. 优化批处理

```json
{
  "embedding": {
    "batch_size": 64  // 增加批处理大小
  }
}
```

### 3. 调整检索参数

```json
{
  "retrieval": {
    "top_k": 5,           // 减少返回结果
    "min_similarity": 0.6  // 提高相似度阈值
  }
}
```

---

## 🎯 最佳实践

### 1. 文档管理

- **定期备份**: 备份 `lrag_storage` 目录
- **文档分类**: 使用元数据标记文档类型
- **质量优先**: 只摄取高质量内容

### 2. 性能优化

- **合理配置**: 根据实际情况调整参数
- **监控性能**: 定期检查响应时间
- **及时清理**: 删除无用文档

### 3. 检索策略

- **默认 hybrid**: 使用混合检索模式
- **简单问题**: 使用 naive 模式
- **复杂问题**: 使用 global 模式
- **上下文相关**: 使用 local 模式

---

## 📈 迁移指南

### 从旧系统迁移

如果你之前使用的是关键词检索或自定义 RAG，可以：

1. **保留原有数据**: 旧的文档和摘要仍然有效
2. **逐步迁移**: 逐步添加文档到 LightRAG
3. **A/B 测试**: 对比新旧系统的效果

### 迁移步骤

```python
# 1. 读取旧文档
import os
from pathlib import Path

wiki_dir = Path("assets/knowledge_base/wiki/summaries")
documents = []

for md_file in wiki_dir.glob("*.md"):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
        documents.append({
            "id": md_file.stem,
            "content": content,
            "metadata": {
                "file_path": str(md_file),
                "title": md_file.stem
            }
        })

# 2. 批量摄取到 LightRAG
rag = RAGIntegrationService()

async def migrate():
    for doc in documents:
        await rag.ingest_document(
            doc_id=doc["id"],
            content=doc["content"],
            metadata=doc["metadata"]
        )
        print(f"已迁移: {doc['id']}")

asyncio.run(migrate())

print("迁移完成！")
```

---

## 🔗 相关文档

- [设计文档](RAG_PHASE1_LIGHTRAG_DESIGN.md) - 详细设计说明
- [LightRAG 官方文档](https://github.com/HKUDS/LightRAG) - 官方文档
- [API 参考](RAG_PHASE1_LIGHTRAG_API.md) - API 文档
- [故障排查](RAG_PHASE1_LIGHTRAG_TROUBLESHOOTING.md) - 详细故障排查

---

## 💡 提示和技巧

### 1. 快速验证

使用简单的测试问题验证系统是否正常：

```bash
make qa question="测试问题"
```

### 2. 查看日志

查看详细的检索和生成过程：

```bash
tail -f /app/work/logs/bypass/app.log
```

### 3. 监控性能

定期检查性能指标：

```python
stats = rag.get_stats()
print(f"文档数: {stats['total_documents']}")
```

---

**文档版本**: v1.0
**创建日期**: 2025-04-09
**状态**: ✅ 可用
**推荐**: 使用 LightRAG 快速实现 RAG 功能
