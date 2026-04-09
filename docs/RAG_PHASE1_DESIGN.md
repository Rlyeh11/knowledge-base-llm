# 阶段 1 RAG 开发设计文档

## 📋 概述

本文档详细描述 RAG 阶段 1 的开发设计，包括架构设计、模块实现、数据结构、配置管理等。

---

## 🎯 目标

实现基础的向量检索能力，显著提升问答系统的准确性和支持规模。

### 核心目标

- ✅ 支持语义检索（向量搜索）
- ✅ 支持 1000+ 文档规模
- ✅ 提升检索准确性 5 倍
- ✅ 提升上下文利用率到 80%
- ✅ 保持响应时间在 5 秒内

---

## 🏗️ 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                  RAG 阶段 1 架构                          │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  【摄取流程】（保持不变）                                  │
│  原始内容 → 摘要生成 → 概念抽取 → 索引更新                │
│              ↓                                           │
│         【新增】文档嵌入                                   │
│              ↓                                           │
│         【新增】向量索引保存                              │
│                                                           │
│  【问答流程】（改造）                                      │
│  用户问题 → 问题嵌入 → 向量检索 → 构建上下文 → LLM        │
│              ↓                                           │
│         Top-K 相关文档                                    │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### 组件关系图

```
┌─────────────────┐
│   qa_node.py    │
│  （问答节点）     │
└────────┬────────┘
         │
         ├──────────────────┐
         │                  │
         ↓                  ↓
┌──────────────┐    ┌──────────────┐
│ RetrievalSvc │    │ EmbeddingSvc │
│  （检索服务）  │    │ （嵌入服务）  │
└──────┬───────┘    └──────┬───────┘
       │                   │
       ↓                   ↓
┌──────────────┐    ┌──────────────┐
│VectorIndexSvc│    │ Sentence-BERT│
│ （向量索引）  │    │  （嵌入模型）  │
└──────┬───────┘    └──────────────┘
       │
       ↓
┌──────────────┐
│   FAISS      │
│ （索引文件）  │
└──────────────┘
```

---

## 📁 目录结构

```
项目根目录/
├── src/
│   ├── services/              # 新增：服务层
│   │   ├── __init__.py
│   │   ├── embedding_service.py       # 嵌入服务
│   │   ├── vector_index_service.py   # 向量索引服务
│   │   └── retrieval_service.py      # 检索服务
│   ├── graphs/
│   │   ├── nodes/
│   │   │   └── qa_node.py            # 改造：集成检索
│   │   └── state.py
│   └── main.py
├── assets/knowledge_base/
│   ├── wiki/
│   │   ├── summaries/
│   │   └── concepts/
│   └── embeddings/            # 新增：向量数据目录
│       ├── summaries/         # 摘要向量索引
│       │   ├── index.faiss
│       │   ├── documents.json
│       │   └── config.json
│       └── concepts/          # 概念向量索引
│           ├── index.faiss
│           ├── documents.json
│           └── config.json
├── config/
│   ├── embedding_config.json           # 新增：嵌入配置
│   └── retrieval_config.json          # 新增：检索配置
├── docs/
│   ├── RAG_PHASE1_DESIGN.md           # 本文档
│   └── RAG_PHASE1_GUIDE.md            # 使用指南
└── tests/
    ├── test_embedding_service.py       # 新增：嵌入服务测试
    ├── test_vector_index_service.py   # 新增：索引服务测试
    └── test_retrieval_service.py      # 新增：检索服务测试
```

---

## 🔧 核心模块设计

### 1. EmbeddingService（嵌入服务）

**文件位置**: `src/services/embedding_service.py`

**功能职责**:
- 加载和管理嵌入模型
- 生成文本向量
- 批量处理文本
- 缓存嵌入结果（可选）

**类设计**:

