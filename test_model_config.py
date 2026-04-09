#!/usr/bin/env python3
"""
模型配置测试脚本
用于验证模型配置是否正确
"""

import os
import json
import requests
import sys
from pathlib import Path

# 配置文件路径
CONFIG_FILES = [
    "config/summary_llm_cfg.json",
    "config/concept_extract_llm_cfg.json",
    "config/qa_llm_cfg.json",
    "config/health_check_llm_cfg.json",
]

ENV_FILE = ".env"


def load_env():
    """加载环境变量"""
    env_vars = {}
    env_path = Path(ENV_FILE)

    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    else:
        print(f"⚠️  未找到 .env 文件")
        return None

    return env_vars


def load_config(config_file):
    """加载配置文件"""
    config_path = Path(config_file)
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_file}")
        return None

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_config_files():
    """测试配置文件"""
    print("=" * 60)
    print("测试 1: 配置文件")
    print("=" * 60)

    model_ids = set()
    all_ok = True

    for config_file in CONFIG_FILES:
        config = load_config(config_file)
        if config:
            model_config = config.get("config", {})
            model_id = model_config.get("model", "")

            if model_id:
                model_ids.add(model_id)
                print(f"✅ {config_file}")
                print(f"   模型: {model_id}")
            else:
                print(f"❌ {config_file} - 未找到模型配置")
                all_ok = False
        else:
            all_ok = False

    print()
    if model_ids:
        print(f"📋 发现 {len(model_ids)} 个不同的模型:")
        for model_id in model_ids:
            print(f"   - {model_id}")
    else:
        print("⚠️  未找到任何模型配置")

    return all_ok


def test_env_file():
    """测试环境变量文件"""
    print("\n" + "=" * 60)
    print("测试 2: 环境变量文件")
    print("=" * 60)

    env_vars = load_env()

    if env_vars is None:
        return False

    required_keys = [
        "MODEL_TYPE",
        "MODEL_ID",
    ]

    all_ok = True
    for key in required_keys:
        if key in env_vars:
            value = env_vars[key]
            if key == "API_KEY":
                # 隐藏 API Key
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"✅ {key}: {masked_value}")
            else:
                print(f"✅ {key}: {value}")
        else:
            print(f"❌ {key}: 未配置")
            all_ok = False

    # 检查 API Key
    if "OPENAI_API_KEY" in env_vars or "COZE_API_KEY" in env_vars:
        api_key = env_vars.get("OPENAI_API_KEY") or env_vars.get("COZE_API_KEY")
        if api_key and api_key != "your-api-key-here":
            print("✅ API Key: 已配置")
        else:
            print("❌ API Key: 未配置或使用默认值")
            all_ok = False
    else:
        print("⚠️  未找到 API Key 配置")

    return all_ok


def test_model_consistency():
    """测试模型配置一致性"""
    print("\n" + "=" * 60)
    print("测试 3: 模型配置一致性")
    print("=" * 60)

    env_vars = load_env()
    if env_vars is None:
        return False

    env_model_id = env_vars.get("MODEL_ID", "")
    if not env_model_id:
        print("⚠️  .env 文件中未配置 MODEL_ID")
        return False

    print(f"📝 .env 中的模型 ID: {env_model_id}")

    config_models = []
    for config_file in CONFIG_FILES:
        config = load_config(config_file)
        if config:
            model_id = config.get("config", {}).get("model", "")
            if model_id:
                config_models.append((config_file, model_id))

    all_consistent = True
    for config_file, model_id in config_models:
        if model_id == env_model_id:
            print(f"✅ {Path(config_file).name}: 一致 ({model_id})")
        else:
            print(f"⚠️  {Path(config_file).name}: 不一致 ({model_id})")
            all_consistent = False

    if all_consistent:
        print("\n✅ 所有配置文件模型 ID 一致")
    else:
        print("\n⚠️  配置文件模型 ID 不一致，建议统一")

    return all_consistent


def test_api_connection():
    """测试 API 连接"""
    print("\n" + "=" * 60)
    print("测试 4: API 连接（可选）")
    print("=" * 60)

    # 检查服务是否运行
    server_url = "http://localhost:5000/health"

    try:
        response = requests.get(server_url, timeout=5)
        if response.status_code == 200:
            print(f"✅ 服务运行中: {server_url}")
            return True
        else:
            print(f"⚠️  服务未正常响应: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"⚠️  无法连接到服务: {server_url}")
        print("   请先启动服务: python src/main.py -m http -p 5000")
        return False
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False


def print_summary(results):
    """打印测试总结"""
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    test_names = [
        "配置文件",
        "环境变量文件",
        "模型配置一致性",
        "API 连接",
    ]

    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")

    passed = sum(results)
    total = len(results)

    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！模型配置正确。")
        print("\n下一步:")
        print("  1. 启动服务: python src/main.py -m http -p 5000")
        print("  2. 测试功能: python client.py qa \"测试问题\"")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查配置。")
        print("\n快速修复:")
        print("  1. 运行配置脚本: ./configure_model.sh <model_type>")
        print("  2. 查看文档: MODEL_CONFIG.md")
        return 1


def main():
    print("🧪 模型配置测试工具")
    print("=" * 60)
    print()

    results = []

    # 运行测试
    results.append(test_config_files())
    results.append(test_env_file())
    results.append(test_model_consistency())
    results.append(test_api_connection())

    # 打印总结
    return print_summary(results)


if __name__ == "__main__":
    sys.exit(main())
