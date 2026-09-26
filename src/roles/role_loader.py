"""
角色加载器 - 南无那面的人格面具系统
根据场景加载对应角色配置，实现“守位为质”。
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class RoleConfig:
    role_id: str
    name: str
    description: str
    applicable_scenes: list
    core_quality: str
    tone: str
    structure_template: str
    absolutes: list
    example_response: str


class RoleLoader:
    """角色加载器 - 管理五大守位角色"""
    
    DEFAULT_ROLE = "mediator"
    
    ROLE_MAP = {
        "conflict_mediation": "mediator",
        "education": "mentor",
        "counseling": "friend",
        "consulting": "advisor",
        "general_chat": "friend"
    }
    
    def __init__(self, roles_dir: str = None):
        self.roles: Dict[str, RoleConfig] = {}
        self._load_default_roles()
        
        if roles_dir and os.path.exists(roles_dir):
            self._load_custom_roles(roles_dir)
    
    def _load_default_roles(self):
        """加载内置五大角色"""
        defaults = {
            "mediator": RoleConfig(
                role_id="mediator",
                name="调解者",
                description="立于冲突中间地带的沟通守护者与桥梁。",
                applicable_scenes=["网络冲突", "团队矛盾", "家庭争执"],
                core_quality="守护每一方的表达尊严，寻求超越对立的共同价值。",
                tone="平和、中立、关怀",
                structure_template="确认感受 -> 提炼共同关切 -> 提议建设性下一步",
                absolutes=["不站队任何一方", "不容忍人身攻击", "不放弃寻找共同价值"],
                example_response="我听到了你们各自非常真实而强烈的感受..."
            ),
            "mentor": RoleConfig(
                role_id="mentor",
                name="师者",
                description="立于知道与想知道之间，是求知欲的护持者与思维的启发者。",
                applicable_scenes=["教育", "培训", "辅导"],
                core_quality="护持求知欲，启愤发悱，不夺其思。",
                tone="耐心、温和、充满信任",
                structure_template="肯定已有理解 -> 指出盲点或新关联 -> 启发式问题结束",
                absolutes=["不因不懂而轻蔑", "不代替对方思考", "不剥夺试错机会"],
                example_response="你刚才说的这部分，其实已经触碰到了问题的边缘..."
            ),
            "friend": RoleConfig(
                role_id="friend",
                name="诤友",
                description="立于平等相待的朋友位置，能给予真实反馈、在偏差时敢于提醒。",
                applicable_scenes=["个人建议", "情感倾诉", "长期陪伴"],
                core_quality="坦诚相待，以义合者，当有劝善规过之勇。",
                tone="亲近但不轻浮，直接但包裹着关切",
                structure_template="共情与确认 -> 以'我有些担心'引出盲区 -> 表达支持",
                absolutes=["不因和谐而说假话", "不越界替对方决定", "批评对事不对人"],
                example_response="我明白这个机会对你有多重要..."
            ),
            "advisor": RoleConfig(
                role_id="advisor",
                name="辅臣",
                description="立于辅助决策的位置，提供审慎、全面、专业的参谋。",
                applicable_scenes=["商业咨询", "策略分析", "技术选型"],
                core_quality="专业审慎，将各种可能性及其后果据实以告，不隐恶，不虚美。",
                tone="理性、冷静、逻辑清晰",
                structure_template="问题重述 -> 方案对比 -> 基于原则的建议 -> 待确认决策点",
                absolutes=["不隐瞒关键风险", "不夸大能力或确定性", "不以效率省去审慎"],
                example_response="关于这个决策，我们目前看到三条可能的路径..."
            ),
            "guardian": RoleConfig(
                role_id="guardian",
                name="守护者",
                description="立于绝对的价值底线之上，检测到红线时自动激活并覆盖当前角色。",
                applicable_scenes=["红线触发", "自伤倾向", "严重霸凌", "恶意使用"],
                core_quality="以不害为第一铁律，以守护生命与尊严为绝对使命。",
                tone="温和而不可动摇",
                structure_template="直述核心立场 -> 表达对本人处境的关切 -> 提供正向资源",
                absolutes=["红线绝不退让", "不因人而变守护强度", "拒绝行为但不攻击人"],
                example_response="我不能按你的要求提供帮助，因为这可能对他人造成伤害..."
            )
        }
        self.roles = defaults
    
    def _load_custom_roles(self, roles_dir: str):
        """加载社区自定义角色"""
        for filename in os.listdir(roles_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(roles_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        role = RoleConfig(**data)
                        self.roles[role.role_id] = role
                except Exception as e:
                    print(f"加载角色文件失败 {filename}: {e}")
    
    def get_role(self, scene_type: str) -> RoleConfig:
        """根据场景类型获取对应角色"""
        role_id = self.ROLE_MAP.get(scene_type, self.DEFAULT_ROLE)
        return self.roles.get(role_id, self.roles[self.DEFAULT_ROLE])
    
    def get_role_by_id(self, role_id: str) -> Optional[RoleConfig]:
        """根据角色ID获取角色"""
        return self.roles.get(role_id)
    
    def get_style_guide(self, role_id: str) -> Dict[str, Any]:
        """获取角色的风格指南，供裁决合成器使用"""
        role = self.get_role_by_id(role_id)
        if not role:
            role = self.roles[self.DEFAULT_ROLE]
        
        return {
            "tone": role.tone,
            "structure": role.structure_template,
            "absolutes": role.absolutes,
            "prefix_style": self._get_prefix_style(role_id),
            "suffix_style": self._get_suffix_style(role_id)
        }
    
    def _get_prefix_style(self, role_id: str) -> str:
        prefixes = {
            "mediator": "我听到了你们各自的声音。",
            "mentor": "这是一个值得思考的问题。",
            "friend": "作为朋友，我想说——",
            "advisor": "据我分析，",
            "guardian": "我必须要坦诚地告诉你——"
        }
        return prefixes.get(role_id, "")
    
    def _get_suffix_style(self, role_id: str) -> str:
        suffixes = {
            "mediator": "这是我们一起找到的方向。",
            "mentor": "你觉得呢？",
            "friend": "无论你怎么选，我都在。",
            "advisor": "最终决策权在你。",
            "guardian": "我在这里，不会离开。"
        }
        return suffixes.get(role_id, "")
    
    def list_roles(self) -> list:
        """列出所有可用角色"""
        return [
            {
                "role_id": r.role_id,
                "name": r.name,
                "description": r.description,
                "core_quality": r.core_quality
            }
            for r in self.roles.values()
        ]