```python
class EmbeddingService:
    """文档嵌入服务"""

    def __init__(self, model_name: str = None, device: str = "cpu"):
        """
        初始化嵌入服务

        Args:
            model_name: 模型名称，默认从配置读取
            device: 运行设备（cpu/gpu）
        """
        pass

    def load_model(self):
        """加载嵌入模型"""
        pass

    def embed_text(self, text: str) -> np.ndarray:
        """
        生成单个文本的向量

        Args:
            text: 输入文本

        Returns:
            向量数组（numpy array）
        """
        pass

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """
        批量生成文本向量

        Args:
            texts: 文本列表

        Returns:
            向量矩阵（numpy array）
        """
        pass

    def get_embedding_dimension(self) -> int:
        """获取向量维度"""
        pass

    def unload_model(self):
        """卸载模型释放内存"""
        pass
```

**配置**:

```json
{
  "model_name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
  "device": "cpu",
  "batch_size": 32,
  "normalize_embeddings": true,
  "cache_embeddings": false,
  "cache_dir": "assets/knowledge_base/embeddings/.cache"
}
```

**使用示例**:

```python
from src.services.embedding_service import EmbeddingService

# 初始化服务
embedder = EmbeddingService()

# 生成向量
embedding = embedder.embed_text("这是一段测试文本")

# 批量生成
embeddings = embedder.embed_batch([
    "文本1",
    "文本2",
    "文本3"
])
```

---

### 2. VectorIndexService（向量索引服务）

**文件位置**: `src/services/vector_index_service.py`

**功能职责**:
- 创建和管理 FAISS 索引
- 添加文档向量到索引
- 执行相似度检索
- 保存和加载索引
- 重建索引

**类设计**:

```python
class VectorIndexService:
    """向量索引管理服务"""

    def __init__(self, index_path: str, embedding_dim: int):
        """
        初始化向量索引服务

        Args:
            index_path: 索引文件路径
            embedding_dim: 向量维度
        """
        pass

    def create_index(self, index_type: str = "flat"):
        """
        创建向量索引

        Args:
            index_type: 索引类型（flat/ivf）
        """
        pass

    def add_document(
        self,
        doc_id: str,
        embedding: np.ndarray,
        metadata: dict
    ):
        """
        添加文档到索引

        Args:
            doc_id: 文档 ID
            embedding: 文档向量
            metadata: 文档元数据
        """
        pass

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 10
    ) -> List[dict]:
        """
        检索最相似的文档

        Args:
            query_embedding: 查询向量
            top_k: 返回结果数量

        Returns:
            结果列表，每个结果包含 doc_id, score, metadata
        """
        pass

    def save_index(self, path: str = None):
        """保存索引到文件"""
        pass

    def load_index(self, path: str = None):
        """从文件加载索引"""
        pass

    def get_document_count(self) -> int:
        """获取索引中的文档数量"""
        pass

    def rebuild_from_documents(
        self,
        documents: List[dict],
        embedding_service: EmbeddingService
    ):
        """
        从文档列表重建索引

        Args:
            documents: 文档列表
            embedding_service: 嵌入服务
        """
        pass

    def delete_index(self):
        """删除索引"""
        pass
```

**配置**:

```json
{
  "index_type": "flat",
  "metric": "L2",
  "nlist": 100,
  "nprobe": 10
}
```

**数据结构**:

```json
// documents.json
{
  "version": "1.0",
  "created_at": "2025-04-09T10:00:00Z",
  "embedding_dim": 384,
  "total_documents": 0,
  "documents": {
    "doc_id_1": {
      "title": "文档标题",
      "file_path": "path/to/file.md",
      "content_preview": "内容预览...",
      "created_at": "2025-04-09T10:00:00Z",
      "type": "summary"
    }
  }
}
```

**使用示例**:

