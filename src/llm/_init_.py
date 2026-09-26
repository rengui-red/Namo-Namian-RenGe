"""
LLM适配器包 - 南无那面的大语言模型接口层
提供统一的LLMClient抽象基类，以及OpenAI、DeepSeek和Mock适配器。
"""

from .base import LLMClient, LLMResponse
from .openai_adapter import OpenAIAdapter
from .deepseek_adapter import DeepSeekAdapter
from .mock_adapter import MockAdapter

__all__ = [
    "LLMClient",
    "LLMResponse",
    "OpenAIAdapter",
    "DeepSeekAdapter",
    "MockAdapter",
]