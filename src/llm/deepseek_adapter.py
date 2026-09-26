"""
DeepSeek API适配器
支持DeepSeek-V3、DeepSeek-R1等模型。
"""

import time
import os
from typing import Optional
from .base import LLMClient, LLMResponse


class DeepSeekAdapter(LLMClient):
    """
    DeepSeek API适配器。
    
    使用方式:
        client = DeepSeekAdapter(model="deepseek-chat", api_key="sk-...")
        response = client.generate("你好")
    
    也支持通过环境变量 DEEPSEEK_API_KEY 配置。
    """

    def __init__(
        self,
        model: str = "deepseek-chat",
        api_key: Optional[str] = None,
        base_url: str = "https://api.deepseek.com",
        **kwargs
    ):
        super().__init__(model=model, api_key=api_key, **kwargs)
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self.base_url = base_url

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> LLMResponse:
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "使用DeepSeek适配器需要安装openai库: pip install openai"
            )

        client = OpenAI(api_key=self.api_key, base_url=self.base_url)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        elapsed = (time.time() - start) * 1000

        choice = response.choices[0]
        return LLMResponse(
            content=choice.message.content or "",
            model=self.model,
            finish_reason=choice.finish_reason or "stop",
            usage={
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                "total_tokens": response.usage.total_tokens if response.usage else 0,
            },
            latency_ms=elapsed
        )


