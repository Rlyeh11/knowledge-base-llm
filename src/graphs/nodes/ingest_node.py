import os
import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk.fetch import FetchClient
from graphs.state import IngestInput, IngestOutput

def ingest_node(state: IngestInput, config: RunnableConfig, runtime: Runtime[Context]) -> IngestOutput:
    """
    title: 摄取原始资料
    desc: 从URL获取内容并保存为Markdown文件到raw目录
    integrations: fetch-url
    """
    ctx = runtime.context
    
    try:
        # 创建FetchClient
        fetch_client = FetchClient(ctx=ctx)
        
        # 获取URL内容
        response = fetch_client.fetch(url=state.url)
        
        if response.status_code != 0:
            return IngestOutput(
                raw_file_path="",
                title="",
                success=False,
                error_message=f"获取URL失败: {response.status_message}"
            )
        
        # 提取文本内容
        text_content = "\n".join(
            item.text for item in response.content if item.type == "text"
        )
        
        # 生成文件名（使用时间戳和标题）
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in response.title if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')[:50]  # 限制长度
        filename = f"{timestamp}_{safe_title}.md"
        
        # 确保raw目录存在
        raw_dir = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "."), "assets/knowledge_base/raw/articles")
        os.makedirs(raw_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(raw_dir, filename)
        
        # 写入Markdown格式
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {response.title}\n\n")
            f.write(f"**来源URL**: {state.url}\n\n")
            if response.publish_time:
                f.write(f"**发布时间**: {response.publish_time}\n\n")
            f.write("---\n\n")
            f.write(text_content)
        
        return IngestOutput(
            raw_file_path=file_path,
            title=response.title,
            success=True
        )
        
    except Exception as e:
        return IngestOutput(
            raw_file_path="",
            title="",
            success=False,
            error_message=f"摄取失败: {str(e)}"
        )
