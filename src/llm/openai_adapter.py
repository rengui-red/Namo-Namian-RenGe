"""
OpenAI API适配器
支持OpenAI及所有兼容OpenAI接口的服务（如Azure OpenAI、本地vLLM等）。
"""

import time
import os
from typing import Optional, Dict, Any
from .base import LLMClient, LLMResponse


class OpenAIAdapter(LLMClient):
    """
    OpenAI API适配器。
    
    使用方式:
        client = OpenAIAdapter(model="gpt-4o", api_key="sk-...")
        response = client.generate("你好")
    
    也支持通过环境变量 OPENAI_API_KEY 和 OPENAI_BASE_URL 配置。
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        super().__init__(model=model, api_key=api_key, **kwargs)
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = base_url or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

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
                "使用OpenAI适配器需要安装openai库: pip install openai"
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