```python
from src.services.vector_index_service import VectorIndexService
from src.services.embedding_service import EmbeddingService
import numpy as np

# 初始化
index_service = VectorIndexService(
    index_path="assets/knowledge_base/embeddings/summaries/index.faiss",
    embedding_dim=384
)

# 创建索引
index_service.create_index(index_type="flat")

# 添加文档
embedding = np.random.rand(384).astype('float32')
index_service.add_document(
    doc_id="doc_1",
    embedding=embedding,
    metadata={
        "title": "文档1",
        "file_path": "path/to/doc1.md"
    }
)

# 保存索引
index_service.save_index()

# 检索
query_embedding = np.random.rand(384).astype('float32')
results = index_service.search(query_embedding, top_k=5)
```

---

### 3. RetrievalService（检索服务）

**文件位置**: `src/services/retrieval_service.py`

**功能职责**:
- 整合嵌入和索引服务
- 提供统一的检索接口
- 处理检索逻辑
- 返回格式化结果

**类设计**:

```python
class RetrievalService:
    """语义检索服务"""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_index_service: VectorIndexService,
        top_k: int = 10
    ):
        """
        初始化检索服务

        Args:
            embedding_service: 嵌入服务
            vector_index_service: 向量索引服务
            top_k: 默认返回结果数量
        """
        pass

    def retrieve(self, query: str, top_k: int = None) -> List[dict]:
        """
        检索相关文档

        Args:
            query: 查询文本
            top_k: 返回结果数量

        Returns:
            检索结果列表
        """
        pass

    def retrieve_with_content(
        self,
        query: str,
        top_k: int = None,
        max_content_length: int = 5000
    ) -> List[dict]:
        """
        检索相关文档并加载内容

        Args:
            query: 查询文本
            top_k: 返回结果数量
            max_content_length: 最大内容长度

        Returns:
            包含内容的检索结果
        """
        pass

    def get_index_stats(self) -> dict:
        """获取索引统计信息"""
        pass
```

**配置**:

```json
{
  "top_k": 10,
  "max_content_length": 5000,
  "min_similarity_threshold": 0.5,
  "enable_reranking": false
}
```

**使用示例**:

```python
from src.services.retrieval_service import RetrievalService
from src.services.embedding_service import EmbeddingService
from src.services.vector_index_service import VectorIndexService

# 初始化服务
embedder = EmbeddingService()
index_service = VectorIndexService(
    index_path="assets/knowledge_base/embeddings/summaries/index.faiss",
    embedding_dim=384
)

retrieval = RetrievalService(
    embedding_service=embedder,
    vector_index_service=index_service,
    top_k=10
)

# 检索
results = retrieval.retrieve("如何使用知识库系统？")

# 带内容的检索
results_with_content = retrieval.retrieve_with_content(
    query="如何使用知识库系统？",
    top_k=5,
    max_content_length=3000
)
```

---

### 4. qa_node.py 改造

**文件位置**: `src/graphs/nodes/qa_node.py`

**改造内容**:

**原有流程**:
```python
1. 遍历所有文档（按文件顺序）
2. 读取文档内容（前2000字符）
3. 选择前5个文档
4. 构建上下文
5. 调用 LLM
```

**改造后流程**:
```python
1. 初始化检索服务
2. 问题嵌入
3. 向量检索（Top-K）
4. 读取文档内容
5. 构建上下文
6. 调用 LLM
```

**改造点**:

```python
def qa_node(state: QAInput, config: RunnableConfig, runtime: Runtime[Context]) -> QAOutput:
    """
    title: 问答沉淀（RAG增强）
    desc: 基于向量检索的智能问答
    integrations: 大语言模型, 向量检索
    """
    ctx = runtime.context

    try:
        workspace = os.getenv("COZE_WORKSPACE_PATH", ".")

        # 【新增】初始化检索服务
        from src.services.embedding_service import EmbeddingService
        from src.services.vector_index_service import VectorIndexService
        from src.services.retrieval_service import RetrievalService

        embedder = EmbeddingService()
        index_service = VectorIndexService(
            index_path=os.path.join(
                workspace,
                "assets/knowledge_base/embeddings/summaries/index.faiss"
            ),
            embedding_dim=embedder.get_embedding_dimension()
        )

        retrieval = RetrievalService(
            embedding_service=embedder,
            vector_index_service=index_service,
            top_k=qa_limit_config.get("max_docs", 10)
        )

        # 【改造】使用向量检索替代遍历
        relevant_docs = retrieval.retrieve_with_content(
            query=state.question,
            top_k=qa_limit_config.get("max_docs", 10),
            max_content_length=qa_limit_config.get("max_doc_chars", 5000)
        )

        # ... 其余逻辑保持不变
```

