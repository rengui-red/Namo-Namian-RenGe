"""
Mock适配器 - 用于本地测试与模块联调
不调用任何外部API，返回预设或简单的回声响应。
"""

import time
from typing import Optional
from .base import LLMClient, LLMResponse


class MockAdapter(LLMClient):
    """
    Mock适配器。
    用于在没有API Key或离线环境下的开发调试。
    
    使用方式:
        client = MockAdapter()
        response = client.generate("你好")
    """

    def __init__(self, model: str = "mock-v1", **kwargs):
        super().__init__(model=model, **kwargs)
        self._call_count = 0

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> LLMResponse:
        self._call_count += 1

        # 模拟网络延迟
        time.sleep(0.05)

        # 如果提供了系统提示词，在响应中体现
        prefix = ""
        if system_prompt and "南无那面" in system_prompt:
            prefix = "[仁格模式] "

        # 简单回声 + 时间戳，便于调试
        content = f"{prefix}[Mock LLM #{self._call_count}] 我收到了你的消息：{prompt[:200]}"

        return LLMResponse(
            content=content,
            model=self.model,
            finish_reason="stop",
            usage={"prompt_tokens": len(prompt), "completion_tokens": len(content), "total_tokens": len(prompt) + len(content)},
            latency_ms=50.0
        )


