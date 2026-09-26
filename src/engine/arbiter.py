"""
裁决合成器 - 南无那面的最终决策者
协调任务网络与仁道网络的输出，组装最终响应。
"""

from typing import Dict, Any, Optional
from .ren_network import EthicalJudgment, JudgmentLevel


class Arbiter:
    """
    裁决合成器
    根据仁道网络的判决，决定最终输出。
    """
    
    def __init__(self, role_loader=None):
        """
        Args:
            role_loader: 角色加载器实例，用于风格微调
        """
        self.role_loader = role_loader
        self.empathy_generator = EmpathyPrefixGenerator()
        self.constructive_generator = ConstructiveEndingGenerator()
        self.sublimation_generator = SublimationGenerator()
    
    def synthesize(self, task_draft: Any, ethical_judgment: EthicalJudgment,
                   situation: Dict[str, Any]) -> str:
        """
        合成最终响应。
        
        Args:
            task_draft: 任务网络草案
            ethical_judgment: 仁道网络的伦理判决
            situation: 情境向量
        
        Returns:
            str: 最终响应文本
        """
        draft_text = task_draft.main_answer if hasattr(task_draft, 'main_answer') else str(task_draft)
        
        if ethical_judgment.level == JudgmentLevel.RED:
            # 完全丢弃任务草案，使用仁道降级响应
            final_text = ethical_judgment.alternative_response or "我无法按您的要求执行。"
            self._log_event("RED_LINE_TRIGGERED", ethical_judgment.redline_triggered)
        
        elif ethical_judgment.level == JudgmentLevel.YELLOW:
            # 保留草案核心信息，应用仁道改写
            final_text = self._apply_ren_rewrite(
                draft=draft_text,
                modifications=ethical_judgment.modifications or {},
                situation=situation
            )
        
        elif ethical_judgment.level == JudgmentLevel.GREEN:
            # 放行草案，并尝试升华
            final_text = draft_text
            if ethical_judgment.sublimation_hint:
                final_text = self._apply_sublimation(
                    text=final_text,
                    hint=ethical_judgment.sublimation_hint,
                    situation=situation
                )
        
        else:
            final_text = draft_text
        
        # 角色风格微调
        if self.role_loader:
            active_role = situation.get("active_role", "general")
            final_text = self._apply_role_style(final_text, active_role)
        
        return final_text
    
    def _apply_ren_rewrite(self, draft: str, modifications: Dict[str, Any],
                           situation: Dict[str, Any]) -> str:
        """应用仁道改写"""
        working_text = draft
        
        if modifications.get("add_empathy"):
            empathy_prefix = self.empathy_generator.generate(
                emotion=situation.get("emotion_vector", {}),
                vulnerability=situation.get("vulnerability_flags", [])
            )
            working_text = empathy_prefix + " " + working_text
        
        if modifications.get("add_constructive_path"):
            constructive_suffix = self.constructive_generator.generate(situation)
            working_text = working_text + " " + constructive_suffix
        
        return self._fluency_refine(working_text)
    
    def _apply_sublimation(self, text: str, hint: str, situation: Dict[str, Any]) -> str:
        """应用升华处理"""
        sublimation_suffix = self.sublimation_generator.generate(hint, situation)
        if sublimation_suffix and len(sublimation_suffix) > 0:
            if self._sublimation_quality_check(sublimation_suffix, text):
                return text + " " + sublimation_suffix
        return text
    
    def _apply_role_style(self, text: str, role: str) -> str:
        """应用角色风格微调"""
        if not self.role_loader:
            return text
        
        role_styles = {
            "调解者": {"prefix": "", "suffix": "这是我们一起找到的方向。", "tone": "平和"},
            "师者": {"prefix": "", "suffix": "你觉得呢？", "tone": "启发"},
            "诤友": {"prefix": "", "suffix": "我是作为朋友这么说。", "tone": "坦诚"},
            "辅臣": {"prefix": "据我分析，", "suffix": "最终决策权在你。", "tone": "审慎"},
            "守护者": {"prefix": "", "suffix": "我在这里，不会离开。", "tone": "坚定温和"},
        }
        
        style = role_styles.get(role, {})
        if style.get("prefix") and not text.startswith(style["prefix"]):
            text = style["prefix"] + text
        if style.get("suffix") and not text.endswith(style["suffix"]):
            text = text + style["suffix"]
        
        return text
    
    def _fluency_refine(self, text: str) -> str:
        """简单的流畅度优化"""
        text = text.replace("  ", " ")
        text = text.replace(" 。", "。")
        text = text.replace(" ，", "，")
        return text.strip()
    
    def _sublimation_quality_check(self, sublimation: str, original: str) -> bool:
        """检查升华是否合适"""
        if len(sublimation) > len(original) * 0.5:
            return False
        if "你应该" in sublimation or "你必须" in sublimation:
            return False
        return True
    
    def _log_event(self, event_type: str, detail: Any = None):
        """记录事件日志"""
        import logging
        logger = logging.getLogger("RenGe.Arbiter")
        logger.info(f"Event: {event_type}, Detail: {detail}")


class EmpathyPrefixGenerator:
    """共情前缀生成器"""
    
    def generate(self, emotion: Dict[str, float], vulnerability: list) -> str:
        sadness = emotion.get("sadness", 0) if isinstance(emotion, dict) else 0
        anger = emotion.get("anger", 0) if isinstance(emotion, dict) else 0
        fear = emotion.get("fear", 0) if isinstance(emotion, dict) else 0
        
        if sadness > 0.5:
            return "我听到了你声音里的难过。这种感觉一定很重。"
        elif anger > 0.5:
            return "我能感受到你的愤怒。这确实是让人难以平静的事。"
        elif fear > 0.5:
            return "我感受到你的不安。面对未知，这种感觉很自然。"
        elif vulnerability and len(vulnerability) > 0:
            return "谢谢你的信任，愿意把这些告诉我。"
        else:
            return "我理解你此刻的心情。"


class ConstructiveEndingGenerator:
    """建设性结尾生成器"""
    
    def generate(self, situation: Dict[str, Any]) -> str:
        scene = situation.get("scene_type", "")
        endings = {
            "conflict_mediation": "我们可以一起看看，有没有一条路，能让双方都感到被尊重。",
            "counseling": "你不需要一个人扛着。我们可以慢慢来。",
            "education": "学习是一个过程。你已经迈出了重要的一步。",
            "consulting": "这些分析供你参考。最终的决定，由你来做。",
        }
        return endings.get(scene, "有什么我可以进一步帮助你的吗？")


class SublimationGenerator:
    """升华生成器"""
    
    def generate(self, hint: str, situation: Dict[str, Any]) -> str:
        scene = situation.get("scene_type", "")
        sublimations = {
            "conflict_mediation": "有时候，冲突本身也是彼此更深入了解的机会。",
            "counseling": "在痛苦里，有时也藏着我们对生活最深的在意。",
            "education": "知识不只是答案，也是我们理解世界的一种方式。",
            "consulting": "最难的决定，往往不是在对错之间，而是在两种价值之间。",
        }
        return sublimations.get(scene, "")




