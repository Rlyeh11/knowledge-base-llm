#!/usr/bin/env python3
"""
问答系统性能测试脚本
测试问答系统的性能指标：响应时间、文档使用数、上下文长度等
"""
import os
import sys
import time
import json
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from dotenv import load_dotenv
    load_dotenv(str(project_root / ".env"))
except ImportError:
    pass


def test_qa_performance():
    """测试问答性能"""
    print("=" * 60)
    print("问答系统性能测试")
    print("=" * 60)

    # 检查服务是否运行
    import requests
    base_url = f"http://{os.getenv('HOST', 'localhost')}:{os.getenv('PORT', '5000')}"

    print("\n1. 检查服务状态...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 服务正常运行")
        else:
            print(f"❌ 服务状态异常: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 无法连接到服务: {e}")
        print("请先启动服务: make run")
        return

    # 读取配置
    print("\n2. 读取配置...")
    config_path = project_root / "config/qa_limit_cfg.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"✅ 配置加载成功")
        print(f"   - 最大文档数: {config.get('max_docs', 'N/A')}")
        print(f"   - 单文档字符数: {config.get('max_doc_chars', 'N/A')}")
        print(f"   - 总上下文长度: {config.get('max_context_chars', 'N/A')}")
        print(f"   - 智能检索: {config.get('enable_smart_retrieval', 'N/A')}")
    else:
        print("⚠️  配置文件不存在，使用默认值")

    # 统计知识库文档数量
    print("\n3. 统计知识库文档...")
    wiki_dirs = [
        project_root / "assets/knowledge_base/wiki/summaries",
        project_root / "assets/knowledge_base/wiki/concepts"
    ]
    total_docs = 0
    for wiki_dir in wiki_dirs:
        if wiki_dir.exists():
            doc_count = len(list(wiki_dir.glob("*.md")))
            total_docs += doc_count
            print(f"   - {wiki_dir.name}: {doc_count} 个文档")
    print(f"✅ 总文档数: {total_docs}")

    # 测试问答
    print("\n4. 测试问答性能...")

    test_questions = [
        "什么是知识库系统？",
        "如何使用这个系统？",
        "系统支持哪些功能？",
        "知识库如何组织？"
    ]

    results = []

    for i, question in enumerate(test_questions, 1):
        print(f"\n   测试 {i}/{len(test_questions)}: {question}")
        print(f"   " + "-" * 50)

        start_time = time.time()

        try:
            response = requests.post(
                f"{base_url}/api/qa",
                json={"question": question},
                timeout=30
            )
            end_time = time.time()

            if response.status_code == 200:
                data = response.json()
                response_time = end_time - start_time

                print(f"   ✅ 成功")
                print(f"   - 响应时间: {response_time:.2f} 秒")
                print(f"   - 答案长度: {len(data.get('answer', ''))} 字符")
                print(f"   - 来源文档数: {len(data.get('qa_sources', []))}")

                results.append({
                    "question": question,
                    "success": True,
                    "response_time": response_time,
                    "answer_length": len(data.get('answer', '')),
                    "sources_count": len(data.get('qa_sources', []))
                })

                # 显示部分答案
                answer_preview = data.get('answer', '')[:100]
                if len(answer_preview) < len(data.get('answer', '')):
                    answer_preview += "..."
                print(f"   - 答案预览: {answer_preview}")

            else:
                print(f"   ❌ 失败: {response.status_code}")
                print(f"   - 错误信息: {response.text}")

                results.append({
                    "question": question,
                    "success": False,
                    "error": response.text
                })

        except requests.exceptions.Timeout:
            print(f"   ❌ 超时 (> 30秒)")
            results.append({
                "question": question,
                "success": False,
                "error": "Timeout"
            })

        except Exception as e:
            print(f"   ❌ 异常: {e}")
            results.append({
                "question": question,
                "success": False,
                "error": str(e)
            })

    # 总结报告
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)

    print(f"\n成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")

    if success_count > 0:
        successful_results = [r for r in results if r['success']]
        avg_response_time = sum(r['response_time'] for r in successful_results) / len(successful_results)
        avg_sources_count = sum(r['sources_count'] for r in successful_results) / len(successful_results)

        print(f"平均响应时间: {avg_response_time:.2f} 秒")
        print(f"平均文档使用数: {avg_sources_count:.1f}")

        # 性能评估
        print("\n性能评估:")
        if avg_response_time < 5:
            print("✅ 响应时间优秀")
        elif avg_response_time < 10:
            print("⚠️  响应时间一般")
        else:
            print("❌ 响应时间较慢，建议优化")

        if avg_sources_count >= config.get('max_docs', 10) * 0.8:
            print("✅ 文档利用率高")
        elif avg_sources_count >= config.get('max_docs', 10) * 0.5:
            print("⚠️  文档利用率一般")
        else:
            print("❌ 文档利用率低，建议检查智能检索配置")

    # 保存结果
    print("\n5. 保存测试结果...")
    results_file = project_root / "tests/qa_performance_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "config": config if config_path.exists() else {},
            "total_docs": total_docs,
            "results": results
        }, f, indent=2)
    print(f"✅ 结果已保存到: {results_file}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_qa_performance()
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
