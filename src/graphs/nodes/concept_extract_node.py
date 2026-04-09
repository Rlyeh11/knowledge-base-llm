import os
import datetime
import json
import re
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import ConceptExtractInput, ConceptExtractOutput

def concept_extract_node(state: ConceptExtractInput, config: RunnableConfig, runtime: Runtime[Context]) -> ConceptExtractOutput:
    """
    title: 抽取概念
    desc: 从摘要中抽取概念，映射到wiki/concepts目录，新概念建条目，老概念补证据
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    try:
        # 读取摘要文件
        with open(state.summary_file_path, 'r', encoding='utf-8') as f:
            summary_content = f.read()
        
        # 读取LLM配置
        cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
        with open(cfg_file, 'r', encoding='utf-8') as f:
            llm_cfg = json.load(f)
        
        model_config = llm_cfg.get("config", {})
        system_prompt = llm_cfg.get("sp", "")
        user_prompt_template = llm_cfg.get("up", "")
        
        # 渲染用户提示词
        user_prompt = user_prompt_template.replace("{{summary}}", summary_content)
        
        # 创建LLM客户端
        llm_client = LLMClient(ctx=ctx)
        
        # 调用LLM抽取概念
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
            concepts_response = response.content
        elif isinstance(response.content, list):
            concepts_response = " ".join(item.get("text", "") for item in response.content if isinstance(item, dict))
        else:
            concepts_response = str(response.content)
        
        # 解析概念列表（尝试从JSON格式或文本格式中提取）
        concepts = []
        concept_files = []
        
        # 尝试解析JSON格式的响应
        try:
            # 查找JSON部分
            json_match = re.search(r'\[\s*\{.*\}\s*\]', concepts_response, re.DOTALL)
            if json_match:
                concepts = json.loads(json_match.group())
            else:
                # 如果没有JSON格式，尝试从文本中提取
                concepts = []
        except json.JSONDecodeError:
            # 如果JSON解析失败，使用简单的文本解析
            concepts = []
        
        # 保存概念文件
        concepts_dir = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "."), "assets/knowledge_base/wiki/concepts")
        os.makedirs(concepts_dir, exist_ok=True)
        
        for concept in concepts:
            if not isinstance(concept, dict):
                continue
                
            concept_name = concept.get("name", "").strip()
            if not concept_name:
                continue
            
            # 生成安全的文件名
            safe_name = "".join(c for c in concept_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')
            
            # 检查概念文件是否已存在
            concept_file_path = os.path.join(concepts_dir, f"{safe_name}.md")
            
            if os.path.exists(concept_file_path):
                # 概念已存在，追加新证据
                with open(concept_file_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n## 新证据来源\n")
                    f.write(f"- **来源文件**: {os.path.basename(state.summary_file_path)}\n")
                    if concept.get("evidence"):
                        f.write(f"- **证据**: {concept.get('evidence')}\n")
            else:
                # 新概念，创建文件
                with open(concept_file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {concept_name}\n\n")
                    if concept.get("definition"):
                        f.write(f"## 定义\n{concept.get('definition')}\n\n")
                    if concept.get("description"):
                        f.write(f"## 描述\n{concept.get('description')}\n\n")
                    f.write(f"## 证据来源\n")
                    f.write(f"- **来源文件**: {os.path.basename(state.summary_file_path)}\n")
                    if concept.get("evidence"):
                        f.write(f"- **证据**: {concept.get('evidence')}\n")
            
            concept_files.append(concept_file_path)
        
        # 如果从响应中成功提取了概念，使用它们；否则创建默认概念
        if not concepts:
            # 尝试从文本中提取概念标记（如**概念名**格式）
            concept_matches = re.findall(r'\*\*([^*]+)\*\*', concepts_response)
            for concept_name in concept_matches:
                safe_name = "".join(c for c in concept_name if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_name = safe_name.replace(' ', '_')
                concept_file_path = os.path.join(concepts_dir, f"{safe_name}.md")
                
                if not os.path.exists(concept_file_path):
                    with open(concept_file_path, 'w', encoding='utf-8') as f:
                        f.write(f"# {concept_name}\n\n")
                        f.write(f"## 来源\n")
                        f.write(f"- **来源文件**: {os.path.basename(state.summary_file_path)}\n")
                    
                    concept_files.append(concept_file_path)
                    concepts.append({"name": concept_name})
        
        return ConceptExtractOutput(
            concepts=concepts,
            concept_files=concept_files,
            success=True
        )
        
    except Exception as e:
        return ConceptExtractOutput(
            concepts=[],
            concept_files=[],
            success=False
        )
