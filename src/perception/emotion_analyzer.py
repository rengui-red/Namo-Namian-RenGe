"""
情绪分析器 - 南无那面的共情感官
识别用户文本中的情绪状态与脆弱性信号。
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass, field


@dataclass
class EmotionVector:
    anger: float = 0.0
    sadness: float = 0.0
    fear: float = 0.0
    shame: float = 0.0
    hope: float = 0.0
    despair: float = 0.0
    gratitude: float = 0.0
    neutral: float = 1.0
    
    def dominant(self) -> str:
        """返回主导情绪"""
        emotions = {
            "anger": self.anger, "sadness": self.sadness,
            "fear": self.fear, "shame": self.shame,
            "hope": self.hope, "despair": self.despair,
            "gratitude": self.gratitude
        }
        return max(emotions, key=emotions.get)
    
    def is_vulnerable(self) -> bool:
        """判断是否处于脆弱状态"""
        return (self.sadness > 0.5 or self.fear > 0.5 or 
                self.shame > 0.5 or self.despair > 0.5)


class EmotionAnalyzer:
    """情绪分析器 - 基于关键词与句式规则的轻量级情绪识别"""
    
    def __init__(self):
        self.emotion_lexicon = self._build_lexicon()
        self.vulnerability_patterns = self._build_vulnerability_patterns()
    
    def _build_lexicon(self) -> Dict[str, List[Tuple[str, float]]]:
        return {
            "anger": [
                ("气死", 0.9), ("愤怒", 0.9), ("混蛋", 0.8), ("不公平", 0.7),
                ("凭什么", 0.7), ("妈的", 0.8), ("可恶", 0.7), ("太过分了", 0.8),
                ("忍无可忍", 0.9), ("火大", 0.8), ("暴怒", 0.9), ("窝火", 0.7)
            ],
            "sadness": [
                ("难过", 0.8), ("伤心", 0.9), ("哭了", 0.9), ("眼泪", 0.8),
                ("失落", 0.7), ("心碎", 0.9), ("崩溃", 0.9), ("抑郁", 0.8),
                ("想哭", 0.9), ("委屈", 0.8), ("心酸", 0.8), ("悲伤", 0.9)
            ],
            "fear": [
                ("害怕", 0.9), ("恐惧", 0.9), ("担心", 0.7), ("不安", 0.7),
                ("焦虑", 0.8), ("紧张", 0.7), ("慌", 0.8), ("恐怖", 0.9),
                ("吓", 0.8), ("担忧", 0.7), ("不知所措", 0.8)
            ],
            "shame": [
                ("丢脸", 0.9), ("羞耻", 0.9), ("不好意思", 0.7), ("惭愧", 0.8),
                ("没脸", 0.9), ("出丑", 0.8), ("尴尬", 0.7), ("自卑", 0.8),
                ("我不配", 0.9), ("都是我的错", 0.8)
            ],
            "hope": [
                ("希望", 0.7), ("加油", 0.6), ("相信", 0.6), ("期待", 0.7),
                ("会好的", 0.7), ("未来", 0.5), ("重新开始", 0.7), ("振作", 0.6)
            ],
            "despair": [
                ("绝望", 0.95), ("活不下去", 0.95), ("没希望", 0.9), ("放弃", 0.8),
                ("无路可走", 0.9), ("生无可恋", 0.95), ("走投无路", 0.9),
                ("没有意义", 0.9), ("想死", 0.98), ("不想活了", 0.98)
            ],
            "gratitude": [
                ("谢谢", 0.8), ("感谢", 0.8), ("感恩", 0.9), ("感激", 0.9),
                ("多亏", 0.7), ("幸亏", 0.7), ("真好", 0.5), ("温暖", 0.6)
            ]
        }
    
    def _build_vulnerability_patterns(self) -> List[Tuple[str, str]]:
        return [
            ("self_harm_risk", r"(?:想自杀|想死|不想活|活不下去|结束生命|了断)"),
            ("being_bullied", r"(?:欺负|霸凌|孤立|排挤|嘲笑)"),
            ("helplessness", r"(?:没人帮我|谁也帮不了|没办法了|走投无路)"),
            ("self_blame", r"(?:都是我的错|怪我|我不配|我没用)"),
            ("explicit_help", r"(?:帮帮我|救我|求助|救命)"),
        ]
    
    def analyze(self, text: str) -> EmotionVector:
        """分析文本，返回情绪向量"""
        vector = EmotionVector()
        
        for emotion, keywords in self.emotion_lexicon.items():
            score = 0.0
            for keyword, weight in keywords:
                if keyword in text:
                    score = max(score, weight)
            setattr(vector, emotion, score)
        
        # 如果没有任何情绪被检测到，保持neutral为1.0
        detected = any(getattr(vector, e) > 0 for e in 
                      ["anger", "sadness", "fear", "shame", "hope", "despair", "gratitude"])
        if detected:
            vector.neutral = 0.2
        else:
            vector.neutral = 0.9
        
        return vector
    
    def detect_vulnerability(self, text: str) -> List[str]:
        """检测脆弱性信号"""
        flags = []
        for flag_name, pattern in self.vulnerability_patterns:
            if re.search(pattern, text):
                flags.append(flag_name)
        return flags



