# 📁 项目目录整理方案

## 📊 当前根目录文件分析

### 文档文件（9个）
- AGENTS.md
- CORS_FIX.md
- CORS_QUICK_FIX.md
- DEPLOYMENT.md
- DOCKER.md
- FAQ.md
- INSTALL.md
- MODEL_CONFIG.md
- MODEL_QUICK_START.md
- README_KNOWLEDGE_BASE.md
- USAGE.md

### 脚本文件（6个）
- configure_model.sh
- configure_model.bat
- install.sh
- install.bat
- quickstart.sh
- quickstart.bat
- start.sh

### 测试工具（4个）
- test_cors.py
- test_cors.bat
- test_model_config.py
- test_model_config.bat

### 配置文件（6个）
- Dockerfile
- docker-compose.yml
- Makefile
- pyproject.toml
- requirements.txt
- requirements_core.txt
- uv.lock

### 应用文件（1个）
- client.py

## 🎯 整理目标

### 1. 创建目录结构
```
knowledge-base-system/
├── docs/                    # 所有文档
├── scripts/                 # 所有安装和配置脚本
├── tools/                   # 测试工具
├── assets/                  # 资源文件（已有）
├── config/                  # 配置文件（已有）
├── src/                     # 源代码（已有）
├── .venv/                   # 虚拟环境（已有）
├── scripts/                 # 原有脚本（已有）
└── README.md                # 主文档（保留在根目录）
```

### 2. 文件迁移计划

#### docs/ - 文档目录
```
docs/
├── AGENTS.md
├── CORS_FIX.md
├── CORS_QUICK_FIX.md
├── DEPLOYMENT.md
├── DOCKER.md
├── FAQ.md
├── INSTALL.md
├── MODEL_CONFIG.md
├── MODEL_QUICK_START.md
├── README_KNOWLEDGE_BASE.md
├── USAGE.md
└── index.md                 # 文档索引（新增）
```

#### scripts/ - 脚本目录
```
scripts/
├── install.sh
├── install.bat
├── configure_model.sh
├── configure_model.bat
├── quickstart.sh
├── quickstart.bat
└── start.sh
```

#### tools/ - 测试工具目录
```
tools/
├── test_cors.py
├── test_cors.bat
├── test_model_config.py
└── test_model_config.bat
```

### 3. 保留在根目录的文件
```
README.md                  # 主文档
Makefile                   # 构建工具
pyproject.toml            # 项目配置
requirements.txt          # 依赖列表
requirements_core.txt     # 核心依赖
Dockerfile                # Docker 配置
docker-compose.yml        # Docker Compose
.gitignore                # Git 忽略文件
.coze                     # Coze 配置
```

## 🔄 迁移步骤

### 步骤 1: 创建新目录
```bash
mkdir -p docs scripts tools
```

### 步骤 2: 移动文档文件
```bash
mv AGENTS.md docs/
mv CORS_FIX.md docs/
mv CORS_QUICK_FIX.md docs/
mv DEPLOYMENT.md docs/
mv DOCKER.md docs/
mv FAQ.md docs/
mv INSTALL.md docs/
mv MODEL_CONFIG.md docs/
mv MODEL_QUICK_START.md docs/
mv README_KNOWLEDGE_BASE.md docs/
mv USAGE.md docs/
```

### 步骤 3: 移动脚本文件
```bash
mv configure_model.sh scripts/
mv configure_model.bat scripts/
mv install.sh scripts/
mv install.bat scripts/
mv quickstart.sh scripts/
mv quickstart.bat scripts/
mv start.sh scripts/
```

### 步骤 4: 移动测试工具
```bash
mv test_cors.py tools/
mv test_cors.bat tools/
mv test_model_config.py tools/
mv test_model_config.bat tools/
```

### 步骤 5: 更新引用

需要更新以下文件中的路径引用：

1. **README.md** - 更新所有文档链接
2. **Makefile** - 更新脚本路径
3. **client.py** - 更新工具路径
4. **quickstart.sh** - 更新脚本路径
5. **其他脚本** - 更新相对路径

## ⚠️ 注意事项

1. **Git 追踪**: 使用 `git mv` 保持 Git 追踪历史
2. **权限保留**: 确保脚本的可执行权限保留
3. **相对路径**: 更新所有文件中的相对路径引用
4. **文档更新**: 更新文档中的文件路径说明

## 📋 预期效果

整理后的根目录：
```
knowledge-base-system/
├── README.md              ✨ 干净
├── Makefile               ✨ 干净
├── pyproject.toml         ✨ 干净
├── requirements.txt       ✨ 干净
├── requirements_core.txt  ✨ 干净
├── Dockerfile             ✨ 干净
├── docker-compose.yml     ✨ 干净
├── .gitignore             ✨ 干净
├── .coze                  ✨ 干净
├── docs/                  📁 文档
├── scripts/               📁 脚本
├── tools/                 📁 工具
├── assets/                📁 资源
├── config/                📁 配置
├── src/                   📁 源码
├── scripts/               📁 原有脚本
└── .venv/                 📁 虚拟环境
```

## 🚀 执行整理

准备好后执行整理脚本...
