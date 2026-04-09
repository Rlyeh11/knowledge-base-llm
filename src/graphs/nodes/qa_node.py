import os
import datetime
import json
import glob
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import QAInput, QAOutput

def qa_node(state: QAInput, config: RunnableConfig, runtime: Runtime[Context]) -> QAOutput:
    """
    title: 问答沉淀
    desc: 处理复杂问题，基于知识库内容生成答案并保存到outputs/qa
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    try:
        workspace = os.getenv("COZE_WORKSPACE_PATH", ".")
        
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
                            # 只读取前2000字符作为上下文
                            relevant_docs.append({
                                "file": os.path.relpath(file_path, workspace),
                                "content": content[:2000]
                            })
                    except:
                        pass
        
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
            for doc in relevant_docs[:5]  # 限制为5个文档
        ])
        
        # 渲染用户提示词
        user_prompt = user_prompt_template.replace("{{question}}", state.question)
        user_prompt = user_prompt.replace("{{context}}", context[:8000])
        
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
            f.write("---\n\n")
            f.write("## 答案\n\n")
            f.write(answer)
            f.write("\n\n---\n\n")
            f.write("## 来源文档\n\n")
            for doc in relevant_docs[:5]:
                f.write(f"- `{doc['file']}`\n")
        
        return QAOutput(
            answer=answer,
            qa_file_path=qa_file_path,
            qa_sources=[doc['file'] for doc in relevant_docs[:5]],
            success=True
        )
        
    except Exception as e:
        return QAOutput(
            answer=f"处理失败: {str(e)}",
            qa_file_path="",
            qa_sources=[],
            success=False
        )
