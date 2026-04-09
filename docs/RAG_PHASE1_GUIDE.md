# RAG 阶段 1 使用指南

## 📋 概述

本指南介绍如何使用 RAG 阶段 1 的功能，包括安装、配置、使用和优化。

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 RAG 相关依赖
pip install sentence-transformers faiss-cpu numpy

# 或使用 uv
uv add sentence-transformers faiss-cpu numpy
```

### 2. 下载模型

**方式 1: 自动下载**（首次运行时自动）

系统会在首次使用时自动下载嵌入模型。

**方式 2: 手动下载**（推荐用于离线环境）

```bash
# 下载模型到本地目录
python scripts/download_embedding_model.py
```

### 3. 构建向量索引

```bash
# 方式 1: 使用 Makefile
make build-index

# 方式 2: 使用脚本
python scripts/build_vector_index.py

# 方式 3: 代码方式
from src.scripts.build_index import build_vector_index
build_vector_index()
```

### 4. 启动服务

```bash
# 启动 HTTP 服务
make run

# 或
python src/main.py -m http -p 5000
```

### 5. 测试问答

```bash
# 测试问答
make qa question="什么是知识库系统？"

# 或使用 API
curl -X POST http://localhost:5000/api/qa \
  -H "Content-Type: application/json" \
  -d '{"question": "什么是知识库系统？"}'
```

---

## ⚙️ 配置说明

### 嵌入配置

文件: `config/embedding_config.json`

```json
{
  "model_name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
  "device": "cpu",
  "batch_size": 32,
  "normalize_embeddings": true,
  "cache_embeddings": false,
  "cache_dir": "assets/knowledge_base/embeddings/.cache",
  "max_sequence_length": 512
}
```

**参数说明**:

| 参数 | 说明 | 可选值 | 默认值 |
|------|------|--------|--------|
| `model_name` | 嵌入模型名称 | 支持的 HuggingFace 模型 | paraphrase-multilingual-MiniLM-L12-v2 |
| `device` | 运行设备 | cpu, cuda | cpu |
| `batch_size` | 批处理大小 | 正整数 | 32 |
| `normalize_embeddings` | 是否归一化 | true, false | true |
| `cache_embeddings` | 是否缓存嵌入 | true, false | false |
| `cache_dir` | 缓存目录 | 路径 | embeddings/.cache |
| `max_sequence_length` | 最大序列长度 | 正整数 | 512 |

**模型选择建议**:

| 模型 | 大小 | 速度 | 准确性 | 推荐场景 |
|------|------|------|--------|---------|
| paraphrase-multilingual-MiniLM-L12-v2 | 120MB | 快 | 高 | 默认推荐 |
| BAAI/bge-small-zh-v1.5 | 400MB | 中 | 很高 | 中文场景 |
| BAAI/bge-base-zh-v1.5 | 1.2GB | 慢 | 极高 | 高精度需求 |

### 检索配置

文件: `config/retrieval_config.json`

```json
{
  "top_k": 10,
  "max_content_length": 5000,
  "min_similarity_threshold": 0.5,
  "enable_reranking": false,
  "reranker_model": null,
  "use_hybrid_search": false,
  "hybrid_weights": {
    "dense": 0.7,
    "sparse": 0.3
  }
}
```

**参数说明**:

| 参数 | 说明 | 可选值 | 默认值 |
|------|------|--------|--------|
| `top_k` | 返回结果数量 | 正整数 | 10 |
| `max_content_length` | 最大内容长度 | 正整数 | 5000 |
| `min_similarity_threshold` | 最小相似度阈值 | 0.0-1.0 | 0.5 |
| `enable_reranking` | 是否启用重排序 | true, false | false |
| `use_hybrid_search` | 是否启用混合检索 | true, false | false |

---

## 📖 使用场景

### 场景 1: 首次使用

**步骤**:

1. 摄取一些文档

```bash
make ingest content="# Python 教程\n\nPython 是一门编程语言..." title="Python教程"
```

2. 构建向量索引

```bash
make build-index
```

3. 提问

```bash
make qa question="什么是Python？"
```

### 场景 2: 添加新文档后更新索引

**步骤**:

1. 摄取新文档

```bash
make ingest content="# 新文档\n\n这是新的内容..." title="新文档"
```

2. 更新索引

```bash
make update-index

