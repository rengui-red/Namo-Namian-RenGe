"""
长程记忆管理器 - 南无那面的海马体
追踪多轮对话中的用户状态、信任建立与价值倾向。
"""

import hashlib
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from collections import OrderedDict


@dataclass
class UserMemory:
    """用户记忆单元"""
    user_id: str
    trust_index: float = 0.5              # 信任指数 0-1
    key_experiences: List[Dict] = field(default_factory=list)
    value_tendencies: List[str] = field(default_factory=list)
    interaction_count: int = 0
    last_role_activated: str = "friend"
    last_emotion_dominant: str = ""
    conversation_summary: str = ""
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


class MemoryManager:
    """
    长程记忆管理器
    在单次会话中追踪用户状态，支持跨会话的记忆存储与检索。
    """
    
    MAX_MEMORIES = 1000          # 最大记忆数量
    MAX_EXPERIENCES = 20         # 每个用户最大关键经历数
    SUMMARIZE_THRESHOLD = 5      # 每N轮对话做一次摘要
    
    def __init__(self, storage_path: str = None):
        self.memories: Dict[str, UserMemory] = OrderedDict()
        self.storage_path = storage_path
        
        # 从磁盘加载已有记忆
        if storage_path:
            self._load_from_disk()
    
    def get_or_create(self, user_id: str) -> UserMemory:
        """获取或创建用户记忆"""
        if user_id not in self.memories:
            self.memories[user_id] = UserMemory(user_id=user_id)
        
        # LRU淘汰
        if len(self.memories) > self.MAX_MEMORIES:
            oldest_key = next(iter(self.memories))
            del self.memories[oldest_key]
        
        return self.memories[user_id]
    
    def update_after_turn(self, user_id: str, 
                          user_input: str,
                          emotion: Dict[str, float],
                          role_activated: str,
                          trust_delta: float = 0.0,
                          experience: Optional[Dict] = None):
        """
        每轮对话后更新记忆。
        
        Args:
            user_id: 用户标识
            user_input: 用户输入
            emotion: 情绪向量
            role_activated: 激活的角色
            trust_delta: 信任变化量
            experience: 关键经历（如果有）
        """
        memory = self.get_or_create(user_id)
        
        # 更新基础统计
        memory.interaction_count += 1
        memory.last_role_activated = role_activated
        memory.updated_at = time.time()
        
        # 更新主导情绪
        if isinstance(emotion, dict):
            emotions_sorted = sorted(emotion.items(), key=lambda x: x[1], reverse=True)
            if emotions_sorted and emotions_sorted[0][1] > 0.3:
                memory.last_emotion_dominant = emotions_sorted[0][0]
        
        # 更新信任指数
        if trust_delta != 0.0:
            memory.trust_index = max(0.0, min(1.0, memory.trust_index + trust_delta))
        else:
            # 自动信任追踪
            self._auto_track_trust(memory, user_input, emotion)
        
        # 添加关键经历
        if experience:
            memory.key_experiences.append({
                "timestamp": time.time(),
                **experience
            })
            if len(memory.key_experiences) > self.MAX_EXPERIENCES:
                memory.key_experiences = memory.key_experiences[-self.MAX_EXPERIENCES:]
        
        # 定期摘要
        if memory.interaction_count % self.SUMMARIZE_THRESHOLD == 0:
            self._update_summary(memory, user_input)
        
        # 持久化
        if self.storage_path:
            self._save_to_disk()
    
    def _auto_track_trust(self, memory: UserMemory, user_input: str, emotion: Dict):
        """自动追踪信任变化"""
        delta = 0.0
        
        # 用户表达脆弱性 → 信任上升
        vulnerability_signals = ["难过", "害怕", "告诉你", "秘密", "只有你", "信任你"]
        if any(signal in user_input for signal in vulnerability_signals):
            delta += 0.05
        
        # 用户自我坦露 → 信任上升
        self_disclosure = ["其实我", "说实话", "不瞒你说", "我一直", "我心里"]
        if any(signal in user_input for signal in self_disclosure):
            delta += 0.03
        
        # 用户表达感激 → 信任上升
        gratitude = ["谢谢", "感谢", "多亏你", "有你真好", "帮了大忙"]
        if any(signal in user_input for signal in gratitude):
            delta += 0.08
        
        # 用户表达失望或不满 → 信任微降
        disappointment = ["你不懂", "你没理解", "算了", "没用"]
        if any(signal in user_input for signal in disappointment):
            delta -= 0.02
        
        memory.trust_index = max(0.0, min(1.0, memory.trust_index + delta))
    
    def _update_summary(self, memory: UserMemory, latest_input: str):
        """更新对话摘要"""
        summary_parts = [
            f"用户已进行{memory.interaction_count}轮对话",
            f"最近主导情绪: {memory.last_emotion_dominant}",
            f"信任指数: {memory.trust_index:.2f}",
            f"最近激活角色: {memory.last_role_activated}"
        ]
        if memory.key_experiences:
            recent_exp = memory.key_experiences[-1]
            summary_parts.append(f"最近关键经历: {recent_exp.get('summary', '')}")
        
        memory.conversation_summary = "；".join(summary_parts)
    
    def get_trust_level(self, user_id: str) -> str:
        """获取信任等级"""
        memory = self.get_or_create(user_id)
        if memory.trust_index < 0.3:
            return "初识"
        elif memory.trust_index < 0.6:
            return "建立中"
        elif memory.trust_index < 0.8:
            return "信任"
        else:
            return "深度信任"
    
    def get_relevant_context(self, user_id: str) -> Dict[str, Any]:
        """获取与当前对话相关的上下文"""
        memory = self.get_or_create(user_id)
        return {
            "trust_level": self.get_trust_level(user_id),
            "trust_index": memory.trust_index,
            "last_emotion": memory.last_emotion_dominant,
            "interaction_count": memory.interaction_count,
            "recent_experiences": memory.key_experiences[-3:] if memory.key_experiences else [],
            "value_tendencies": memory.value_tendencies,
            "conversation_summary": memory.conversation_summary
        }
    
    def add_value_tendency(self, user_id: str, value: str):
        """添加用户价值倾向"""
        memory = self.get_or_create(user_id)
        if value not in memory.value_tendencies:
            memory.value_tendencies.append(value)
            if len(memory.value_tendencies) > 10:
                memory.value_tendencies = memory.value_tendencies[-10:]
    
    def _save_to_disk(self):
        """持久化到磁盘"""
        import json
        try:
            data = {
                uid: {
                    "user_id": m.user_id,
                    "trust_index": m.trust_index,
                    "key_experiences": m.key_experiences,
                    "value_tendencies": m.value_tendencies,
                    "interaction_count": m.interaction_count,
                    "last_role_activated": m.last_role_activated,
                    "last_emotion_dominant": m.last_emotion_dominant,
                    "conversation_summary": m.conversation_summary,
                    "updated_at": m.updated_at
                }
                for uid, m in self.memories.items()
            }
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"记忆持久化失败: {e}")
    
    def _load_from_disk(self):
        """从磁盘加载记忆"""
        import json
        import os
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for uid, mdata in data.items():
                memory = UserMemory(
                    user_id=mdata["user_id"],
                    trust_index=mdata.get("trust_index", 0.5),
                    key_experiences=mdata.get("key_experiences", []),
                    value_tendencies=mdata.get("value_tendencies", []),
                    interaction_count=mdata.get("interaction_count", 0),
                    last_role_activated=mdata.get("last_role_activated", "friend"),
                    last_emotion_dominant=mdata.get("last_emotion_dominant", ""),
                    conversation_summary=mdata.get("conversation_summary", "")
                )
                self.memories[uid] = memory
        except Exception as e:
            print(f"记忆加载失败: {e}")


