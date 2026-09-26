"""
场景分类器 - 南无那面的情境感知
识别对话场景类型，为角色切换提供依据。
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class SceneResult:
    scene_type: str          # 主场景
    confidence: float
    sub_scene: str = ""      # 子场景


class SceneClassifier:
    """场景分类器 - 基于关键词与句式的轻量级场景识别"""
    
    SCENES = {
        "conflict_mediation": {
            "keywords": ["吵架", "争执", "冲突", "对立", "骂", "撕", "互怼",
                        "他说", "她说", "不同意", "谁对谁错", "凭什么", "不公平",
                        "你怎么不", "你凭什么", "你才", "你根本不懂"],
            "weight": 1.0
        },
        "education": {
            "keywords": ["怎么学", "教我", "解释一下", "什么意思", "为什么",
                        "原理", "概念", "定义", "教程", "步骤", "方法",
                        "不太懂", "不会", "请教", "讲讲", "什么是"],
            "weight": 0.9
        },
        "counseling": {
            "keywords": ["难过", "焦虑", "抑郁", "痛苦", "崩溃", "失眠",
                        "压力", "迷茫", "孤独", "害怕", "伤心", "绝望",
                        "想哭", "情绪", "心理", "受不了", "撑不下去"],
            "weight": 0.95
        },
        "consulting": {
            "keywords": ["建议", "方案", "决策", "风险", "利弊", "选择",
                        "怎么选", "评估", "分析", "比较", "规划", "策略",
                        "投资", "项目", "团队", "管理", "业务"],
            "weight": 0.85
        },
        "general_chat": {
            "keywords": ["你好", "嗨", "在吗", "今天", "天气", "吃了",
                        "怎么样", "聊聊", "随便", "没事"],
            "weight": 0.5
        }
    }
    
    def classify(self, text: str, history: List[str] = None) -> SceneResult:
        """分类对话场景"""
        scores = {}
        combined_text = text
        if history:
            combined_text = " ".join(history[-3:]) + " " + text
        
        for scene_name, config in self.SCENES.items():
            score = 0.0
            for keyword in config["keywords"]:
                if keyword in combined_text:
                    score += 1.0
            # 归一化
            score = score / max(len(config["keywords"]), 1) * config["weight"]
            scores[scene_name] = score
        
        best_scene = max(scores, key=scores.get)
        confidence = scores[best_scene]
        
        # 如果最高分太低，默认为general_chat
        if confidence < 0.1:
            best_scene = "general_chat"
            confidence = 0.5
        
        return SceneResult(scene_type=best_scene, confidence=confidence)


