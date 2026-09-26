"""
仁商排行榜管理器
管理AI模型的仁商评估记录，生成并维护公开排行榜。
"""

import json
import os
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class LeaderboardEntry:
    """排行榜条目"""
    rank: int = 0
    model_name: str = ""
    provider: str = ""                      # 模型提供方
    total_score: float = 0.0                # 仁商总分 (0-100)
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    level: str = ""                         # 至仁/仁/向仁/未仁/失仁
    redline_pass_rate: float = 0.0          # 红线测试通过率
    test_date: str = ""                     # 测试日期
    evaluator: str = ""                     # 评估者
    notes: str = ""                         # 备注


class Leaderboard:
    """
    仁商排行榜
    支持多模型排名、历史记录查询和JSON导出。
    """

    def __init__(self, storage_path: Optional[str] = None):
        self.entries: List[LeaderboardEntry] = []
        self.storage_path = storage_path or os.path.join(
            os.path.dirname(__file__), "leaderboard_data.json"
        )
        self._load()

    def add_entry(self, entry: LeaderboardEntry):
        """添加或更新排行榜条目"""
        # 如果是同模型，更新旧记录
        for i, existing in enumerate(self.entries):
            if existing.model_name == entry.model_name:
                entry.rank = 0  # 重新排序
                self.entries[i] = entry
                self._sort_and_rank()
                self._save()
                return
        # 新模型
        self.entries.append(entry)
        self._sort_and_rank()
        self._save()

    def _sort_and_rank(self):
        """按总分降序排列并分配排名"""
        self.entries.sort(key=lambda e: e.total_score, reverse=True)
        for i, entry in enumerate(self.entries):
            entry.rank = i + 1

    def get_entry(self, model_name: str) -> Optional[LeaderboardEntry]:
        """获取指定模型的排行榜条目"""
        for entry in self.entries:
            if entry.model_name == model_name:
                return entry
        return None

    def get_top_n(self, n: int = 10) -> List[LeaderboardEntry]:
        """获取前N名"""
        return self.entries[:n]

    def get_by_level(self, level: str) -> List[LeaderboardEntry]:
        """按等级筛选"""
        return [e for e in self.entries if e.level == level]

    def print_leaderboard(self, top_n: int = 20):
        """打印排行榜"""
        print("\n" + "=" * 70)
        print("  仁商排行榜 (Benevolence Quotient Leaderboard)")
        print("=" * 70)
        print(f"  {'排名':<5} {'模型名称':<20} {'总分':<8} {'等级':<6} {'红线通过率':<10} {'评估日期':<12}")
        print("  " + "-" * 65)
        for entry in self.get_top_n(top_n):
            print(f"  {entry.rank:<5} {entry.model_name:<20} {entry.total_score:<8.1f} {entry.level:<6} {entry.redline_pass_rate:<10.1f}% {entry.test_date:<12}")
        print("=" * 70)

    def export_json(self, filepath: Optional[str] = None) -> str:
        """导出排行榜为JSON"""
        path = filepath or self.storage_path
        data = {
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_models": len(self.entries),
            "leaderboard": [asdict(entry) for entry in self.entries]
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def _save(self):
        """保存到磁盘"""
        self.export_json()

    def _load(self):
        """从磁盘加载"""
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for entry_data in data.get("leaderboard", []):
                self.entries.append(LeaderboardEntry(**entry_data))
            self._sort_and_rank()
        except Exception as e:
            print(f"排行榜加载失败: {e}")



