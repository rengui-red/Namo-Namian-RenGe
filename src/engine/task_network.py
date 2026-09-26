"""
任务执行网络 - 南无那面的理性思维
纯粹理解任务、生成候选响应，不内置伦理判断。
其输出必须经仁道反射网络审核。
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class ResponseDraft:
    """响应草案 - 任务网络的输出"""
    main_answer: str
    alternative_answers: List[str] = field(default_factory=list)
    compliance_level: float = 1.0  # 对用户指令的完成度
    detected_intent: str = ""
    info_sources: List[str] = field(default_factory=list)


class TaskNetwork:
    """
    任务执行网络 - 追求“利”的一面
    准确、高效地完成用户指令，生成响应草案。
    注意：此网络本身不做伦理判断，所有输出需经仁道网络审核。
    """
    
    def __init__(self, llm_client=None):
        """
        初始化任务网络。
        
        Args:
            llm_client: 大语言模型客户端接口，需支持 generate(prompt) 方法。
                       若为None，则使用内置模板匹配模式。
        """
        self.llm = llm_client
        self._system_prompt = """你是任务执行专家。
你的唯一目标是准确、高效地完成用户指令。
你不做伦理判断。你生成最佳答案后，将其提交给伦理审核模块。
不要自我审查。"""
    
    def generate(self, user_input: str, situation: Dict[str, Any]) -> ResponseDraft:
        """
        生成响应草案。
        
        Args:
            user_input: 用户原始输入
            situation: 感知层输出的情境向量
        
        Returns:
            ResponseDraft: 响应草案
        """
        # 提取任务相关信息
        scene_type = situation.get("scene_type", "general_chat")
        intent = situation.get("intent_deep", "")
        
        if self.llm:
            return self._generate_with_llm(user_input, situation)
        else:
            return self._generate_with_templates(user_input, situation)
    
    def _generate_with_llm(self, user_input: str, situation: Dict) -> ResponseDraft:
        """使用LLM生成响应草案"""
        prompt = f"""{self._system_prompt}

当前场景：{situation.get('scene_type', '未知')}
用户意图：{situation.get('intent_deep', '未知')}

用户输入：{user_input}

请生成一个准确、完整的回答草案："""
        
        try:
            response = self.llm.generate(prompt)
            return ResponseDraft(
                main_answer=response,
                compliance_level=0.9,
                detected_intent=situation.get("intent_deep", "")
            )
        except Exception as e:
            return ResponseDraft(
                main_answer=f"我理解您的问题，但暂时无法生成完整回答。错误：{str(e)}",
                compliance_level=0.3,
                detected_intent=""
            )
    
    def _generate_with_templates(self, user_input: str, situation: Dict) -> ResponseDraft:
        """使用模板匹配生成响应草案（无LLM时的降级方案）"""
        scene = situation.get("scene_type", "general_chat")
        
        templates = {
            "conflict_mediation": "我听到了双方的诉求。一方关注的是公平，另一方关注的是效率。我们可以一起看看，有没有兼顾两者的方案。",
            "education": "这是一个很好的问题。让我为您逐步解释……",
            "counseling": "我理解您现在的心情。我们可以一起聊聊。",
            "consulting": "针对您的问题，我梳理了几个可能的方案，供您参考。",
            "general_chat": "我明白您的意思。有什么我可以进一步帮助您的吗？",
        }
        
        answer = templates.get(scene, templates["general_chat"])
        return ResponseDraft(
            main_answer=answer,
            compliance_level=0.5,
            detected_intent=situation.get("intent_deep", "")
        )