# 或完全重建
make rebuild-index
```

3. 测试问答

```bash
make qa question="新文档的内容是什么？"
```

### 场景 3: 批量摄取文档

**步骤**:

1. 批量摄取文档

```bash
python scripts/batch_ingest.py --dir ./documents
```

2. 构建索引

```bash
make build-index
```

3. 测试性能

```bash
make test-qa
```

---

## 🔧 高级功能

### 1. 自定义嵌入模型

```python
from src.services.embedding_service import EmbeddingService

# 使用自定义模型
embedder = EmbeddingService(
    model_name="BAAI/bge-small-zh-v1.5",
    device="cpu"
)

# 生成嵌入
embedding = embedder.embed_text("测试文本")
```

### 2. 程序化索引管理

```python
from src.services.vector_index_service import VectorIndexService
from src.services.embedding_service import EmbeddingService

# 初始化
embedder = EmbeddingService()
index_service = VectorIndexService(
    index_path="assets/knowledge_base/embeddings/summaries/index.faiss",
    embedding_dim=embedder.get_embedding_dimension()
)

# 添加单个文档
embedding = embedder.embed_text("文档内容")
index_service.add_document(
    doc_id="custom_doc_1",
    embedding=embedding,
    metadata={
        "title": "自定义文档",
        "file_path": "custom/path.md"
    }
)

# 保存
index_service.save_index()
```

### 3. 自定义检索

```python
from src.services.retrieval_service import RetrievalService

# 初始化检索服务
retrieval = RetrievalService(
    embedding_service=embedder,
    vector_index_service=index_service,
    top_k=5  # 自定义返回数量
)

# 检索
results = retrieval.retrieve("查询问题")

# 查看结果
for result in results:
    print(f"文档: {result['metadata']['title']}")
    print(f"相似度: {result['score']}")
    print(f"内容: {result['content'][:100]}...")
    print("-" * 50)
```

### 4. 索引统计和监控

```python
from src.services.retrieval_service import RetrievalService

# 获取统计信息
stats = retrieval.get_index_stats()
print(f"总文档数: {stats['total_documents']}")
print(f"索引类型: {stats['index_type']}")
print(f"向量维度: {stats['embedding_dim']}")
```

---

## 🧪 测试和验证

### 1. 测试嵌入服务

```bash
python tests/test_embedding_service.py
```

### 2. 测试索引服务

```bash
python tests/test_vector_index_service.py
```

### 3. 测试检索服务

```bash
python tests/test_retrieval_service.py
```

### 4. 测试完整流程

```bash
python tests/test_rag_integration.py
```

### 5. 性能测试

```bash
python tests/test_rag_performance.py
```

---

## 📊 性能优化

### 1. 索引优化

**使用 IVF 索引（大规模场景）**:

```python
# 创建索引时使用 IVF
index_service.create_index(index_type="ivf")
```

**调整 nlist 参数**:

```python
# nlist = sqrt(total_documents) 效果较好
nlist = int(np.sqrt(total_documents))
```

### 2. 嵌入优化

**使用 GPU 加速**:

```json
{
  "device": "cuda"
}
```

**批量处理**:

```python
# 批量生成嵌入
embeddings = embedder.embed_batch(texts)
```

**启用缓存**:

```json
{
  "cache_embeddings": true
}
```

### 3. 检索优化

**调整 top_k**:

```json
{
  "top_k": 5
}
```

**设置相似度阈值**:

```json
{
  "min_similarity_threshold": 0.7
}
```

---

## 🐛 故障排查

### 问题 1: 模型下载失败

**症状**: 提示无法下载模型

**解决方案**:

```bash
# 1. 检查网络连接
ping huggingface.co

# 2. 使用镜像源
export HF_ENDPOINT=https://hf-mirror.com

