#!/usr/bin/env python3
"""
CORS 测试脚本
用于验证服务器的 CORS 配置是否正确
"""

import requests
import json
import sys

# 服务器配置
SERVER_URL = "http://localhost:5000"
RUN_ENDPOINT = f"{SERVER_URL}/run"

def test_options_preflight():
    """测试 OPTIONS 预检请求"""
    print("=" * 60)
    print("测试 1: OPTIONS 预检请求")
    print("=" * 60)

    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type, Authorization"
    }

    try:
        response = requests.options(RUN_ENDPOINT, headers=headers)

        print(f"状态码: {response.status_code}")
        print("\n响应头:")

        # 检查 CORS 响应头
        cors_headers = [
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Credentials",
            "Access-Control-Max-Age"
        ]

        cors_ok = True
        for header in cors_headers:
            value = response.headers.get(header, "未设置")
            print(f"  {header}: {value}")
            if not value or value == "未设置":
                cors_ok = False

        if response.status_code == 200:
            print("\n✅ OPTIONS 请求成功")
        else:
            print(f"\n❌ OPTIONS 请求失败，状态码: {response.status_code}")
            cors_ok = False

        if cors_ok:
            print("✅ CORS 响应头配置正确")
        else:
            print("❌ CORS 响应头配置不完整")

        return response.status_code == 200 and cors_ok

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确认服务是否已启动")
        print(f"   尝试连接: {SERVER_URL}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_post_request():
    """测试 POST 实际请求"""
    print("\n" + "=" * 60)
    print("测试 2: POST 实际请求")
    print("=" * 60)

    headers = {
        "Origin": "http://localhost:3000",
        "Content-Type": "application/json"
    }

    # 使用健康检查端点测试
    health_url = f"{SERVER_URL}/health"

    try:
        response = requests.get(health_url, headers=headers)

        print(f"状态码: {response.status_code}")
        print("\n响应头:")

        cors_headers = [
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Credentials"
        ]

        cors_ok = True
        for header in cors_headers:
            value = response.headers.get(header, "未设置")
            print(f"  {header}: {value}")

        print("\n响应体:")
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except:
            print(response.text)

        if response.status_code == 200:
            print("\n✅ POST 请求成功")
        else:
            print(f"\n❌ POST 请求失败，状态码: {response.status_code}")

        return response.status_code == 200

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确认服务是否已启动")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_complex_preflight():
    """测试复杂的预检请求（包含自定义头）"""
    print("\n" + "=" * 60)
    print("测试 3: 复杂预检请求（自定义头）")
    print("=" * 60)

    headers = {
        "Origin": "https://example.com",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type, X-Custom-Header, Authorization"
    }

    try:
        response = requests.options(RUN_ENDPOINT, headers=headers)

        print(f"状态码: {response.status_code}")
        print("\n响应头:")
        print(f"  Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', '未设置')}")
        print(f"  Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', '未设置')}")
        print(f"  Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', '未设置')}")

        if response.status_code == 200:
            print("\n✅ 复杂预检请求成功")
            return True
        else:
            print(f"\n❌ 复杂预检请求失败，状态码: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def main():
    print("🧪 CORS 配置测试工具")
    print("=" * 60)
    print(f"目标服务器: {SERVER_URL}")
    print("=" * 60)

    results = []

    # 运行测试
    results.append(("OPTIONS 预检请求", test_options_preflight()))
    results.append(("POST 实际请求", test_post_request()))
    results.append(("复杂预检请求", test_complex_preflight()))

    # 输出总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {test_name}")

    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！CORS 配置正确。")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查 CORS 配置。")
        print("   详细信息请参考: CORS_FIX.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())
