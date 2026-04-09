"""
RAG Integration Service
集成 LightRAG 框架，提供统一的 RAG 服务接口
"""
import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from pathlib import Path


class RAGIntegrationService:
    """LightRAG 集成服务"""

    def __init__(self, config_path: str = "config/lightrag_config.json"):
        """
        初始化 RAG 服务

        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.rag = None
        self._initialize_rag()

    def _load_config(self, config_path: str) -> dict:
        """
        加载配置

        Args:
            config_path: 配置文件路径

        Returns:
            配置字典
        """
        workspace = os.getenv("COZE_WORKSPACE_PATH", ".")
        full_path = os.path.join(workspace, config_path)

        default_config = {
            "embedding": {
                "model_name": "BAAI/bge-small-zh-v1.5",
                "device": "cpu",
                "batch_size": 32
            },
            "vector_store": {
                "type": "faiss",
                "dimension": 512,
                "metric": "cosine"
            },
            "retrieval": {
                "top_k": 10,
                "min_similarity": 0.5
            }
        }

        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 合并配置
                    for key in default_config:
                        if key in loaded_config:
                            default_config[key].update(loaded_config[key])
            except Exception as e:
                print(f"Warning: Failed to load config file, using defaults: {e}")

        return default_config

    def _initialize_rag(self):
        """初始化 LightRAG"""
        try:
            from lightrag import LightRAG
            from lightrag.llm import openai_complete_if_cache, openai_embedding
            from lightrag.utils import EmbeddingFunc

            workspace = os.getenv("COZE_WORKSPACE_PATH", ".")
            storage_path = os.path.join(workspace, "assets/knowledge_base/lrag_storage")

            # 确保存储目录存在
            os.makedirs(storage_path, exist_ok=True)

            # 配置嵌入模型
            embedding_config = self.config.get("embedding", {})
            model_name = embedding_config.get("model_name", "BAAI/bge-small-zh-v1.5")
            device = embedding_config.get("device", "cpu")

            # 定义嵌入函数
            async def embedding_func(texts: List[str]) -> List[List[float]]:
                from sentence_transformers import SentenceTransformer

                # 延迟加载模型
                if not hasattr(self, '_embedding_model'):
                    print(f"Loading embedding model: {model_name}")
                    self._embedding_model = SentenceTransformer(model_name, device=device)

                embeddings = self._embedding_model.encode(
                    texts,
                    normalize_embeddings=True,
                    show_progress_bar=False
                )
                return embeddings.tolist()

            # 配置 LLM
            llm_config = {
                "api_key": os.getenv("OPENAI_API_KEY", ""),
                "base_url": os.getenv("OPENAI_BASE_URL", ""),
                "model": os.getenv("MODEL_ID", "deepseek-chat")
            }

            # 初始化 LightRAG
            self.rag = LightRAG(
                working_dir=storage_path,
                llm_model_func=openai_complete_if_cache(
                    api_key=llm_config["api_key"],
                    base_url=llm_config["base_url"],
                    model=llm_config["model"]
                ),
                embedding_func=EmbeddingFunc(
                    embedding_func=embedding_func,
                    max_token_size=8192
                )
            )

            print(f"LightRAG initialized successfully. Storage path: {storage_path}")

        except Exception as e:
            print(f"Error initializing LightRAG: {e}")
            raise

    async def ingest_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        摄取文档

        Args:
            doc_id: 文档 ID
            content: 文档内容
            metadata: 元数据

        Returns:
            是否成功
        """
        try:
            # 添加文档元数据
            if metadata is None:
                metadata = {}

            metadata["doc_id"] = doc_id

            # 插入文档到 LightRAG
            await self.rag.ainsert(content, metadata=metadata)

            return True

        except Exception as e:
            print(f"Error ingesting document {doc_id}: {e}")
            return False

    async def ingest_documents_batch(
        self,
        documents: List[Dict[str, Any]]
    ) -> int:
        """
        批量摄取文档

        Args:
            documents: 文档列表，每个文档包含 doc_id, content, metadata

        Returns:
            成功的文档数量
        """
        success_count = 0

        for doc in documents:
            doc_id = doc.get("doc_id", "")
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})

            success = await self.ingest_document(doc_id, content, metadata)
            if success:
                success_count += 1

        return success_count

    async def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        检索相关文档

        Args:
            query: 查询文本
            top_k: 返回结果数量

        Returns:
            检索结果列表
        """
        try:
            top_k = top_k or self.config.get("retrieval", {}).get("top_k", 10)

            # 使用 LightRAG 的检索功能
            results = await self.rag.aretrieve(query, top_k=top_k)

            # 格式化结果
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "content": result.get("content", ""),
                    "metadata": result.get("metadata", {}),
                    "score": result.get("score", 0.0)
                })

            return formatted_results

        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []

    async def query(
        self,
        question: str,
        mode: str = "hybrid",
        param: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        查询并生成答案

        Args:
            question: 问题
            mode: 查询模式 (naive/local/global/hybrid)
            param: 查询参数

        Returns:
            答案
        """
        try:
            # 使用 LightRAG 的查询功能
            answer = await self.rag.aquery(
                question,
                mode=mode,
                param=param or {}
            )

            return answer

        except Exception as e:
            print(f"Error querying: {e}")
            return f"查询失败: {str(e)}"

    def get_stats(self) -> Dict[str, Any]:
        """
        获取统计信息

        Returns:
            统计信息字典
        """
        try:
            # LightRAG 不直接提供文档计数，我们返回配置信息
            stats = {
                "embedding_model": self.config.get("embedding", {}).get("model_name"),
                "vector_store": self.config.get("vector_store", {}).get("type"),
                "retrieval_top_k": self.config.get("retrieval", {}).get("top_k"),
                "min_similarity": self.config.get("retrieval", {}).get("min_similarity")
            }

            # 尝试获取存储目录信息
            workspace = os.getenv("COZE_WORKSPACE_PATH", ".")
            storage_path = os.path.join(workspace, "assets/knowledge_base/lrag_storage")

            if os.path.exists(storage_path):
                # 统计文件数量
                vdb_path = os.path.join(storage_path, "vdb")
                if os.path.exists(vdb_path):
                    stats["storage_exists"] = True
                    stats["storage_path"] = storage_path
                else:
                    stats["storage_exists"] = False
            else:
                stats["storage_exists"] = False

            return stats

        except Exception as e:
            print(f"Error getting stats: {e}")
            return {"error": str(e)}

    def check_health(self) -> Dict[str, Any]:
        """
        检查服务健康状态

        Returns:
            健康状态字典
        """
        health_status = {
            "status": "unknown",
            "rag_initialized": False,
            "model_loaded": False,
            "storage_ready": False
        }

        try:
            # 检查 RAG 是否初始化
            health_status["rag_initialized"] = self.rag is not None

            # 检查模型是否加载
            health_status["model_loaded"] = hasattr(self, '_embedding_model')

            # 检查存储是否就绪
            workspace = os.getenv("COZE_WORKSPACE_PATH", ".")
            storage_path = os.path.join(workspace, "assets/knowledge_base/lrag_storage")
            health_status["storage_ready"] = os.path.exists(storage_path)

            # 综合状态
            if all(health_status.values()):
                health_status["status"] = "healthy"
            elif health_status["rag_initialized"]:
                health_status["status"] = "ready"
            else:
                health_status["status"] = "unhealthy"

        except Exception as e:
            health_status["status"] = "error"
            health_status["error"] = str(e)

        return health_status
