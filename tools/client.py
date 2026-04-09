#!/usr/bin/env python3
"""
知识库编译系统 - 简易客户端

使用方法：
    python client.py ingest "你的内容" --title "标题" --type markdown
    python client.py ask "你的问题"
    python client.py health --mode full
"""

import argparse
import requests
import sys
import json


class KnowledgeBaseClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def ingest(self, content, title="", content_type="markdown"):
        """摄取新内容到知识库"""
        payload = {
            "content": content,
            "content_type": content_type,
            "mode": "ingest"
        }
        if title:
            payload["title"] = title

        return self._call_api("/run", payload)

    def ask(self, question):
        """基于知识库回答问题"""
        payload = {
            "question": question,
            "mode": "qa"
        }
        return self._call_api("/run", payload)

    def health_check(self, mode="full"):
        """执行健康检查"""
        payload = {
            "mode": "health_check",
            "health_check_mode": mode
        }
        return self._call_api("/run", payload)

    def _call_api(self, endpoint, payload):
        """调用 API"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ API 调用失败: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="知识库编译系统客户端")
    parser.add_argument("action", choices=["ingest", "ask", "health"], help="操作类型")
    parser.add_argument("--url", default="http://localhost:5000", help="API 服务地址")
    parser.add_argument("--content", help="要摄取的内容")
    parser.add_argument("--title", help="文档标题")
    parser.add_argument("--type", default="markdown", choices=["markdown", "html", "text"], help="内容类型")
    parser.add_argument("--question", help="要问的问题")
    parser.add_argument("--mode", default="full", choices=["full", "consistency", "completeness", "orphan"], help="健康检查模式")

    args = parser.parse_args()

    client = KnowledgeBaseClient(args.url)

    if args.action == "ingest":
        if not args.content:
            print("❌ 请提供要摄取的内容 (--content)")
            sys.exit(1)

        print("📥 正在摄取内容...")
        result = client.ingest(args.content, args.title, args.type)
        print(f"✅ 摄取成功！")
        print(f"📄 文件路径: {result.get('raw_file_path', 'N/A')}")

    elif args.action == "ask":
        if not args.question:
            print("❌ 请提供要问的问题 (--question)")
            sys.exit(1)

        print("❓ 正在查询知识库...")
        result = client.ask(args.question)
        print(f"💡 答案: {result.get('answer', 'N/A')}")
        if result.get('qa_sources'):
            print(f"\n📚 来源:")
            for source in result['qa_sources']:
                print(f"   - {source}")

    elif args.action == "health":
        print("🏥 正在执行健康检查...")
        result = client.health_check(args.mode)
        print(f"✅ 检查完成！")
        print(f"📄 报告路径: {result.get('health_report_path', 'N/A')}")

    # 打印完整结果（如果需要）
    print(f"\n📊 完整结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
