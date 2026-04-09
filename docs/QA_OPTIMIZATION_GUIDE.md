# 问答系统优化配置指南

## 📋 概述

本文档说明如何优化问答系统的性能，以支持更多的文档和更准确的答案。

## 🎯 当前限制

优化前的默认配置：
- **最大文档数**: 5 个
- **单文档字符数**: 2000 字符
- **总上下文长度**: 8000 字符

优化后的默认配置：
- **最大文档数**: 10 个（可配置）
- **单文档字符数**: 5000 字符（可配置）
- **总上下文长度**: 20000 字符（可配置）

## 🚀 快速开始

### 1. 查看当前配置

```bash
cat config/qa_limit_cfg.json
```

### 2. 修改配置

```bash
nano config/qa_limit_cfg.json
```

### 3. 重启服务

```bash
make run
```

## ⚙️ 配置参数说明

### 基础配置

```json
{
  "max_docs": 10,
  "max_doc_chars": 5000,
  "max_context_chars": 20000
}
```

#### `max_docs` (最大文档数)

**说明**: 问答时使用的最大文档数量

**默认值**: 10

**建议值**:
- 小型知识库 (< 20 文档): 20
- 中型知识库 (20-100 文档): 10-15
- 大型知识库 (> 100 文档): 5-10

**注意**:
- 增加此值会提高答案的全面性，但会增加响应时间
- 过高可能导致 LLM 上下文溢出

#### `max_doc_chars` (单文档字符数)

**说明**: 从每个文档中读取的最大字符数

**默认值**: 5000

**建议值**:
- 短文档 (< 1000 字符): 1000
- 中等文档 (1000-5000 字符): 5000
- 长文档 (> 5000 字符): 8000-10000

**注意**:
- 此值控制每个文档的信息密度
- 建议与 `max_context_chars` 配合使用

#### `max_context_chars` (总上下文长度)

**说明**: 传递给 LLM 的总上下文字符数

**默认值**: 20000

**建议值**:
- 短上下文模型 (8K tokens): ~6000
- 中等上下文模型 (32K tokens): ~20000
- 长上下文模型 (128K tokens): ~50000

**计算公式**:
```
max_context_chars = max_docs * max_doc_chars * 1.5
```
（1.5 是考虑到格式开销的系数）

### 高级配置

#### `enable_smart_retrieval` (启用智能检索)

**说明**: 是否启用基于关键词的智能检索

**默认值**: false

**类型**: Boolean

**功能**:
- `false`: 按文件顺序选择文档
- `true`: 根据问题关键词匹配度选择文档

**建议**:
- 文档数量 < 30: `false`（不需要）
- 文档数量 30-100: `true`（推荐）
- 文档数量 > 100: 考虑使用向量数据库（RAG）

#### `retrieval_method` (检索方法)

**说明**: 智能检索使用的方法

**默认值**: keyword

**可选值**:
- `keyword`: 关键词匹配
- `tfidf`: TF-IDF 相似度（需要额外依赖）

**注意**: 当前版本只支持 `keyword`

#### `min_similarity_score` (最小相似度分数)

**说明**: 文档与问题的最小相似度阈值

**默认值**: 0.1

**范围**: 0.0 - 1.0

**建议值**:
- 宽松筛选: 0.05 - 0.1
- 平衡筛选: 0.1 - 0.2
- 严格筛选: 0.2 - 0.5

## 📊 性能配置建议

### 场景 1: 小型知识库 (< 20 文档)

```json
{
  "max_docs": 20,
  "max_doc_chars": 3000,
  "max_context_chars": 25000,
  "enable_smart_retrieval": false
}
```

**特点**:
- 使用所有文档
- 高准确性
- 响应时间快

### 场景 2: 中型知识库 (20-100 文档)

```json
{
  "max_docs": 15,
  "max_doc_chars": 5000,
  "max_context_chars": 30000,
  "enable_smart_retrieval": true,
  "min_similarity_score": 0.15
}
```

**特点**:
- 智能筛选最相关文档
- 平衡准确性和速度
- 适合大多数场景

### 场景 3: 大型知识库 (100-500 文档)

```json
{
  "max_docs": 10,
  "max_doc_chars": 8000,
  "max_context_chars": 40000,
  "enable_smart_retrieval": true,
  "min_similarity_score": 0.2
}
```

**特点**:
- 严格筛选相关文档
- 快速响应
- 需要高质量关键词匹配

### 场景 4: 超大型知识库 (> 500 文档)

**建议**: 使用向量数据库 (RAG)

```json
{
  "max_docs": 5,
  "max_doc_chars": 10000,
  "max_context_chars": 50000,
  "enable_smart_retrieval": true,
  "min_similarity_score": 0.3
}
```

**注意**:
- 此场景建议升级到完整的 RAG 系统
- 参考 `docs/QA_PERFORMANCE_ANALYSIS.md` 了解更多

## 🧪 测试配置

### 测试问答性能

```bash
# 使用测试问题
make qa question="什么是知识库系统？"

# 查看日志中的文档使用情况
tail -f /app/work/logs/bypass/app.log
```

### 性能基准测试

```bash
# 运行性能测试
python tests/test_qa_performance.py
```

### 监控指标

关注以下指标：
1. **响应时间**: < 10 秒为佳
2. **文档使用数**: 是否达到配置的 max_docs
3. **上下文长度**: 是否充分利用 max_context_chars
4. **答案质量**: 是否准确回答问题

## 🔧 故障排查

### 问题 1: 答案不完整

**原因**: 文档数或上下文长度不足

**解决方案**:
```json
{
  "max_docs": 20,
  "max_context_chars": 30000
}
```

### 问题 2: 响应太慢

**原因**: 使用的文档太多或上下文太长

**解决方案**:
```json
{
  "max_docs": 5,
  "max_context_chars": 10000,
  "enable_smart_retrieval": true
}
```

### 问题 3: 答案不准确

**原因**: 相关文档没有被选中

**解决方案**:
```json
{
  "enable_smart_retrieval": true,
  "min_similarity_score": 0.1
}
```

### 问题 4: LLM 上下文溢出

**原因**: 上下文长度超过模型限制

**解决方案**:
```json
{
  "max_context_chars": 6000
}
```

**注意**: 检查模型的 token 限制

## 📈 进阶优化

### 1. 使用 TF-IDF 检索

安装依赖:
```bash
pip install scikit-learn
```

修改配置:
```json
{
  "retrieval_method": "tfidf"
}
```

### 2. 使用向量数据库 (RAG)

参考: `docs/QA_PERFORMANCE_ANALYSIS.md`

### 3. 实现缓存机制

缓存常见问题的答案，减少重复计算

### 4. 分级检索

先使用关键词快速筛选，再用向量检索精确匹配

## 📚 相关文档

- [问答系统性能分析](QA_PERFORMANCE_ANALYSIS.md) - 详细的性能分析和优化方案
- [模型配置](MODEL_CONFIG.md) - LLM 配置说明
- [使用指南](USAGE.md) - 完整使用说明

## 🆘 获取帮助

- 查看日志: `tail -f /app/work/logs/bypass/app.log`
- 提交问题: [GitHub Issues](https://github.com/Rlyeh11/knowledge-base-llm/issues)

---

**文档版本**: v1.0
**更新日期**: 2025-04-09
**状态**: ✅ 可用