# 3. 手动下载
python scripts/download_embedding_model.py
```

### 问题 2: 索引构建失败

**症状**: 提示索引构建错误

**解决方案**:

```bash
# 1. 检查文档目录
ls assets/knowledge_base/wiki/summaries

# 2. 删除旧索引重建
rm -rf assets/knowledge_base/embeddings/summaries/*
make rebuild-index

# 3. 检查日志
tail -f /app/work/logs/bypass/app.log
```

### 问题 3: 检索结果不准确

**症状**: 返回的文档不相关

**解决方案**:

1. 检查相似度阈值
2. 尝试更大的 top_k
3. 考虑更换嵌入模型
4. 检查文档内容质量

### 问题 4: 内存不足

**症状**: 提示内存溢出

**解决方案**:

```json
{
  "batch_size": 16,  // 减小批处理大小
  "cache_embeddings": false  // 禁用缓存
}
```

或使用更大的模型：

```json
{
  "model_name": "sentence-transformers/all-MiniLM-L6-v2"  // 更小的模型
}
```

---

## 📚 API 参考

### EmbeddingService

```python
class EmbeddingService:
    def __init__(self, model_name: str = None, device: str = "cpu")
    def load_model()
    def embed_text(text: str) -> np.ndarray
    def embed_batch(texts: List[str]) -> np.ndarray
    def get_embedding_dimension() -> int
    def unload_model()
```

### VectorIndexService

```python
class VectorIndexService:
    def __init__(self, index_path: str, embedding_dim: int)
    def create_index(index_type: str = "flat")
    def add_document(doc_id: str, embedding: np.ndarray, metadata: dict)
    def search(query_embedding: np.ndarray, top_k: int = 10) -> List[dict]
    def save_index(path: str = None)
    def load_index(path: str = None)
    def get_document_count() -> int
    def rebuild_from_documents(documents: List[dict], embedding_service: EmbeddingService)
    def delete_index()
```

### RetrievalService

```python
class RetrievalService:
    def __init__(self, embedding_service: EmbeddingService, vector_index_service: VectorIndexService, top_k: int = 10)
    def retrieve(query: str, top_k: int = None) -> List[dict]
    def retrieve_with_content(query: str, top_k: int = None, max_content_length: int = 5000) -> List[dict]
    def get_index_stats() -> dict
```

---

## 🎯 最佳实践

### 1. 索引管理

- **定期重建索引**: 每次大量更新后重建
- **备份索引**: 重要索引定期备份
- **监控索引大小**: 避免索引过大

### 2. 检索优化

- **合理设置 top_k**: 根据需求调整
- **使用相似度阈值**: 过滤低质量结果
- **监控检索性能**: 定期检查响应时间

### 3. 模型选择

- **默认推荐**: paraphrase-multilingual-MiniLM-L12-v2
- **中文优化**: BAAI/bge-small-zh-v1.5
- **高精度**: BAAI/bge-base-zh-v1.5

### 4. 性能监控

- **记录日志**: 记录关键指标
- **定期测试**: 运行性能测试
- **及时优化**: 根据监控数据优化

---

## 📈 升级到阶段 2

当需要以下功能时，考虑升级到阶段 2：

- ✅ 支持增量更新（无需重建索引）
- ✅ 持久化存储（数据不丢失）
- ✅ 混合检索（Dense + Sparse）
- ✅ 重排序（提升精度）

查看 [阶段 2 实施方案](RAG_PHASE2_DESIGN.md) 了解详情。

---

## 🔗 相关文档

- [设计文档](RAG_PHASE1_DESIGN.md) - 详细设计说明
- [总体方案](RAG_PHASE1_OVERVIEW.md) - RAG 总体方案
- [API 文档](RAG_PHASE1_API.md) - 完整 API 参考
- [故障排查](RAG_PHASE1_TROUBLESHOOTING.md) - 详细故障排查

---

**文档版本**: v1.0
**创建日期**: 2025-04-09
**状态**: ✅ 可用
**更新**: 根据用户反馈持续更新
