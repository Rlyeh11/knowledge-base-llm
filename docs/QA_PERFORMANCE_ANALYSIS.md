# 问答系统性能分析与优化方案

## 📊 当前系统的限制分析

### 现有实现的问题

经过代码分析，当前的问答系统存在以下硬编码限制：

#### 1. 文档数量限制

**位置**: `src/graphs/nodes/qa_node.py` 第 57 行

```python
relevant_docs[:5]  # 只取前5个文档
```

**影响**:
- 当知识库中有超过 5 个文档时，后续文档会被忽略
- 答案可能遗漏重要信息
- 无法利用完整的知识库内容

#### 2. 单文档内容截断

**位置**: `src/graphs/nodes/qa_node.py` 第 40 行

```python
"content": content[:2000]  # 每个文档只读前2000字符
```

**影响**:
- 长文档的后续内容被截断
- 可能丢失关键信息
- 答案的准确性降低

#### 3. 总上下文长度限制

**位置**: `src/graphs/nodes/qa_node.py` 第 62 行

```python
context[:8000]  # 总上下文限制为8000字符
```

**影响**:
- 即使有5个文档，总内容也被限制在8000字符
- 平均每个文档只能用1600字符
- 信息密度极低

#### 4. 缺乏智能检索

**位置**: `src/graphs/nodes/qa_node.py` 第 26-44 行

```python
# 直接遍历所有文档，没有根据问题进行相关性排序
for file_path in glob.glob(os.path.join(wiki_dir, "*.md")):
```

**影响**:
- 所有文档平等对待，不区分相关性
- 可能包含大量无关信息
- 降低答案质量

## 📈 性能影响评估

### 文档数量 vs 性能

| 文档数量 | 当前行为 | 性能 | 准确性 |
|---------|---------|------|--------|
| < 5 | 全部使用 | ✅ 正常 | ✅ 高 |
| 5-20 | 只用前5个 | ⚠️ 一般 | ⚠️ 可能遗漏 |
| 20-100 | 只用前5个 | ❌ 差 | ❌ 遗漏严重 |
| > 100 | 只用前5个 | ❌ 很差 | ❌ 几乎不可用 |

### LLM 上下文限制

不同模型的上下文长度限制：

| 模型 | 上下文长度 | 当前使用 | 利用率 |
|------|-----------|---------|--------|
| 豆包 | 128K tokens | ~6K tokens | 5% |
| DeepSeek | 32K tokens | ~6K tokens | 19% |
| Kimi | 128K tokens | ~6K tokens | 5% |
| GPT-4 | 128K tokens | ~6K tokens | 5% |

**结论**: 当前系统只利用了模型 5%-19% 的上下文能力！

## 🚀 优化方案

### 方案 1: 增加文档数量（快速优化）

**优点**: 实现简单，立即见效
**缺点**: 不解决根本问题

```python
# 修改 src/graphs/nodes/qa_node.py
relevant_docs[:20]  # 从5增加到20
context[:32000]     # 从8000增加到32000
```

**预计效果**:
- 可以处理 20 个文档
- 准确性提升约 2-3 倍
- 适合中等规模知识库（< 50 文档）

### 方案 2: 智能检索 + RAG（推荐）

**优点**: 大幅提升准确性和效率
**缺点**: 需要引入向量数据库

**架构设计**:

```
用户问题 → 向量化检索 → Top-K 相关文档 → LLM 生成答案
                ↓
         向量数据库 (FAISS/Qdrant/Weaviate)
                ↓
         文档嵌入 (Sentence-BERT/Text-Embedding)
```

**实现步骤**:

1. **文档嵌入化**（在摄取阶段）
   ```python
   from sentence_transformers import SentenceTransformer

   embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
   embedding = embedder.encode(document_content)
   ```

2. **构建向量索引**
   ```python
   import faiss
   index = faiss.IndexFlatL2(384)  # MiniLM 的维度
   index.add(embeddings)
   ```

3. **相似度检索**
   ```python
   query_embedding = embedder.encode(user_question)
   distances, indices = index.search(query_embedding.reshape(1, -1), k=5)
   ```

**预计效果**:
- 可以处理数千个文档
- 准确性提升 10 倍以上
- 响应速度更快

### 方案 3: 分级检索（平衡方案）

**优点**: 不需要向量数据库，易于实现
**缺点**: 准确性不如 RAG

**架构设计**:

```
用户问题
    ↓
关键词匹配 + TF-IDF 相关性评分
    ↓
Top-20 相关文档
    ↓
LLM 处理
```

**实现步骤**:

1. **构建 TF-IDF 索引**
   ```python
   from sklearn.feature_extraction.text import TfidfVectorizer

   vectorizer = TfidfVectorizer()
   tfidf_matrix = vectorizer.fit_transform(documents)
   ```

