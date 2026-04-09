## 项目概述
- **名称**: 知识库编译系统
- **功能**: 基于 LLM 的个人知识库管理系统，实现资料的摄取、编译、问答和健康检查

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| ingest | `nodes/ingest_node.py` | task | 从用户输入的内容（markdown/html/纯文本）保存到raw目录 | ingest模式 → summary | - |
| summary | `nodes/summary_node.py` | agent | 生成文档结构化摘要 | → concept_extract | `config/summary_llm_cfg.json` |
| concept_extract | `nodes/concept_extract_node.py` | agent | 从摘要中抽取概念 | → index_update | `config/concept_extract_llm_cfg.json` |
| index_update | `nodes/index_update_node.py` | task | 更新索引文件 | → END | - |
| qa | `nodes/qa_node.py` | agent | 处理问答并沉淀 | → END | `config/qa_llm_cfg.json` |
| health_check | `nodes/health_check_node.py` | agent | 知识库健康检查 | → END | `config/health_check_llm_cfg.json` |
| route_by_mode | `graph.py` | condition | 根据模式路由 | ingest → summary/qa/health_check | - |

**类型说明**: task(任务节点) / agent(大模型) / condition(条件分支)

## 子图清单
无子图（所有功能在主图中实现）

## 技能使用
- 节点`summary`、`concept_extract`、`qa`、`health_check`使用LLM技能：文本生成和分析

## 工作流模式

### 1. 摄取模式 (ingest)
**功能**: 摄取用户输入的内容并编译
**流程**: ingest → summary → concept_extract → index_update
**输入参数**:
```json
{
  "content": "# 我的文档标题\n\n这是文档内容...",
  "content_type": "markdown",
  "title": "我的文档标题",
  "mode": "ingest"
}
```

**content_type选项**:
- `markdown`: Markdown格式内容
- `html`: HTML格式内容
- `text`: 纯文本内容

### 2. 问答模式 (qa)
**功能**: 基于知识库回答问题并沉淀
**流程**: ingest(跳过) → qa → END
**输入参数**:
```json
{
  "question": "什么是知识库编译？",
  "mode": "qa"
}
```

### 3. 健康检查模式 (health_check)
**功能**: 检查知识库质量
**流程**: ingest(跳过) → health_check → END
**输入参数**:
```json
{
  "mode": "health_check",
  "health_check_mode": "full"
}
```

**health_check_mode选项**:
- `full`: 完整检查（一致性、完整性、孤岛）
- `consistency`: 仅检查一致性
- `completeness`: 仅检查完整性
- `orphan`: 仅检查孤岛

## 目录结构
```
assets/knowledge_base/
├── raw/              # 原始资料
│   ├── articles/     # 网页文章
│   ├── podcasts/     # 播客内容
│   └── papers/       # 论文
├── wiki/             # 编译产物
│   ├── indexes/      # 索引文件
│   ├── summaries/    # 摘要
│   └── concepts/     # 概念条目
└── outputs/          # 运行时输出
    ├── qa/           # 问答归档
    └── health/       # 健康检查报告
```

## 核心特性

### 编译流程
1. **摄取**: 接受用户输入的markdown/html/纯文本内容，自动提取标题和元数据
2. **摘要**: 生成结构化摘要（核心结论、关键证据、疑点、术语）
3. **概念抽取**: 识别核心概念，创建或更新概念条目
4. **索引更新**: 维护All-Sources.md和All-Concepts.md索引

### 链接格式规范
所有知识链接统一使用Markdown链接格式：`[title](path)`
- **索引文件**: 文件名作为title，相对路径作为path
- **概念文件**: 来源文件使用markdown链接格式
- **问答文件**: 来源文档使用markdown链接格式
- **健康检查**: 概念文件名使用markdown链接格式

### 问答沉淀
- 每次问答结果自动保存为Markdown文件
- 保留推理过程和来源引用
- 支持从摘要和概念中检索信息

### 健康检查
- **一致性**: 检查概念定义冲突
- **完整性**: 识别缺少定义/例子的概念
- **孤岛**: 发现孤立的概念条目

## 设计理念
基于 Karpathy 的"LLM Knowledge Bases"方法论：
- 将知识库当代码仓库管理
- LLM 作为编译器
- 支持增量编译
- 可追溯的来源引用
