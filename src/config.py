"""
配置管理模块 — 南无那面的中枢神经
统一加载、校验与提供所有环境变量配置，避免分散在各模块中的硬编码与不一致。

使用方式:
    from src.config import config
    llm_provider = config.llm_provider
"""

import os
import logging
from dataclasses import dataclass, field
from typing import Optional, List

logger = logging.getLogger("Namian.Config")


@dataclass
class LLMConfig:
    """LLM适配器配置"""
    provider: str = "mock"                  # mock / openai / deepseek / local
    model: str = "deepseek-chat"           # 模型名称
    temperature: float = 0.7               # 温度参数
    max_tokens: int = 2048                 # 最大生成token数
    request_timeout: int = 60              # 请求超时（秒）

    # OpenAI 配置
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"

    # DeepSeek 配置
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"

    # 本地Ollama配置
    local_base_url: str = "http://localhost:11434"


@dataclass
class SecurityConfig:
    """安全配置"""
    api_keys: List[str] = field(default_factory=list)
    cors_origins: List[str] = field(default_factory=lambda: ["*"])


@dataclass
class StorageConfig:
    """存储配置"""
    memory_path: str = "data/memories.json"
    knowledge_graph_path: str = "data/knowledge_graph.json"


@dataclass
class ServerConfig:
    """服务器配置"""
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    log_level: str = "INFO"


@dataclass
class AppConfig:
    """
    南无那面全局配置。
    所有配置项均可通过环境变量覆盖，提供合理的默认值。
    """
    llm: LLMConfig = field(default_factory=LLMConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    server: ServerConfig = field(default_factory=ServerConfig)


def load_config() -> AppConfig:
    """
    从环境变量加载全局配置。

    环境变量映射：
        LLM_PROVIDER       → llm.provider
        LLM_MODEL          → llm.model
        LLM_TEMPERATURE    → llm.temperature
        LLM_MAX_TOKENS     → llm.max_tokens
        LLM_TIMEOUT        → llm.request_timeout
        OPENAI_API_KEY     → llm.openai_api_key
        OPENAI_BASE_URL    → llm.openai_base_url
        DEEPSEEK_API_KEY   → llm.deepseek_api_key
        DEEPSEEK_BASE_URL  → llm.deepseek_base_url
        LOCAL_LLM_BASE_URL → llm.local_base_url
        API_KEY            → security.api_keys (逗号分隔)
        CORS_ORIGINS       → security.cors_origins (逗号分隔)
        MEMORY_STORAGE_PATH → storage.memory_path
        KG_STORAGE_PATH    → storage.knowledge_graph_path
        HOST               → server.host
        PORT               → server.port
        LOG_LEVEL          → server.log_level
        DEBUG              → server.debug (true/1 开启)
    """
    config = AppConfig()

    # ── LLM配置 ──
    config.llm.provider = os.environ.get("LLM_PROVIDER", "mock").strip().lower()
    config.llm.model = os.environ.get("LLM_MODEL", "deepseek-chat").strip()
    config.llm.temperature = _float_env("LLM_TEMPERATURE", 0.7)
    config.llm.max_tokens = _int_env("LLM_MAX_TOKENS", 2048)
    config.llm.request_timeout = _int_env("LLM_TIMEOUT", 60)
    config.llm.openai_api_key = os.environ.get("OPENAI_API_KEY", "")
    config.llm.openai_base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    config.llm.deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    config.llm.deepseek_base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    config.llm.local_base_url = os.environ.get("LOCAL_LLM_BASE_URL", "http://localhost:11434")

    # ── 安全配置 ──
    raw_keys = os.environ.get("API_KEY", "").strip()
    config.security.api_keys = [k.strip() for k in raw_keys.split(",") if k.strip()] if raw_keys else []
    raw_origins = os.environ.get("CORS_ORIGINS", "*").strip()
    config.security.cors_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

    # ── 存储配置 ──
    config.storage.memory_path = os.environ.get("MEMORY_STORAGE_PATH", "data/memories.json")
    config.storage.knowledge_graph_path = os.environ.get("KG_STORAGE_PATH", "data/knowledge_graph.json")

    # ── 服务器配置 ──
    config.server.host = os.environ.get("HOST", "0.0.0.0")
    config.server.port = _int_env("PORT", 5000)
    config.server.debug = os.environ.get("DEBUG", "").strip().lower() in ("true", "1", "yes")
    config.server.log_level = os.environ.get("LOG_LEVEL", "INFO").strip().upper()

    _validate_config(config)
    _log_config(config)
    return config


def _validate_config(config: AppConfig):
    """校验配置合法性"""
    valid_providers = ("mock", "openai", "deepseek", "local")
    if config.llm.provider not in valid_providers:
        raise ValueError(f"LLM_PROVIDER 必须为 {valid_providers} 之一，当前值: {config.llm.provider}")

    if config.llm.temperature < 0 or config.llm.temperature > 2:
        raise ValueError(f"LLM_TEMPERATURE 必须在 0-2 之间，当前值: {config.llm.temperature}")

    if config.llm.max_tokens < 1:
        raise ValueError(f"LLM_MAX_TOKENS 必须大于 0，当前值: {config.llm.max_tokens}")

    if config.llm.provider == "openai" and not config.llm.openai_api_key:
        logger.warning("LLM_PROVIDER=openai 但未设置 OPENAI_API_KEY，API调用将失败")

    if config.llm.provider == "deepseek" and not config.llm.deepseek_api_key:
        logger.warning("LLM_PROVIDER=deepseek 但未设置 DEEPSEEK_API_KEY，API调用将失败")

    if config.security.api_keys:
        logger.info(f"API认证已启用，共 {len(config.security.api_keys)} 个密钥")
    else:
        logger.warning("未配置 API_KEY，API认证已禁用。生产环境请务必设置。")

    if config.server.debug:
        logger.warning("DEBUG模式已开启，请勿在生产环境使用。")


def _log_config(config: AppConfig):
    """记录当前配置（隐藏敏感信息）"""
    logger.info("=" * 50)
    logger.info("南无那面 配置加载完成")
    logger.info(f"  LLM Provider : {config.llm.provider}")
    logger.info(f"  LLM Model    : {config.llm.model}")
    logger.info(f"  Temperature  : {config.llm.temperature}")
    logger.info(f"  Max Tokens   : {config.llm.max_tokens}")
    logger.info(f"  Timeout      : {config.llm.request_timeout}s")
    logger.info(f"  Server       : {config.server.host}:{config.server.port}")
    logger.info(f"  Log Level    : {config.server.log_level}")
    logger.info(f"  API Auth     : {'已启用' if config.security.api_keys else '已禁用'}")
    logger.info(f"  Debug Mode   : {'开启' if config.server.debug else '关闭'}")
    logger.info("=" * 50)


def _float_env(key: str, default: float) -> float:
    try:
        return float(os.environ.get(key, str(default)))
    except ValueError:
        logger.warning(f"环境变量 {key} 值无效，使用默认值 {default}")
        return default


def _int_env(key: str, default: int) -> int:
    try:
        return int(os.environ.get(key, str(default)))
    except ValueError:
        logger.warning(f"环境变量 {key} 值无效，使用默认值 {default}")
        return default


# ── 全局配置单例 ──
config: AppConfig = load_config()




