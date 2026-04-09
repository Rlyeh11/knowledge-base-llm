from typing import Literal
from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)

# 导入所有节点
from graphs.nodes.ingest_node import ingest_node
from graphs.nodes.summary_node import summary_node
from graphs.nodes.concept_extract_node import concept_extract_node
from graphs.nodes.index_update_node import index_update_node
from graphs.nodes.qa_node import qa_node
from graphs.nodes.health_check_node import health_check_node

# 条件判断函数：根据模式决定流程
def route_by_mode(state: GlobalState) -> str:
    """
    title: 根据模式路由
    desc: 根据工作流模式（ingest/qa/health_check）决定执行哪个流程
    """
    mode = state.mode if hasattr(state, 'mode') else "ingest"
    
    if mode == "qa":
        return "qa"
    elif mode == "health_check":
        return "health_check"
    else:
        return "ingest"

# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加所有节点
builder.add_node("ingest", ingest_node)
builder.add_node("summary", summary_node, metadata={"type": "agent", "llm_cfg": "config/summary_llm_cfg.json"})
builder.add_node("concept_extract", concept_extract_node, metadata={"type": "agent", "llm_cfg": "config/concept_extract_llm_cfg.json"})
builder.add_node("index_update", index_update_node)
builder.add_node("qa", qa_node, metadata={"type": "agent", "llm_cfg": "config/qa_llm_cfg.json"})
builder.add_node("health_check", health_check_node, metadata={"type": "agent", "llm_cfg": "config/health_check_llm_cfg.json"})

# 设置入口点
builder.set_entry_point("ingest")

# 添加条件分支（从ingest节点路由）
# 注意：对于ingest模式，ingest节点会成功执行，然后继续summary
# 对于qa和health_check模式，ingest节点会返回success但不需要继续处理
builder.add_conditional_edges(
    source="ingest",
    path=route_by_mode,
    path_map={
        "ingest": "summary",
        "qa": "qa",
        "health_check": "health_check"
    }
)

# 摄取流程：ingest → summary → concept_extract → index_update
builder.add_edge("summary", "concept_extract")
builder.add_edge("concept_extract", "index_update")
builder.add_edge("index_update", END)

# 问答流程：qa → END
builder.add_edge("qa", END)

# 健康检查流程：health_check → END
builder.add_edge("health_check", END)

# 编译图
main_graph = builder.compile()
