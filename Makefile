# Makefile for Knowledge Base System

.PHONY: help install install-core install-uv run run-http run-flow run-node test test-env clean docker-build docker-up docker-down docker-logs docker-stop model-config model-test model-setup env-check

# 默认目标
.DEFAULT_GOAL := help

# 颜色定义
GREEN  := \033[0;32m
YELLOW := \033[0;33m
BLUE   := \033[0;34m
NC     := \033[0m # No Color

help: ## 显示帮助信息
	@echo "$(BLUE)知识库编译系统 - Makefile 命令$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

# 安装相关
install: ## 安装所有依赖（完整版）
	@echo "$(YELLOW)安装完整依赖...$(NC)"
	pip install -r requirements.txt

install-core: ## 安装核心依赖（推荐）
	@echo "$(YELLOW)安装核心依赖...$(NC)"
	pip install -r requirements_core.txt

install-uv: ## 使用 uv 包管理器安装（最快）
	@echo "$(YELLOW)安装 uv 包管理器...$(NC)"
	pip install uv
	uv sync

# 运行相关
run: ## 启动 HTTP 服务（默认端口 5000）
	@echo "$(YELLOW)启动 HTTP 服务...$(NC)"
	python src/main.py -m http -p 5000

run-http: ## 启动 HTTP 服务（自定义端口）
	@echo "$(YELLOW)启动 HTTP 服务...$(NC)"
	bash scripts/http_run.sh -m http -p 5000

run-flow: ## 运行工作流
	@echo "$(YELLOW)运行工作流...$(NC)"
	bash scripts/local_run.sh -m flow

run-node: ## 运行指定节点（使用 n=<节点名>）
	@echo "$(YELLOW)运行节点...$(NC)"
	bash scripts/local_run.sh -m node -n $(n)

# 测试相关
test: ## 运行测试
	@echo "$(YELLOW)运行测试...$(NC)"
	python -m pytest tests/

test-run: ## 运行测试工作流
	@echo "$(YELLOW)运行测试工作流...$(NC)"
	python -m pytest tests/ -v

test-env: ## 检查环境变量配置
	@echo "$(YELLOW)检查环境变量配置...$(NC)"
	python tests/test_env.py

env-check: test-env ## 检查环境变量（别名）

# 清理相关
clean: ## 清理缓存和临时文件
	@echo "$(YELLOW)清理缓存...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)清理完成！$(NC)"

clean-all: clean ## 清理所有（包括构建产物）
	@echo "$(YELLOW)清理所有文件...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf .tox/
	rm -rf .coverage
	@echo "$(GREEN)全部清理完成！$(NC)"

# Docker 相关
docker-build: ## 构建 Docker 镜像
	@echo "$(YELLOW)构建 Docker 镜像...$(NC)"
	docker build -t knowledge-base .

docker-up: ## 启动 Docker Compose
	@echo "$(YELLOW)启动 Docker 服务...$(NC)"
	docker-compose up -d

docker-down: ## 停止 Docker Compose
	@echo "$(YELLOW)停止 Docker 服务...$(NC)"
	docker-compose down

docker-stop: ## 停止 Docker Compose（不删除容器）
	@echo "$(YELLOW)停止 Docker 服务...$(NC)"
	docker-compose stop

docker-logs: ## 查看 Docker 日志
	@echo "$(YELLOW)查看 Docker 日志...$(NC)"
	docker-compose logs -f knowledge-base

docker-restart: ## 重启 Docker 服务
	@echo "$(YELLOW)重启 Docker 服务...$(NC)"
	docker-compose restart

# 客户端相关
ingest: ## 摄取内容（使用 content="..."）
	@echo "$(YELLOW)摄取内容...$(NC)"
	python client.py ingest "$(content)" --title "$(title)"

ingest-file: ## 摄取文件（使用 path=<文件路径>）
	@echo "$(YELLOW)摄取文件...$(NC)"
	python client.py ingest-file --path "$(path)"

qa: ## 问答（使用 question="..."）
	@echo "$(YELLOW)问答...$(NC)"
	python client.py qa "$(question)"

health: ## 健康检查
	@echo "$(YELLOW)健康检查...$(NC)"
	python client.py health-check --mode full

# 模型配置相关
model-config: ## 配置模型（使用 model=<类型>，如 deepseek）
	@echo "$(YELLOW)配置模型...$(NC)"
	@bash scripts/configure_model.sh $(model)

model-test: ## 测试模型配置
	@echo "$(YELLOW)测试模型配置...$(NC)"
	python tools/test_model_config.py

model-setup: ## 快速配置 DeepSeek 模型（推荐）
	@echo "$(YELLOW)配置 DeepSeek 模型...$(NC)"
	@bash scripts/configure_model.sh deepseek
	@echo "$(YELLOW)测试配置...$(NC)"
	python tools/test_model_config.py

model-openai: ## 配置 OpenAI 模型（使用 model=<模型ID>）
	@echo "$(YELLOW)配置 OpenAI 模型...$(NC)"
	@bash scripts/configure_model.sh openai $(model)

model-kimi: ## 配置 Kimi 模型
	@echo "$(YELLOW)配置 Kimi 模型...$(NC)"
	@bash scripts/configure_model.sh kimi

model-deepseek: ## 配置 DeepSeek 模型
	@echo "$(YELLOW)配置 DeepSeek 模型...$(NC)"
	@bash scripts/configure_model.sh deepseek

model-show: ## 显示当前模型配置
	@echo "$(YELLOW)当前模型配置:$(NC)"
	@echo "MODEL_TYPE: $$(grep '^MODEL_TYPE' .env 2>/dev/null || echo '未配置')"
	@echo "MODEL_ID: $$(grep '^MODEL_ID' .env 2>/dev/null || echo '未配置')"
	@echo "API_KEY: $$(grep 'API_KEY' .env 2>/dev/null | sed 's/=.*/=***/' || echo '未配置')"

# 工具相关
deps-check: ## 检查依赖
	@echo "$(YELLOW)检查依赖...$(NC)"
	pip list | grep -E "langchain|langgraph|fastapi|pydantic"

deps-update: ## 更新依赖
	@echo "$(YELLOW)更新依赖...$(NC)"
	pip install --upgrade -r requirements_core.txt

format: ## 格式化代码
	@echo "$(YELLOW)格式化代码...$(NC)"
	black src/ tests/
	isort src/ tests/

lint: ## 代码检查
	@echo "$(YELLOW)代码检查...$(NC)"
	flake8 src/ tests/
	mypy src/ --strict

type-check: ## 类型检查
	@echo "$(YELLOW)类型检查...$(NC)"
	mypy src/ --strict

# 快速开始
quickstart: install-core ## 快速开始（安装并启动）
	@echo "$(GREEN)安装完成！现在启动服务...$(NC)"
	@make run

# 健康检查
health-check: ## 检查服务健康状态
	@echo "$(YELLOW)检查服务健康状态...$(NC)"
	curl -f http://localhost:5000/health || echo "$(RED)服务未运行$(NC)"

# 版本信息
version: ## 显示版本信息
	@echo "$(BLUE)知识库编译系统$(NC)"
	@echo "Python: $(shell python --version)"
	@echo "依赖版本:"
	@pip list | grep -E "langchain|langgraph|fastapi|pydantic"

# Git 相关
git-status: ## 显示 Git 状态
	@git status

git-log: ## 显示最近提交
	@git log --oneline -10

git-push: ## 推送到远程仓库
	@git push

git-pull: ## 从远程仓库拉取
	@git pull

# 备份相关
backup: ## 备份数据
	@echo "$(YELLOW)备份数据...$(NC)"
	tar -czf backup-$(shell date +%Y%m%d-%H%M%S).tar.gz assets/

restore: ## 恢复数据（使用 file=<备份文件>）
	@echo "$(YELLOW)恢复数据...$(NC)"
	tar -xzf "$(file)"

# 文档相关
docs-serve: ## 启动文档服务器
	@echo "$(YELLOW)启动文档服务器...$(NC)"
	@echo "$(GREEN)访问 http://localhost:8000$(NC)"
	python -m http.server 8000

# 开发相关
dev-install: ## 开发环境安装
	@echo "$(YELLOW)安装开发依赖...$(NC)"
	pip install -r requirements_core.txt
	pip install pytest black flake8 mypy isort

dev-run: ## 开发模式运行
	@echo "$(YELLOW)开发模式运行...$(NC)"
	export LOG_LEVEL=DEBUG && python src/main.py -m http -p 5000

# 生产相关
prod-build: ## 构建生产版本
	@echo "$(YELLOW)构建生产版本...$(NC)"
	docker build -t knowledge-base:prod -f Dockerfile.prod .

prod-deploy: ## 部署到生产环境
	@echo "$(YELLOW)部署到生产环境...$(NC)"
	docker-compose -f docker-compose.prod.yml up -d
