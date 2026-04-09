import os
import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import IngestInput, IngestOutput

def ingest_node(state: IngestInput, config: RunnableConfig, runtime: Runtime[Context]) -> IngestOutput:
    """
    title: 摄取原始资料
    desc: 从用户输入的markdown/html/纯文本内容保存到raw目录
    integrations:
    """
    ctx = runtime.context

    try:
        # 获取内容和类型
        content = state.content
        content_type = state.content_type

        # 生成或提取标题
        title = state.title
        if not title:
            # 尝试从内容中提取标题
            lines = content.strip().split('\n')
            for line in lines:
                line = line.strip()
                # 查找markdown标题或第一行非空文本
                if line.startswith('#'):
                    title = line.lstrip('#').strip()
                    break
                if line:
                    title = line[:50]  # 使用前50个字符作为标题
                    break

            if not title:
                title = f"文档_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # 生成文件名（使用时间戳和标题）
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_', '.')).strip()
        safe_title = safe_title.replace(' ', '_')[:50]  # 限制长度

        # 根据内容类型确定文件扩展名
        if content_type == "markdown":
            file_ext = ".md"
        elif content_type == "html":
            file_ext = ".html"
        else:  # text
            file_ext = ".txt"

        filename = f"{timestamp}_{safe_title}{file_ext}"

        # 确保raw目录存在
        raw_dir = os.path.join(os.getenv("COZE_WORKSPACE_PATH", "."), "assets/knowledge_base/raw/articles")
        os.makedirs(raw_dir, exist_ok=True)

        # 保存文件
        file_path = os.path.join(raw_dir, filename)

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            if content_type == "markdown":
                # 对于markdown，添加标题元数据
                f.write(f"# {title}\n\n")
                f.write(f"**内容类型**: {content_type}\n")
                f.write(f"**摄取时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(content)
            elif content_type == "html":
                # 对于html，保持原始格式
                f.write(f"<!-- 标题: {title} -->\n")
                f.write(f"<!-- 内容类型: {content_type} -->\n")
                f.write(f"<!-- 摄取时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->\n\n")
                f.write(content)
            else:  # text
                # 对于纯文本，添加标题行
                f.write(f"标题: {title}\n")
                f.write(f"内容类型: {content_type}\n")
                f.write(f"摄取时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(content)

        return IngestOutput(
            raw_file_path=file_path,
            title=title,
            success=True
        )

    except Exception as e:
        return IngestOutput(
            raw_file_path="",
            title="",
            success=False,
            error_message=f"摄取失败: {str(e)}"
        )
