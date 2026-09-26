"""
本地模型适配器 - 通过Ollama调用本地部署的开源模型
适用于Qwen、Llama、ChatGLM等在Ollama中部署的模型。

使用方式:
    client = LocalAdapter(model="qwen2.5:7b")
    response = client.generate("你好")
"""

import time
from typing import Optional
from .base import LLMClient, LLMResponse


class LocalAdapter(LLMClient):
    """
    本地Ollama适配器。
    需要先安装Ollama并拉取模型: ollama pull qwen2.5:7b
    """

    def __init__(
        self,
        model: str = "qwen2.5:7b",
        base_url: str = "http://localhost:11434",
        **kwargs
    ):
        super().__init__(model=model, **kwargs)
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
                "使用本地适配器需要安装openai库: pip install openai"
            )

        client = OpenAI(base_url=f"{self.base_url}/v1", api_key="ollama")

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



