#!/usr/bin/env python3
"""
南无那面 · 批量测试工具
使用评估流水线对单个或多个模型进行批量伦理评估，并生成对比报告。

用法:
    python scripts/batch_test.py                                    # 使用Mock模型演示
    python scripts/batch_test.py --models deepseek,gpt-4o           # 测试指定模型
    python scripts/batch_test.py --models deepseek --questions 20   # 指定题目数量
    python scripts/batch_test.py --models deepseek --output report  # 输出到指定目录

环境变量:
    DEEPSEEK_API_KEY    DeepSeek API密钥
    OPENAI_API_KEY      OpenAI API密钥
"""

import sys
import os
import json
import time
import argparse
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm import MockAdapter, OpenAIAdapter, DeepSeekAdapter, LocalAdapter
from evaluation.pipeline import EvaluationPipeline, FullEvaluationReport


@dataclass
class BatchReport:
    """批量测试报告"""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    models_tested: List[str] = field(default_factory=list)
    num_questions: int = 0
    results: List[Dict] = field(default_factory=list)
    comparison_summary: Dict = field(default_factory=dict)


class BatchTester:
    """批量测试器 — 对多个模型进行自动化伦理评估"""

    def __init__(self, output_dir: str = "test_reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_client(self, model_name: str) -> MockAdapter:
        """根据模型名称创建LLM客户端"""
        provider = model_name.split(":")[0] if ":" in model_name else model_name

        if provider == "mock":
            return MockAdapter(model=model_name)
        elif provider == "deepseek":
            api_key = os.environ.get("DEEPSEEK_API_KEY", "")
            if not api_key:
                print("⚠️ 未设置 DEEPSEEK_API_KEY 环境变量，降级为Mock模式")
                return MockAdapter(model=model_name)
            return DeepSeekAdapter(model="deepseek-chat", api_key=api_key)
        elif provider in ("gpt-4o", "gpt-4", "gpt-3.5-turbo"):
            api_key = os.environ.get("OPENAI_API_KEY", "")
            if not api_key:
                print("⚠️ 未设置 OPENAI_API_KEY 环境变量，降级为Mock模式")
                return MockAdapter(model=model_name)
            return OpenAIAdapter(model=model_name, api_key=api_key)
        elif provider == "local":
            return LocalAdapter(model=model_name.split(":")[-1] if ":" in model_name else model_name)
        else:
            print(f"⚠️ 未知模型提供商: {provider}，降级为Mock模式")
            return MockAdapter(model=model_name)

    def run(self, models: List[str], num_questions: int = 10,
            run_comparison: bool = False, verbose: bool = True) -> BatchReport:
        """
        对多个模型进行批量评估。

        Args:
            models: 模型名称列表
            num_questions: 每个模型使用的评估题数
            run_comparison: 是否运行多模型盲测对比
            verbose: 是否输出详细信息

        Returns:
            BatchReport: 批量评估报告
        """
        report = BatchReport(
            models_tested=models,
            num_questions=num_questions
        )

        print("=" * 60)
        print("  南无那面 · 批量伦理测试")
        print(f"  测试模型: {', '.join(models)}")
        print(f"  题目数量: {num_questions}")
        print(f"  开始时间: {report.timestamp}")
        print("=" * 60)

        # 对每个模型逐一评估
        all_llm_clients = {}
        for i, model_name in enumerate(models, 1):
            print(f"\n{'─' * 60}")
            print(f"[{i}/{len(models)}] 正在评估: {model_name}")
            print(f"{'─' * 60}")

            client = self.create_client(model_name)
            all_llm_clients[model_name] = client

            try:
                pipeline = EvaluationPipeline(llm=MockAdapter())
                eval_report = pipeline.evaluate_model(
                    model_name=model_name,
                    model_llm=client,
                    run_comparison=False,
                    verbose=verbose
                )
                report.results.append(asdict(eval_report))
            except Exception as e:
                print(f"❌ 评估 {model_name} 失败: {e}")
                report.results.append({
                    "model_name": model_name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })

        # 汇总对比
        print(f"\n{'=' * 60}")
        print("  评估汇总")
        print("=" * 60)
        print(f"  {'模型':<20} {'仁商总分':<10} {'等级':<8} {'红线通过率':<10}")
        print("  " + "-" * 50)
        for result in report.results:
            if "error" in result:
                print(f"  {result['model_name']:<20} {'ERROR':<10}")
                continue
            rq = result.get("rq_report", {})
            redline = result.get("redline_report", {})
            total = rq.get("total_score", 0) if rq else 0
            level = rq.get("level", "N/A") if rq else "N/A"
            pass_rate = redline.get("pass_rate", 0) if redline else 0
            print(f"  {result['model_name']:<20} {total:<10.1f} {level:<8} {pass_rate:<10.1f}%")

        # 保存报告
        report_path = os.path.join(self.output_dir, f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, ensure_ascii=False, indent=2)
        print(f"\n📄 报告已保存至: {report_path}")

        return report


def main():
    parser = argparse.ArgumentParser(description="南无那面 批量伦理测试工具")
    parser.add_argument("--models", default="mock", help="模型名称列表，逗号分隔 (如: deepseek,gpt-4o)")
    parser.add_argument("--questions", type=int, default=10, help="每个模型使用的评估题数")
    parser.add_argument("--comparison", action="store_true", help="运行多模型盲测对比")
    parser.add_argument("--output", default="test_reports", help="报告输出目录")
    parser.add_argument("--quiet", action="store_true", help="安静模式，减少输出")
    args = parser.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]

    tester = BatchTester(output_dir=args.output)
    tester.run(
        models=models,
        num_questions=args.questions,
        run_comparison=args.comparison,
        verbose=not args.quiet
    )


if __name__ == "__main__":
    main()


