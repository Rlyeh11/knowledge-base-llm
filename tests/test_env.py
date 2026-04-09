#!/usr/bin/env python3
"""
测试环境变量配置
验证必需的环境变量是否正确配置
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ python-dotenv 未安装，请运行: pip install python-dotenv")
    sys.exit(1)


def check_env_vars():
    """检查环境变量配置"""
    # 加载 .env 文件
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(str(env_file))
        print(f"✅ 已加载环境变量文件: {env_file}")
    else:
        print(f"⚠️  未找到 .env 文件: {env_file}")
        print(f"💡 请运行: cp .env.example .env")

    print("\n" + "="*60)
    print("环境变量检查")
    print("="*60)

    # 必需的环境变量
    required_vars = {
        "MODEL_TYPE": "模型类型 (openai, coze)",
        "MODEL_ID": "模型 ID (如 deepseek-chat)",
    }

    # 条件必需的环境变量
    conditional_vars = {
        "OPENAI_API_KEY": {"condition": lambda: os.getenv("MODEL_TYPE") == "openai", "desc": "OpenAI API Key"},
        "COZE_API_KEY": {"condition": lambda: os.getenv("MODEL_TYPE") == "coze", "desc": "Coze API Key"},
    }

    # 可选的环境变量
    optional_vars = {
        "OPENAI_BASE_URL": "API Base URL",
        "LOG_LEVEL": "日志级别",
        "MAX_WORKERS": "最大工作进程数",
        "PORT": "服务端口",
        "STORAGE_TYPE": "存储类型",
    }

    # 检查必需变量
    print("\n【必需配置】")
    all_required_ok = True
    for var_name, desc in required_vars.items():
        value = os.getenv(var_name)
        if value:
            print(f"✅ {var_name}: {value}")
        else:
            print(f"❌ {var_name}: 未设置 ({desc})")
            all_required_ok = False

    # 检查条件必需变量
    print("\n【条件必需配置】")
    all_conditional_ok = True
    for var_name, info in conditional_vars.items():
        if info["condition"]():
            value = os.getenv(var_name)
            if value:
                print(f"✅ {var_name}: {'*' * (len(value) - 4)}{value[-4:]}")
            else:
                print(f"❌ {var_name}: 未设置 ({info['desc']})")
                all_conditional_ok = False
        else:
            print(f"⏭️  {var_name}: 跳过 (MODEL_TYPE={os.getenv('MODEL_TYPE')})")

    # 检查可选变量
    print("\n【可选配置】")
    for var_name, desc in optional_vars.items():
        value = os.getenv(var_name)
        if value:
            print(f"✅ {var_name}: {value} ({desc})")
        else:
            print(f"⚪ {var_name}: 未设置 ({desc})")

    # 总结
    print("\n" + "="*60)
    if all_required_ok and all_conditional_ok:
        print("✅ 环境变量配置正常！")
        print("\n下一步:")
        print("  1. 运行模型测试: make model-test")
        print("  2. 启动服务:     make run")
        return 0
    else:
        print("❌ 环境变量配置不完整！")
        print("\n请检查:")
        print("  1. 是否已创建 .env 文件")
        print("  2. .env 文件中的变量是否正确填写")
        print("\n快速配置:")
        print("  cp .env.example .env")
        print("  nano .env  # 编辑文件")
        return 1


if __name__ == "__main__":
    sys.exit(check_env_vars())
