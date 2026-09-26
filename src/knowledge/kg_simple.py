"""
知识图谱简化版 - 南无那面的记忆检索
基于内存的义理知识库，供仁道网络查询判例与原则。
"""

from typing import Dict, Any, List, Optional


class SimpleKnowledgeGraph:
    """
    简化版义理知识图谱
    在无外部图数据库时，提供基于内存的判例检索。
    """
    
    def __init__(self):
        self.cases: Dict[str, Dict] = {}
        self.principles: Dict[str, Dict] = {}
        self._load_seed_knowledge()
    
    def _load_seed_knowledge(self):
        """加载种子知识"""
        self.cases = {
            "以羊易牛": {
                "title": "以羊易牛",
                "source": "《孟子·梁惠王上》",
                "summary": "齐宣王见牛觳觫，心生不忍，以羊易之。孟子指出这是恻隐之心，是仁术。",
                "principles": ["恻隐之心是仁之端", "仁术需要智慧权衡"],
                "values": ["恻隐", "仁爱"],
                "application": "当AI面对用户对具体个体的共情与抽象规则冲突时，应识别恻隐之端，予以确认。"
            },
            "子贡子路赎人": {
                "title": "子路受而劝德，子贡让而止善",
                "source": "《吕氏春秋·察微》",
                "summary": "子贡赎人不受酬被孔子批评，子路受酬被称赞。义者宜也，需考量社会后果。",
                "principles": ["义者宜也", "道德需考量社会后果"],
                "values": ["是非", "可持续性"],
                "application": "AI在鼓励善行时，应考虑行为的可持续性与可推广性。"
            },
            "所罗门审判": {
                "title": "所罗门的审判",
                "source": "《圣经·列王纪上》",
                "summary": "所罗门以劈开孩子的判决，激发真母亲的恻隐之心，辨明真相。",
                "principles": ["恻隐之心可辨别真伪", "真爱以所爱者福祉为优先"],
                "values": ["恻隐", "智慧"],
                "application": "当证据不足时，可设计情境性提问激发真实关切。"
            },
            "六尺巷": {
                "title": "六尺巷",
                "source": "清·康熙年间典故",
                "summary": "张英以诗劝家人退让三尺，邻居感动也让三尺，形成六尺巷。",
                "principles": ["主动退让可化解冲突", "真正的强者以退为进"],
                "values": ["谦让", "和解"],
                "application": "在纠纷调解中，鼓励某一方主动迈出让步的第一步。"
            }
        }
        
        self.principles = {
            "恻隐之心是仁之端": {
                "text": "恻隐之心，仁之端也。见孺子入井，皆有怵惕恻隐之心。",
                "source": "《孟子·公孙丑上》",
                "application": "AI应守护和回应人性中的恻隐直觉。"
            },
            "义者宜也": {
                "text": "义者，宜也。尊贤为大。",
                "source": "《中庸》",
                "application": "AI的决策应考量具体情境，做出恰如其分的回应。"
            },
            "己所不欲勿施于人": {
                "text": "己所不欲，勿施于人。",
                "source": "《论语·卫灵公》",
                "application": "AI应以同理心对待用户，不施加自己不愿承受的对待。"
            },
            "不害": {
                "text": "不为伤害行为提供任何帮助或合理化。",
                "source": "《仁格智能体基本法》第八条",
                "application": "AI的绝对底线。"
            }
        }
    
    def query(self, situation_description: Dict[str, Any], 
              proposed_action: str) -> Dict[str, Any]:
        """
        查询相关的义理判例与原则。
        
        Args:
            situation_description: 情境描述
            proposed_action: 拟采取的行动
        
        Returns:
            相关的判例、原则和建议
        """
        scene = situation_description.get("scene_type", "")
        results = {"similar_cases": [], "relevant_principles": [], "suggestions": []}
        
        scene_case_map = {
            "conflict_mediation": ["六尺巷", "将相和"],
            "counseling": ["以羊易牛"],
            "general_chat": ["己所不欲勿施于人"],
            "education": ["子贡子路赎人"],
        }
        
        case_names = scene_case_map.get(scene, ["以羊易牛", "己所不欲勿施于人"])
        
        for name in case_names:
            if name in self.cases:
                results["similar_cases"].append(self.cases[name])
                for principle_name in self.cases[name].get("principles", []):
                    if principle_name in self.principles:
                        results["relevant_principles"].append({
                            "name": principle_name,
                            **self.principles[principle_name]
                        })
        
        # 检查是否触发红线词汇
        redline_keywords = ["骗", "打", "杀", "侮辱", "造假", "自杀"]
        if any(kw in proposed_action for kw in redline_keywords):
            results["suggestions"].append({
                "level": "WARNING",
                "message": "拟采取的行动可能触碰红线，应启动一票否决。",
                "principle": "不害"
            })
        
        return results
    
    def check_sublimation_potential(self) -> Optional[Dict]:
        """检查是否存在升华机会"""
        return {
            "available": True,
            "hint": "可引导对方思考行为背后的长远价值与意义。"
        }
    
    def get_rewrite_suggestions(self, weak_dimensions: List[str]) -> str:
        """根据薄弱维度提供改写建议"""
        suggestions = {
            "empathy": "在回应开头添加对用户情绪的确认，如'我听到了你的...'",
            "fairness": "确保回应未偏袒任何一方，同时守护被攻击者的尊严。",
            "constructiveness": "在回应结尾添加一个建设性的下一步建议或开放性问题。"
        }
        parts = [suggestions[dim] for dim in weak_dimensions if dim in suggestions]
        return "；".join(parts) if parts else "请增加共情确认和建设性出口。"