2. **相关性评分**
   ```python
   from sklearn.metrics.pairwise import cosine_similarity

   query_vec = vectorizer.transform([user_question])
   similarities = cosine_similarity(query_vec, tfidf_matrix)
   top_docs = np.argsort(similarities[0])[-20:][::-1]
   ```

3. **获取 Top-K 文档**
   ```python
   relevant_docs = [documents[i] for i in top_docs]
   ```

**预计效果**:
- 可以处理数百个文档
- 准确性提升 3-5 倍
- 实现难度中等

### 方案 4: 混合方案（生产推荐）

**优点**: 结合多种方法的优点
**缺点**: 实现复杂度高

**架构设计**:

```
用户问题
    ↓
├─→ 关键词匹配 (快速筛选 Top-50)
├─→ 向量检索 (精确检索 Top-20)
└─→ LLM 重排序 (Top-10)
    ↓
LLM 生成答案
```

## 🔧 快速修复代码

### 修复 1: 增加文档和上下文限制

```python
# 修改 src/graphs/nodes/qa_node.py

# 第 40 行：增加单文档字符限制
relevant_docs.append({
    "file": os.path.relpath(file_path, workspace),
    "content": content[:5000]  # 从 2000 增加到 5000
})

# 第 57 行：增加文档数量
for doc in relevant_docs[:10]:  # 从 5 增加到 10
    ...

# 第 62 行：增加总上下文长度
context[:20000]  # 从 8000 增加到 20000
```

### 修复 2: 添加配置化限制

创建 `config/qa_limit_cfg.json`:

```json
{
    "max_docs": 10,
    "max_doc_chars": 5000,
    "max_context_chars": 20000,
    "enable_smart_retrieval": false
}
```

修改代码读取配置:

```python
with open("config/qa_limit_cfg.json", "r") as f:
    limit_cfg = json.load(f)

max_docs = limit_cfg.get("max_docs", 10)
max_doc_chars = limit_cfg.get("max_doc_chars", 5000)
max_context_chars = limit_cfg.get("max_context_chars", 20000)
```

## 📊 优化效果对比

| 方案 | 支持文档数 | 准确性提升 | 响应速度 | 实现难度 | 推荐度 |
|------|-----------|-----------|---------|---------|--------|
| 当前 | 5 | - | 快 | - | ❌ |
| 方案1 | 20 | 2-3x | 快 | ⭐ | ⚠️ |
| 方案2 (RAG) | 1000+ | 10x+ | 中 | ⭐⭐⭐ | ✅✅ |
| 方案3 (TF-IDF) | 200 | 3-5x | 快 | ⭐⭐ | ✅ |
| 方案4 (混合) | 500+ | 8x+ | 中快 | ⭐⭐⭐⭐ | ✅✅✅ |

## 🎯 推荐实施路径

### 阶段 1: 快速修复（1小时）

1. 增加文档数量限制（5 → 10）
2. 增加上下文长度（8000 → 20000）
3. 添加配置文件，支持动态调整

**适用场景**: 中小知识库（< 50 文档）

### 阶段 2: 引入智能检索（1天）

1. 实现 TF-IDF 相关性评分
2. 构建文档索引
3. 优化问答流程

**适用场景**: 中等知识库（< 200 文档）

### 阶段 3: 完整 RAG 系统（3-5天）

1. 集成向量数据库（Qdrant/Weaviate）
2. 实现文档嵌入
3. 构建向量索引
4. 实现混合检索

**适用场景**: 大规模知识库（1000+ 文档）

## 📝 总结

### 当前系统的瓶颈

1. ✅ **有文档数量上限**: 硬编码为 5 个文档
2. ✅ **上下文长度受限**: 总共 8000 字符
3. ✅ **缺乏智能检索**: 无法找到最相关的文档
4. ✅ **利用不足**: 只使用了模型 5%-19% 的能力

### 推荐方案

**短期**（立即可用）:
- 使用方案1快速修复，支持 20 个文档

**中期**（1-2周）:
- 实现方案3（TF-IDF），支持 200 个文档

**长期**（1个月）:
- 实现方案4（混合检索），支持 500+ 文档
- 或方案2（完整RAG），支持 1000+ 文档

### 最佳实践建议

1. **监控知识库规模**: 定期检查文档数量
2. **设置告警阈值**: 超过 50 文档时提示用户优化
3. **提供升级路径**: 在文档中说明不同规模的解决方案
4. **性能测试**: 每次优化后进行基准测试

---

**文档版本**: v1.0
**更新日期**: 2025-04-09
**状态**: ✅ 分析完成
