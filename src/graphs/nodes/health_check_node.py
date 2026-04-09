import os
import datetime
import json
import glob
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import HealthCheckInput, HealthCheckOutput

def health_check_node(state: HealthCheckInput, config: RunnableConfig, runtime: Runtime[Context]) -> HealthCheckOutput:
    """
    title: 健康检查
    desc: 检查知识库的一致性、完整性和孤岛问题
    integrations: 大语言模型
    """
    ctx = runtime.context
    
    try:
        workspace = os.getenv("COZE_WORKSPACE_PATH", ".")
        
        # 收集概念文件
        concepts_dir = os.path.join(workspace, "assets/knowledge_base/wiki/concepts")
        concepts_data = []
        
        if os.path.exists(concepts_dir):
            for file_path in glob.glob(os.path.join(concepts_dir, "*.md")):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        concepts_data.append({
                            "file": os.path.basename(file_path),
                            "content": content
                        })
                except:
                    pass
        
        # 构建上下文
        context = "\n\n---\n\n".join([
            f"## {concept['file']}\n{concept['content']}"
            for concept in concepts_data
        ])
        
        # 读取LLM配置
        cfg_file = os.path.join(workspace, config['metadata']['llm_cfg'])
        with open(cfg_file, 'r', encoding='utf-8') as f:
            llm_cfg = json.load(f)
        
        model_config = llm_cfg.get("config", {})
        system_prompt = llm_cfg.get("sp", "")
        user_prompt_template = llm_cfg.get("up", "")
        
        # 根据模式选择检查类型（使用health_check_mode字段）
        check_mode = state.health_check_mode
        check_types = []
        if check_mode == "full":
            check_types = ["一致性", "完整性", "孤岛"]
        elif check_mode == "consistency":
            check_types = ["一致性"]
        elif check_mode == "completeness":
            check_types = ["完整性"]
        elif check_mode == "orphan":
            check_types = ["孤岛"]
        
        # 渲染用户提示词
        user_prompt = user_prompt_template.replace("{{context}}", context[:10000])
        user_prompt = user_prompt.replace("{{check_types}}", ", ".join(check_types))
        
        # 创建LLM客户端
        llm_client = LLMClient(ctx=ctx)
        
        # 调用LLM生成健康检查报告
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = llm_client.invoke(
            messages=messages,
            model=model_config.get("model", "doubao-seed-1-8-251228"),
            temperature=model_config.get("temperature", 0.3),
            max_completion_tokens=model_config.get("max_completion_tokens", 6000)
        )
        
        # 提取响应内容
        if isinstance(response.content, str):
            health_report = response.content
        elif isinstance(response.content, list):
            health_report = " ".join(item.get("text", "") for item in response.content if isinstance(item, dict))
        else:
            health_report = str(response.content)
        
        # 生成报告文件路径
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"health_check_{check_mode}_{timestamp}.md"
        report_dir = os.path.join(workspace, "assets/knowledge_base/outputs/health")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, report_filename)
        
        # 保存健康检查报告
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# 知识库健康检查报告\n\n")
            f.write(f"**检查时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**检查类型**: {check_mode}\n\n")
            f.write("---\n\n")
            f.write(health_report)
            f.write("\n\n---\n\n")
            f.write(f"**检查的文件数量**: {len(concepts_data)}\n")
        
        return HealthCheckOutput(
            health_report=health_report,
            health_report_path=report_path,
            success=True
        )
        
    except Exception as e:
        return HealthCheckOutput(
            health_report=f"健康检查失败: {str(e)}",
            health_report_path="",
            success=False
        )