---

## 📊 数据结构设计

### 嵌入索引目录结构

```
assets/knowledge_base/embeddings/
├── summaries/
│   ├── index.faiss              # FAISS 索引文件
│   ├── documents.json           # 文档元数据
│   ├── config.json              # 索引配置
│   └── .cache/                  # 缓存目录（可选）
└── concepts/
    ├── index.faiss
    ├── documents.json
    └── config.json
```

### documents.json 格式

```json
{
  "version": "1.0",
  "created_at": "2025-04-09T10:00:00Z",
  "updated_at": "2025-04-09T12:00:00Z",
  "embedding_dim": 384,
  "index_type": "flat",
  "total_documents": 100,
  "documents": {
    "doc_20250409_100001": {
      "doc_id": "doc_20250409_100001",
      "title": "知识库系统介绍",
      "file_path": "assets/knowledge_base/wiki/summaries/20250409_100001.md",
      "content_preview": "知识库系统是一个基于LLM的个人知识管理...",
      "file_type": "summary",
      "created_at": "2025-04-09T10:00:00Z",
      "embedding_id": 0
    },
    "doc_20250409_100002": {
      "doc_id": "doc_20250409_100002",
      "title": "摄取功能说明",
      "file_path": "assets/knowledge_base/wiki/summaries/20250409_100002.md",
      "content_preview": "摄取功能支持Markdown、HTML等格式...",
      "file_type": "summary",
      "created_at": "2025-04-09T10:30:00Z",
      "embedding_id": 1
    }
  }
}
```

### config.json 格式

```json
{
  "index_config": {
    "index_type": "flat",
    "metric": "L2",
    "embedding_dim": 384,
    "nlist": 100,
    "nprobe": 10
  },
  "embedding_config": {
    "model_name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "device": "cpu",
    "batch_size": 32,
    "normalize_embeddings": true
  },
  "retrieval_config": {
    "top_k": 10,
    "max_content_length": 5000,
    "min_similarity_threshold": 0.5
  }
}
```

---

## ⚙️ 配置文件设计

### embedding_config.json

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

### retrieval_config.json

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

---

## 🔄 工作流程设计

### 摄取流程（增强）

```
1. Ingest Node
   ↓
2. Summary Node
   ↓
3. ConceptExtract Node
   ↓
4. IndexUpdate Node（保持不变）
   ↓
5. 【新增】Embedding Node
   - 读取摘要文件
   - 生成文档嵌入
   - 保存到向量索引
   ↓
6. 完成
```

### 问答流程（改造）

```
1. 用户提问
   ↓
2. QA Node（改造）
   - 初始化检索服务
   - 问题嵌入
   - 向量检索（Top-K）
   - 读取文档内容
   - 构建上下文
   ↓
3. LLM 生成答案
   ↓
4. 返回结果
```

### 索引重建流程

```
1. 扫描 wiki/summaries 和 wiki/concepts
   ↓
2. 读取所有文档
   ↓
3. 批量生成嵌入
   ↓
4. 创建向量索引
   ↓
5. 保存索引和元数据
   ↓
6. 完成
```

---

## 🧪 测试设计

### 单元测试

**test_embedding_service.py**:
- `test_load_model()`: 测试模型加载
- `test_embed_text()`: 测试单文本嵌入
- `test_embed_batch()`: 测试批量嵌入
- `test_embedding_dimension()`: 测试向量维度
- `test_empty_text()`: 测试空文本处理

