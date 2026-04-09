import os
import datetime
import json
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import HumanMessage
from graphs.state import SummaryInput, SummaryOutput

def summary_node(state: SummaryInput, config: RunnableConfig, runtime: Runtime[Context]) -> SummaryOutput:
    """
    title: 生成文档摘要
    desc: 为raw文档生成结构化摘要，包括核心结论、关键证据、疑点、术语
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    try:
        # 读取原始文件
        with open(state.raw_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 读取LLM配置
        cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
        with open(cfg_file, 'r', encoding='utf-8') as f:
            llm_cfg = json.load(f)
        
        model_config = llm_cfg.get("config", {})
        system_prompt = llm_cfg.get("sp", "")
        user_prompt_template = llm_cfg.get("up", "")
        
        # 渲染用户提示词
        user_prompt = user_prompt_template.replace("{{content}}", content[:10000])  # 限制长度
        
        # 创建LLM客户端
        llm_client = LLMClient(ctx=ctx)
        
        # 调用LLM生成摘要
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = llm_client.invoke(
            messages=messages,
            model=model_config.get("model", "doubao-seed-1-8-251228"),
            temperature=model_config.get("temperature", 0.3),
            max_completion_tokens=model_config.get("max_completion_tokens", 4000)
        )
        
        # 提取响应内容
        if isinstance(response.content, str):
            summary_content = response.content
        elif isinstance(response.content, list):
            summary_content = " ".join(item.get("text", "") for item in response.content if isinstance(item, dict))
        else:
            summary_content = str(response.content)
        
        # 生成摘要文件路径
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_filename = os.path.basename(state.raw_file_path)
        summary_filename = f"summary_{timestamp}_{raw_filename}"
        summary_dir = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "."), "assets/knowledge_base/wiki/summaries")
        os.makedirs(summary_dir, exist_ok=True)
        summary_file_path = os.path.join(summary_dir, summary_filename)
        
        # 保存摘要
        with open(summary_file_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        return SummaryOutput(
            summary_content=summary_content,
            summary_file_path=summary_file_path,
            success=True
        )
        
    except Exception as e:
        return SummaryOutput(
            summary_content="",
            summary_file_path="",
            success=False
        )
