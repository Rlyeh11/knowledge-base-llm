import os
from typing import List, Dict, Optional, Any, Literal
from pydantic import BaseModel, Field
from utils.file.file import File

# ============== 全局状态 ==============
class GlobalState(BaseModel):
    """知识库工作流的全局状态"""
    # 工作流模式
    mode: Literal["ingest", "qa", "health_check"] = Field(default="ingest", description="工作流模式")
    health_check_mode: Literal["full", "consistency", "completeness", "orphan"] = Field(default="full", description="健康检查子模式")

    # 摄取阶段
    content: str = Field(default="", description="要摄取的内容（markdown/html/纯文本）")
    content_type: Literal["markdown", "html", "text"] = Field(default="markdown", description="内容类型")
    raw_file_path: str = Field(default="", description="原始文件保存路径")
    
    # 摘要阶段
    summary_content: str = Field(default="", description="生成的摘要内容")
    summary_file_path: str = Field(default="", description="摘要文件保存路径")
    
    # 概念抽取阶段
    concepts: List[Dict[str, Any]] = Field(default=[], description="抽取的概念列表")
    concept_files: List[str] = Field(default=[], description="概念文件路径列表")
    
    # 索引更新阶段
    sources_index_updated: bool = Field(default=False, description="来源索引是否已更新")
    concepts_index_updated: bool = Field(default=False, description="概念索引是否已更新")
    
    # 问答阶段
    question: str = Field(default="", description="用户问题")
    answer: str = Field(default="", description="生成的答案")
    qa_file_path: str = Field(default="", description="问答文件保存路径")
    qa_sources: List[str] = Field(default=[], description="问题涉及的来源文件")
    
    # 健康检查阶段
    health_report: str = Field(default="", description="健康检查报告")
    health_report_path: str = Field(default="", description="健康检查报告文件路径")
    
    # 通用状态
    error_message: str = Field(default="", description="错误信息")
    success: bool = Field(default=False, description="操作是否成功")

# ============== 工作流输入输出 ==============
class GraphInput(BaseModel):
    """工作流输入"""
    # 摄取模式
    content: Optional[str] = Field(default=None, description="要摄取的内容（markdown/html/纯文本）")
    content_type: Optional[Literal["markdown", "html", "text"]] = Field(default="markdown", description="内容类型")
    title: Optional[str] = Field(default=None, description="文档标题（可选）")

    # 问答模式
    question: Optional[str] = Field(default=None, description="用户问题")

    # 健康检查模式
    mode: Literal["ingest", "qa", "health_check"] = Field(default="ingest", description="工作流模式")

    # 健康检查子模式
    health_check_mode: Optional[Literal["full", "consistency", "completeness", "orphan"]] = Field(default="full", description="健康检查子模式")

class GraphOutput(BaseModel):
    """工作流输出"""
    success: bool = Field(default=False, description="操作是否成功")
    message: str = Field(default="", description="返回消息")
    output_file: str = Field(default="", description="输出文件路径")

# ============== 摄取节点 ==============
class IngestInput(BaseModel):
    """摄取节点输入"""
    content: str = Field(..., description="要摄取的内容（markdown/html/纯文本）")
    content_type: Literal["markdown", "html", "text"] = Field(default="markdown", description="内容类型")
    title: Optional[str] = Field(default=None, description="文档标题（可选）")

class IngestOutput(BaseModel):
    """摄取节点输出"""
    raw_file_path: str = Field(..., description="原始文件保存路径")
    title: str = Field(..., description="文档标题")
    success: bool = Field(..., description="操作是否成功")
    error_message: str = Field(default="", description="错误信息")

# ============== 摘要生成节点 ==============
class SummaryInput(BaseModel):
    """摘要生成节点输入"""
    raw_file_path: str = Field(..., description="原始文件路径")

class SummaryOutput(BaseModel):
    """摘要生成节点输出"""
    summary_content: str = Field(..., description="生成的摘要内容")
    summary_file_path: str = Field(..., description="摘要文件保存路径")
    success: bool = Field(..., description="操作是否成功")

# ============== 概念抽取节点 ==============
class ConceptExtractInput(BaseModel):
    """概念抽取节点输入"""
    summary_file_path: str = Field(..., description="摘要文件路径")

class ConceptExtractOutput(BaseModel):
    """概念抽取节点输出"""
    concepts: List[Dict[str, Any]] = Field(..., description="抽取的概念列表")
    concept_files: List[str] = Field(..., description="概念文件路径列表")
    success: bool = Field(..., description="操作是否成功")

# ============== 索引更新节点 ==============
class IndexUpdateInput(BaseModel):
    """索引更新节点输入"""
    raw_file_path: str = Field(..., description="原始文件路径")
    summary_file_path: str = Field(..., description="摘要文件路径")
    concepts: List[Dict[str, Any]] = Field(..., description="概念列表")

class IndexUpdateOutput(BaseModel):
    """索引更新节点输出"""
    sources_index_updated: bool = Field(..., description="来源索引是否已更新")
    concepts_index_updated: bool = Field(..., description="概念索引是否已更新")
    success: bool = Field(..., description="操作是否成功")

# ============== 问答沉淀节点 ==============
class QAInput(BaseModel):
    """问答沉淀节点输入"""
    question: str = Field(..., description="用户问题")

class QAOutput(BaseModel):
    """问答沉淀节点输出"""
    answer: str = Field(..., description="生成的答案")
    qa_file_path: str = Field(..., description="问答文件保存路径")
    qa_sources: List[str] = Field(..., description="问题涉及的来源文件")
    success: bool = Field(..., description="操作是否成功")

# ============== 健康检查节点 ==============
class HealthCheckInput(BaseModel):
    """健康检查节点输入"""
    health_check_mode: Literal["full", "consistency", "completeness", "orphan"] = Field(default="full", description="健康检查子模式")

class HealthCheckOutput(BaseModel):
    """健康检查节点输出"""
    health_report: str = Field(..., description="健康检查报告")
    health_report_path: str = Field(..., description="健康检查报告文件路径")
    success: bool = Field(..., description="操作是否成功")
