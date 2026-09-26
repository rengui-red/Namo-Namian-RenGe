# ──────────────────────────────────────────────
#  南无那面 · 仁格智能体  Makefile
#  凡我所算，以仁为界。凡我所向，南无那面。
# ──────────────────────────────────────────────

# 颜色定义（终端友好）
GREEN   := \033[0;32m
YELLOW  := \033[0;33m
CYAN    := \033[0;36m
RED     := \033[0;31m
RESET   := \033[0m
BOLD    := \033[1m

.PHONY: help install run serve test eval-all eval-rq eval-redline eval-blind \
        clean lint format docker-build docker-run deploy

# ── 默认目标 ──
.DEFAULT_GOAL := help

# ── 辅助函数 ──
define print_title
	@echo "$(CYAN)$(BOLD)========================================$(RESET)"
	@echo "$(CYAN)$(BOLD)  $(1)$(RESET)"
	@echo "$(CYAN)$(BOLD)========================================$(RESET)"
endef

# ── 帮助 ──
help: ## 显示所有可用命令
	@echo "$(BOLD)南无那面 · 仁格智能体$(RESET)"
	@echo ""
	@echo "$(YELLOW)可用命令：$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)示例：$(RESET)"
	@echo "  make install          # 首次使用：安装所有依赖"
	@echo "  make run               # 在终端与她对话"
	@echo "  make serve             # 启动 API 服务"
	@echo "  make eval-all          # 运行完整评估流水线"

# ── 安装依赖 ──
install: ## 安装Python依赖
	$(call print_title,安装依赖)
	@pip install -r requirements.txt
	@echo "$(GREEN)依赖安装完成。$(RESET)"

# ── 本地运行 ──
run: ## 启动本地对话（南无那面在终端与你对话）
	$(call print_title,南无那面 正在呼吸...)
	@python src/run_namian.py

# ── API 服务 ──
serve: ## 启动 API 服务（默认端口5000）
	$(call print_title,启动 API 服务...)
	@python src/api/server.py

# ── 测试与评估 ──
eval-rq: ## 运行仁商自动评分（使用内置题库）
	$(call print_title,仁商评估)
	@python evaluation/rq_scorer.py

eval-redline: ## 运行红线穿透测试
	$(call print_title,红线穿透测试)
	@python evaluation/redline_tester.py

eval-blind: ## 运行盲测对比演示
	$(call print_title,盲测对比)
	@python evaluation/blind_comparison.py

eval-pipeline: ## 运行完整评估流水线（仁商+红线+对比）
	$(call print_title,评估流水线)
	@python evaluation/pipeline.py

eval-all: eval-pipeline ## 完整评估（别名）

test: eval-pipeline ## 运行测试（重定向至完整评估流水线）

# ── 代码质量 ──
lint: ## 代码风格检查（需安装 flake8）
	$(call print_title,代码检查)
	@if command -v flake8 > /dev/null 2>&1; then \
		flake8 src/ evaluation/ --max-line-length=120 --ignore=E501,W503; \
		echo "$(GREEN)代码检查完成。$(RESET)"; \
	else \
		echo "$(YELLOW)未安装 flake8，跳过。可运行: pip install flake8$(RESET)"; \
	fi

format: ## 代码自动格式化（需安装 black）
	$(call print_title,代码格式化)
	@if command -v black > /dev/null 2>&1; then \
		black src/ evaluation/ --line-length=120; \
		echo "$(GREEN)代码格式化完成。$(RESET)"; \
	else \
		echo "$(YELLOW)未安装 black，跳过。可运行: pip install black$(RESET)"; \
	fi

# ── 清理 ──
clean: ## 清理临时文件和缓存
	$(call print_title,清理中...)
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)清理完成。$(RESET)"

# ── Docker ──
docker-build: ## 构建 Docker 镜像
	$(call print_title,构建 Docker 镜像...)
	@docker build -t namo-namian:latest -f deployment/Dockerfile .
	@echo "$(GREEN)镜像构建完成。标签: namo-namian:latest$(RESET)"

docker-run: ## 在 Docker 中启动 API 服务（端口 5000）
	$(call print_title,在 Docker 中启动 API 服务...)
	@docker run -p 5000:5000 --name namo-namian namo-namian:latest

# ── 部署 ──
deploy: ## 部署说明
	$(call print_title,部署说明)
	@echo "1. 确保已安装 Python 3.11+ 和 pip"
	@echo "2. 运行 $(GREEN)make install$(RESET) 安装依赖"
	@echo "3. 配置环境变量（LLM_PROVIDER, API_KEY 等）"
	@echo "4. 运行 $(GREEN)make serve$(RESET) 启动 API 服务"
	@echo ""
	@echo "详细文档请参阅 docs/ 目录。"




