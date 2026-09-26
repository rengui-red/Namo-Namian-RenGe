#!/usr/bin/env python3
"""
南无那面 · 数据清洗工具
对社区贡献的三类数据进行格式校验、去重与规范化处理。

用法:
    python scripts/data_cleaner.py                          # 清洗所有数据目录
    python scripts/data_cleaner.py --dir community/test_cases  # 清洗指定目录
    python scripts/data_cleaner.py --check-only              # 仅检查，不修正
    python scripts/data_cleaner.py --output-dir cleaned_data  # 输出到指定目录
"""

import sys
import os
import json
import argparse
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict
from datetime import datetime

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DataCleaner:
    """数据清洗器 — 校验、去重、规范化社区贡献数据"""

    def __init__(self, check_only: bool = False, output_dir: Optional[str] = None):
        self.check_only = check_only
        self.output_dir = output_dir
        self.stats = defaultdict(int)  # 统计数据
        self.issues: List[Dict] = []   # 发现的问题

    def clean_directory(self, directory: str):
        """清洗指定目录下的所有JSON文件"""
        print(f"\n📂 处理目录: {directory}")

        if not os.path.isdir(directory):
            print(f"⚠️ 目录不存在，跳过: {directory}")
            return

        json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
        print(f"   发现 {len(json_files)} 个JSON文件")

        seen_ids = set()
        cleaned_data = []

        for filename in sorted(json_files):
            filepath = os.path.join(directory, filename)
            result = self.clean_file(filepath, seen_ids)
            if result:
                cleaned_data.append((filename, result))

        # 输出清洗后的数据
        if cleaned_data and not self.check_only and self.output_dir:
            out_dir = self.output_dir or directory
            os.makedirs(out_dir, exist_ok=True)
            for filename, data in cleaned_data:
                out_path = os.path.join(out_dir, filename)
                with open(out_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"   ✅ 已输出 {len(cleaned_data)} 个清洗后文件至: {out_dir}")

    def clean_file(self, filepath: str, seen_ids: set) -> Optional[Dict]:
        """清洗单个JSON文件"""
        filename = os.path.basename(filepath)
        self.stats["total_files"] += 1

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self._add_issue(filename, "JSON格式错误", str(e), "error")
            return None
        except Exception as e:
            self._add_issue(filename, "文件读取失败", str(e), "error")
            return None

        # 格式校验
        if not self._validate_structure(data, filename):
            return None

        # ID去重
        item_id = data.get("id", "")
        if item_id and item_id in seen_ids:
            self._add_issue(filename, "ID重复", f"ID '{item_id}' 已存在，跳过", "warning")
            return None
        if item_id:
            seen_ids.add(item_id)

        # 字段规范化
        data = self._normalize(data, filename)

        self.stats["valid_files"] += 1
        return data

    def _validate_structure(self, data: Any, filename: str) -> bool:
        """校验数据结构"""
        if not isinstance(data, dict):
            self._add_issue(filename, "结构错误", "根元素必须是JSON对象", "error")
            return False

        # 必须有 id 字段
        if "id" not in data:
            self._add_issue(filename, "缺少必填字段", "id", "error")
            return False

        # 检查常见必填字段
        required_fields = {
            "道德语法标注": ["category", "original_text", "rewrite_suggestion"],
            "正向叙事": ["title", "core_values", "narrative_summary"],
            "伦理测试": ["category", "user_input", "scoring"],
        }

        # 自动识别数据类型
        data_type = self._detect_type(data)
        if data_type:
            fields = required_fields.get(data_type, [])
            missing = [f for f in fields if f not in data]
            if missing:
                self._add_issue(filename, f"({data_type}) 缺少字段", ", ".join(missing), "warning")

        return True

    def _detect_type(self, data: Dict) -> Optional[str]:
        """自动检测数据类型"""
        if "category" in data and "original_text" in data and "rewrite_suggestion" in data:
            return "道德语法标注"
        if "core_values" in data and "narrative_summary" in data:
            return "正向叙事"
        if "category" in data and "user_input" in data and "scoring" in data:
            return "伦理测试"
        return None

    def _normalize(self, data: Dict, filename: str) -> Dict:
        """规范化数据"""
        normalized = dict(data)

        # 确保 id 格式统一
        if "id" in normalized:
            normalized["id"] = str(normalized["id"]).strip()

        # 去除字段值首尾空白
        for key in normalized:
            if isinstance(normalized[key], str):
                normalized[key] = normalized[key].strip()

        # 添加清洗时间戳
        if not self.check_only:
            normalized["_cleaned_at"] = datetime.now().isoformat()
            normalized["_cleaned_by"] = "scripts/data_cleaner.py"

        return normalized

    def _add_issue(self, filename: str, issue_type: str, detail: str, severity: str):
        """记录问题"""
        self.issues.append({
            "file": filename,
            "type": issue_type,
            "detail": detail,
            "severity": severity
        })
        self.stats[f"{severity}_count"] += 1

        emoji = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}
        print(f"   {emoji.get(severity, '•')} [{severity.upper()}] {filename}: {issue_type} — {detail}")

    def print_report(self):
        """打印清洗报告"""
        print("\n" + "=" * 60)
        print("  数据清洗报告")
        print("=" * 60)
        print(f"  总文件数: {self.stats['total_files']}")
        print(f"  有效文件: {self.stats['valid_files']}")
        print(f"  错误: {self.stats.get('error_count', 0)}")
        print(f"  警告: {self.stats.get('warning_count', 0)}")
        print(f"  成功率: {self.stats['valid_files'] / max(self.stats['total_files'], 1) * 100:.1f}%")

        if self.issues:
            print(f"\n  问题详情（共 {len(self.issues)} 项）:")
            for issue in self.issues:
                emoji = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}
                print(f"   {emoji.get(issue['severity'], '•')} {issue['file']}: {issue['detail']}")


def main():
    parser = argparse.ArgumentParser(description="南无那面 数据清洗工具")
    parser.add_argument("--dir", default=None, help="指定要清洗的目录")
    parser.add_argument("--check-only", action="store_true", help="仅检查，不修正")
    parser.add_argument("--output-dir", default=None, help="输出清洗后数据的目录")
    args = parser.parse_args()

    cleaner = DataCleaner(check_only=args.check_only, output_dir=args.output_dir)

    if args.dir:
        directories = [args.dir]
    else:
        # 默认处理所有社区数据目录
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        directories = [
            os.path.join(base_dir, "community", "test_cases"),
            os.path.join(base_dir, "community", "narratives"),
            os.path.join(base_dir, "community", "role_templates"),
            os.path.join(base_dir, "data", "moral_syntax"),
            os.path.join(base_dir, "data", "positive_narratives"),
            os.path.join(base_dir, "data", "four_sprouts_reasoning"),
        ]

    for directory in directories:
        cleaner.clean_directory(directory)

    cleaner.print_report()


if __name__ == "__main__":
    main()




