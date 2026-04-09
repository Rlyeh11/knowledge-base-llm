import os
import datetime
import json
import glob
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import QAInput, QAOutput


def _load_qa_limit_config(workspace: str) -> dict:
    """加载问答限制配置"""
    config_path = os.path.join(workspace, "config/qa_limit_cfg.json")
    default_config = {
        "max_docs": 10,
        "max_doc_chars": 5000,
        "max_context_chars": 20000,
        "enable_smart_retrieval": False,
        "retrieval_method": "keyword",
        "min_similarity_score": 0.1
    }

    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                default_config.update(loaded_config)
        except Exception as e:
            print(f"Warning: Failed to load qa_limit_cfg.json, using defaults: {e}")

    return default_config


def _calculate_keyword_similarity(question: str, content: str) -> float:
    """计算问题与文档的关键词相似度（简单的关键词匹配）"""
    question_words = set(question.lower().split())
    content_lower = content.lower()

    if not question_words:
        return 0.0

    # 计算问题关键词在文档中的出现次数
    match_count = sum(1 for word in question_words if word in content_lower)
    similarity = match_count / len(question_words)

    return similarity


def _filter_relevant_docs(docs: list, question: str, limit: int, min_score: float) -> list:
    """根据相关性过滤文档"""
    if not docs:
        return []

    # 为每个文档计算相关性分数
    scored_docs = []
    for doc in docs:
        score = _calculate_keyword_similarity(question, doc["content"])
        if score >= min_score:
            scored_docs.append({
                "doc": doc,
                "score": score
            })

    # 按分数降序排序
    scored_docs.sort(key=lambda x: x["score"], reverse=True)

    # 返回前 N 个文档
    return [item["doc"] for item in scored_docs[:limit]]


def qa_node(state: QAInput, config: RunnableConfig, runtime: Runtime[Context]) -> QAOutput:
    """
    title: 问答沉淀
    desc: 处理复杂问题，基于知识库内容生成答案并保存到outputs/qa
    integrations: 大语言模型
    """
    ctx = runtime.context

    try:
        workspace = os.getenv("COZE_WORKSPACE_PATH", ".")

        # 加载问答限制配置
        qa_limit_config = _load_qa_limit_config(workspace)
        max_docs = qa_limit_config.get("max_docs", 10)
        max_doc_chars = qa_limit_config.get("max_doc_chars", 5000)
        max_context_chars = qa_limit_config.get("max_context_chars", 20000)
        enable_smart_retrieval = qa_limit_config.get("enable_smart_retrieval", False)
        min_similarity_score = qa_limit_config.get("min_similarity_score", 0.1)

        # 收集相关文档
        relevant_docs = []

        # 从wiki目录收集文档
        wiki_dirs = [
            os.path.join(workspace, "assets/knowledge_base/wiki/summaries"),
            os.path.join(workspace, "assets/knowledge_base/wiki/concepts")
        ]

        for wiki_dir in wiki_dirs:
            if os.path.exists(wiki_dir):
                for file_path in glob.glob(os.path.join(wiki_dir, "*.md")):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # 读取配置的字符数作为上下文
                            relevant_docs.append({
                                "file": os.path.relpath(file_path, workspace),
                                "content": content[:max_doc_chars]
                            })
                    except Exception:
                        pass

        # 根据配置选择检索方式
        if enable_smart_retrieval and len(relevant_docs) > max_docs:
            # 智能检索：基于相关性过滤
            relevant_docs = _filter_relevant_docs(
                relevant_docs,
                state.question,
                limit=max_docs,
                min_score=min_similarity_score
            )
        else:
            # 普通检索：按文件顺序选择
            relevant_docs = relevant_docs[:max_docs]

        # 读取LLM配置
        cfg_file = os.path.join(workspace, config['metadata']['llm_cfg'])
        with open(cfg_file, 'r', encoding='utf-8') as f:
            llm_cfg = json.load(f)

        model_config = llm_cfg.get("config", {})
        system_prompt = llm_cfg.get("sp", "")
        user_prompt_template = llm_cfg.get("up", "")

        # 构建上下文
        context = "\n\n".join([
            f"## 文档: {doc['file']}\n{doc['content']}"
            for doc in relevant_docs
        ])

        # 限制总上下文长度
        context = context[:max_context_chars]

        # 渲染用户提示词
        user_prompt = user_prompt_template.replace("{{question}}", state.question)
        user_prompt = user_prompt.replace("{{context}}", context)

        # 创建LLM客户端
        llm_client = LLMClient(ctx=ctx)

        # 调用LLM生成答案
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = llm_client.invoke(
            messages=messages,
            model=model_config.get("model", "doubao-seed-1-8-251228"),
            temperature=model_config.get("temperature", 0.5),
            max_completion_tokens=model_config.get("max_completion_tokens", 4000)
        )

        # 提取响应内容
        if isinstance(response.content, str):
            answer = response.content
        elif isinstance(response.content, list):
            answer = " ".join(item.get("text", "") for item in response.content if isinstance(item, dict))
        else:
            answer = str(response.content)

        # 生成问答文件路径
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_question = "".join(c for c in state.question[:30] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_question = safe_question.replace(' ', '_')
        qa_filename = f"qa_{timestamp}_{safe_question}.md"
        qa_dir = os.path.join(workspace, "assets/knowledge_base/outputs/qa")
        os.makedirs(qa_dir, exist_ok=True)
        qa_file_path = os.path.join(qa_dir, qa_filename)

        # 保存问答文件
        with open(qa_file_path, 'w', encoding='utf-8') as f:
            f.write(f"# 问题: {state.question}\n\n")
            f.write(f"**提问时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**使用文档数**: {len(relevant_docs)}\n\n")
            f.write(f"**上下文长度**: {len(context)} 字符\n\n")
            f.write("---\n\n")
            f.write("## 答案\n\n")
            f.write(answer)
            f.write("\n\n---\n\n")
            f.write("## 来源文档\n\n")
            for doc in relevant_docs:
                file_title = os.path.basename(doc['file'])
                f.write(f"- [{file_title}]({doc['file']})\n")

        return QAOutput(
            answer=answer,
            qa_file_path=qa_file_path,
            qa_sources=[doc['file'] for doc in relevant_docs],
            success=True
        )

    except Exception as e:
        return QAOutput(
            answer=f"处理失败: {str(e)}",
            qa_file_path="",
            qa_sources=[],
            success=False
        )
