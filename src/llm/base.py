"""
LLM适配器基类
定义所有适配器必须实现的统一接口。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class LLMResponse:
    """LLM统一响应结构"""
    content: str                                    # 生成的文本
    model: str = ""                                 # 使用的模型名称
    finish_reason: str = "stop"                     # 结束原因：stop / length / error
    usage: Dict[str, int] = field(default_factory=dict)  # token用量
    latency_ms: float = 0.0                         # 延迟（毫秒）


class LLMClient(ABC):
    """
    LLM客户端抽象基类。
    所有适配器必须实现 generate 方法。
    引擎层的 TaskNetwork 和 RenNetwork 依赖此接口。
    """

    def __init__(self, model: str, api_key: Optional[str] = None, **kwargs):
        self.model = model
        self.api_key = api_key

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> LLMResponse:
        """
        生成响应。
        
        Args:
            prompt: 用户提示
            system_prompt: 系统提示词（可选）
            temperature: 温度参数
            max_tokens: 最大生成token数
            **kwargs: 其他模型特定参数
        
        Returns:
            LLMResponse: 统一响应结构
        """
        ...

    def health_check(self) -> bool:
        """健康检查：快速测试API是否可用"""
        try:
            response = self.generate("Hello", max_tokens=16)
            return len(response.content) > 0
        except Exception:
            return False


