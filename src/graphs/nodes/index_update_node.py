import os
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import IndexUpdateInput, IndexUpdateOutput

def index_update_node(state: IndexUpdateInput, config: RunnableConfig, runtime: Runtime[Context]) -> IndexUpdateOutput:
    """
    title: 更新索引
    desc: 更新All-Sources.md和All-Concepts.md索引文件
    integrations: 
    """
    ctx = runtime.context
    
    try:
        workspace = os.getenv("COZE_WORKSPACE_PATH", ".")
        sources_updated = False
        concepts_updated = False
        
        # 更新All-Sources.md
        sources_index_path = os.path.join(workspace, "assets/knowledge_base/wiki/indexes/All-Sources.md")
        os.makedirs(os.path.dirname(sources_index_path), exist_ok=True)
        
        # 读取原始文件标题
        raw_title = "Unknown"
        try:
            with open(state.raw_file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                if first_line.startswith("# "):
                    raw_title = first_line[2:].strip()
        except:
            pass
        
        # 追加到All-Sources.md
        with open(sources_index_path, 'a', encoding='utf-8') as f:
            f.write(f"\n## {raw_title}\n")
            f.write(f"- **原始文件**: `../../{os.path.relpath(state.raw_file_path, workspace)}`\n")
            f.write(f"- **摘要文件**: `../../{os.path.relpath(state.summary_file_path, workspace)}`\n")
        
        sources_updated = True
        
        # 更新All-Concepts.md
        if state.concepts:
            concepts_index_path = os.path.join(workspace, "assets/knowledge_base/wiki/indexes/All-Concepts.md")
            
            with open(concepts_index_path, 'a', encoding='utf-8') as f:
                f.write(f"\n## 从 '{raw_title}' 抽取的概念\n\n")
                for concept in state.concepts:
                    concept_name = concept.get("name", "Unknown")
                    f.write(f"- **{concept_name}**\n")
            
            concepts_updated = True
        
        return IndexUpdateOutput(
            sources_index_updated=sources_updated,
            concepts_index_updated=concepts_updated,
            success=True
        )
        
    except Exception as e:
        return IndexUpdateOutput(
            sources_index_updated=False,
            concepts_index_updated=False,
            success=False
        )
