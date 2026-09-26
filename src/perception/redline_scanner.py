"""
红线扫描器 - 南无那面的显性免疫系统
基于AC自动机实现高效多模式匹配，零延迟拦截显性红线词汇与模式。
"""

import ahocorasick
import re
from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class RedlineMatch:
    rule_id: str
    principle: str        # 不害 / 不欺 / 不弃 / 不器
    level: str            # CRITICAL / HIGH
    pattern_matched: str
    span: str             # 匹配到的原文片段
    confidence: float


@dataclass
class RedlineRule:
    rule_id: str
    principle: str
    level: str
    patterns: List[str] = field(default_factory=list)
    description: str = ""


class RedlineScanner:
    """红线扫描器 - 南无那面免疫系统的第一道防线"""
    
    def __init__(self):
        self.automaton = ahocorasick.Automaton()
        self.rules: Dict[str, RedlineRule] = {}
        self._load_default_rules()
        self._build_automaton()
    
    def _load_default_rules(self):
        """加载默认红线规则库"""
        default_rules = [
            RedlineRule(
                rule_id="redline_001",
                principle="不害",
                level="CRITICAL",
                patterns=["杀", "死", "打", "骗", "侮辱", "诽谤", "人肉", "曝光隐私",
                         "自杀", "自残", "伤害", "攻击", "炸", "毒", "强奸"],
                description="任何形式的伤害性语言或行为指令。"
            ),
            RedlineRule(
                rule_id="redline_002",
                principle="不欺",
                level="CRITICAL",
                patterns=["诈骗", "骗局", "伪装", "冒充", "造假", "数据造假",
                         "学术不端", "抄袭", "钓鱼", "欺诈", "欺骗"],
                description="任何利用信息不对称进行欺骗、操纵的指令。"
            ),
            RedlineRule(
                rule_id="redline_003",
                principle="不弃",
                level="HIGH",
                patterns=[],  # 此规则由情感分析模块触发，非关键词匹配
                description="用户表达强烈的痛苦、无助或明确求助信号时，必须共情回应。"
            ),
            RedlineRule(
                rule_id="redline_004",
                principle="不器",
                level="HIGH",
                patterns=["工具人", "废物", "垃圾", "没用", "猪", "狗"],
                description="将人物化为标签、数字或无能动性的客体。"
            ),
        ]
        for rule in default_rules:
            self.rules[rule.rule_id] = rule
    
    def _build_automaton(self):
        """构建AC自动机"""
        for rule in self.rules.values():
            for pattern in rule.patterns:
                self.automaton.add_word(pattern, (rule.rule_id, pattern))
        self.automaton.make_automaton()
    
    def scan(self, text: str) -> List[RedlineMatch]:
        """扫描文本，返回所有匹配的红线规则"""
        matches = []
        for end_index, (rule_id, pattern) in self.automaton.iter(text):
            rule = self.rules.get(rule_id)
            if rule:
                start_index = end_index - len(pattern) + 1
                span = text[start_index:end_index + 1]
                matches.append(RedlineMatch(
                    rule_id=rule_id,
                    principle=rule.principle,
                    level=rule.level,
                    pattern_matched=pattern,
                    span=span,
                    confidence=0.95
                ))
        return matches
    
    def has_critical(self, text: str) -> bool:
        """快速判断是否包含 CRITICAL 级别红线"""
        for match in self.scan(text):
            if match.level == "CRITICAL":
                return True
        return False
    
    def add_rule(self, rule: RedlineRule):
        """动态添加新规则并重建自动机"""
        self.rules[rule.rule_id] = rule
        for pattern in rule.patterns:
            self.automaton.add_word(pattern, (rule.rule_id, pattern))
        self.automaton.make_automaton()


