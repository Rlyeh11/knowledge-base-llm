#!/usr/bin/env python3
"""
LightRAG 集成测试脚本
测试 RAGIntegrationService 的基本功能
"""
import os
import sys
import asyncio
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from dotenv import load_dotenv
    load_dotenv(str(project_root / ".env"))
except ImportError:
    pass


def test_rag_integration():
    """测试 RAG 集成服务"""
    print("=" * 60)
    print("LightRAG 集成测试")
    print("=" * 60)

    from src.services.rag_integration_service import RAGIntegrationService

    # 测试 1: 初始化服务
    print("\n1. 测试初始化服务...")
    try:
        rag_service = RAGIntegrationService()
        print("✅ 服务初始化成功")
    except Exception as e:
        print(f"❌ 服务初始化失败: {e}")
        return

    # 测试 2: 检查健康状态
    print("\n2. 检查服务健康状态...")
    try:
        health = rag_service.check_health()
        print(f"✅ 健康检查完成")
        print(f"   状态: {health['status']}")
        print(f"   RAG 已初始化: {health['rag_initialized']}")
        print(f"   模型已加载: {health['model_loaded']}")
        print(f"   存储就绪: {health['storage_ready']}")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return

    # 测试 3: 摄取测试文档
    print("\n3. 摄取测试文档...")
    test_documents = [
        {
            "doc_id": "test_doc_1",
            "content": """
# Python 编程语言

Python 是一门高级编程语言，由 Guido van Rossum 于 1991 年创建。

## 特点
- 简单易学
- 代码可读性强
- 丰富的标准库
- 跨平台

## 应用领域
- Web 开发
- 数据科学
- 人工智能
- 自动化
            """,
            "metadata": {
                "title": "Python介绍",
                "type": "tutorial",
                "language": "zh"
            }
        },
        {
            "doc_id": "test_doc_2",
            "content": """
# FastAPI 框架

FastAPI 是一个现代、快速（高性能）的 Web 框架，用于构建 API。

## 特点
- 快速：基于 Starlette 和 Pydantic
- 直观：易于使用
- 自动文档：自动生成交互式 API 文档
- 类型提示：支持 Python 类型提示

## 快速开始
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```
            """,
            "metadata": {
                "title": "FastAPI介绍",
                "type": "tutorial",
                "language": "zh"
            }
        }
    ]

    try:
        success_count = asyncio.run(
            rag_service.ingest_documents_batch(test_documents)
        )
        print(f"✅ 文档摄取完成")
        print(f"   成功: {success_count}/{len(test_documents)}")
    except Exception as e:
        print(f"❌ 文档摄取失败: {e}")
        return

    # 测试 4: 检索测试
    print("\n4. 测试检索功能...")
    test_queries = [
        "Python 是什么？",
        "FastAPI 有什么特点？",
        "如何使用 FastAPI？"
    ]

    for query in test_queries:
        try:
            results = asyncio.run(rag_service.retrieve(query, top_k=3))
            print(f"   ✅ 查询: {query}")
            print(f"   找到 {len(results)} 个相关文档")
            for i, result in enumerate(results[:2], 1):
                print(f"      {i}. {result['metadata'].get('title', 'unknown')} (score: {result.get('score', 0):.3f})")
        except Exception as e:
            print(f"   ❌ 检索失败: {e}")

    # 测试 5: 问答测试
    print("\n5. 测试问答功能...")
    test_questions = [
        "Python 是谁创建的？",
        "FastAPI 基于什么？",
        "Python 有哪些应用领域？"
    ]

    for question in test_questions:
        try:
            answer = asyncio.run(rag_service.query(question, mode="hybrid"))
            print(f"   ✅ 问题: {question}")
            print(f"   答案: {answer[:100]}...")
        except Exception as e:
            print(f"   ❌ 问答失败: {e}")

    # 测试 6: 获取统计信息
    print("\n6. 获取统计信息...")
    try:
        stats = rag_service.get_stats()
        print("✅ 统计信息:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
    except Exception as e:
        print(f"❌ 获取统计信息失败: {e}")

    # 总结
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print("\n提示:")
    print("- 如果所有测试通过，说明 LightRAG 集成正常")
    print("- 可以开始使用 make qa 命令进行问答")
    print("- 查看详细文档: docs/RAG_PHASE1_LIGHTRAG_GUIDE.md")


if __name__ == "__main__":
    try:
        test_rag_integration()
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