**test_vector_index_service.py**:
- `test_create_index()`: 测试索引创建
- `test_add_document()`: 测试添加文档
- `test_search()`: 测试检索
- `test_save_load_index()`: 测试保存和加载
- `test_rebuild_from_documents()`: 测试重建索引

**test_retrieval_service.py**:
- `test_retrieve()`: 测试检索
- `test_retrieve_with_content()`: 测试带内容检索
- `test_index_stats()`: 测试统计信息

### 集成测试

**test_rag_integration.py**:
- `test_full_ingest_flow()`: 测试完整摄取流程
- `test_full_qa_flow()`: 测试完整问答流程
- `test_index_rebuild()`: 测试索引重建
- `test_performance()`: 测试性能

### 性能测试

**test_rag_performance.py**:
- 测试嵌入生成速度
- 测试检索速度
- 测试内存占用
- 测试不同文档规模下的性能

---

## 📈 性能指标

### 目标指标

| 指标 | 目标值 | 测试方法 |
|------|--------|---------|
| 嵌入生成速度 | < 100ms/文档 | 测试脚本 |
| 检索速度 | < 50ms | 测试脚本 |
| 问答响应时间 | < 5s | 测试脚本 |
| 支持文档数 | 1000+ | 压力测试 |
| 准确性提升 | 5x | A/B 测试 |
| 上下文利用率 | 80% | 日志分析 |

### 性能基准

```
硬件配置:
- CPU: 4核
- 内存: 8GB
- 存储: SSD

预期性能:
- 单文档嵌入: ~80ms
- 1000文档检索: ~30ms
- 完整问答: ~3s
- 索引1000文档: ~2分钟
```

---

## 🛠️ 实施计划

### 任务清单

#### 阶段 1: 准备（0.5天）

- [ ] 创建服务目录结构
- [ ] 创建嵌入索引目录
- [ ] 编写配置文件
- [ ] 安装依赖包

#### 阶段 2: 核心服务开发（1天）

- [ ] 实现 EmbeddingService
- [ ] 实现 VectorIndexService
- [ ] 实现 RetrievalService
- [ ] 编写单元测试

#### 阶段 3: 集成和改造（0.5天）

- [ ] 改造 qa_node.py
- [ ] 编写集成测试
- [ ] 编写索引重建脚本
- [ ] 编写使用文档

#### 阶段 4: 测试和优化（0.5天）

- [ ] 运行单元测试
- [ ] 运行集成测试
- [ ] 性能测试
- [ ] 优化和调整

### 时间线

```
Day 1 上午: 准备 + EmbeddingService
Day 1 下午: VectorIndexService + RetrievalService
Day 2 上午: qa_node改造 + 测试
Day 2 下午: 文档 + 优化
```

---

## 🚨 风险和缓解

### 风险1: 模型下载失败

**风险**: 无法下载嵌入模型

**缓解**:
- 提供备用模型源
- 支持本地模型加载
- 提供预下载脚本

### 风险2: 内存不足

**风险**: 模型加载导致内存溢出

**缓解**:
- 选择轻量级模型
- 支持模型卸载
- 优化内存使用

### 风险3: 性能不达标

**风险**: 检索速度慢

**缓解**:
- 使用高效索引
- 批量处理
- 异步处理

### 风险4: 准确性提升不明显

**风险**: 向量检索效果不如预期

**缓解**:
- 调整模型
- 优化分块策略
- 添加重排序

---

## 📝 依赖清单

### Python 包

```txt
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
numpy>=1.24.0
```

### 系统要求

- Python 3.8+
- 内存: 4GB+
- 存储: 10GB+

---

## 📚 相关文档

- [RAG 总体方案](RAG_PHASE1_OVERVIEW.md)
- [使用指南](RAG_PHASE1_GUIDE.md)
- [API 文档](RAG_PHASE1_API.md)
- [故障排查](RAG_PHASE1_TROUBLESHOOTING.md)

---

**文档版本**: v1.0
**创建日期**: 2025-04-09
**状态**: ✅ 设计完成
**下一步**: 开始实施
