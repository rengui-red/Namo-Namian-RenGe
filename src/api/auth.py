"""
API认证中间件 — 南无那面的山门守卫
基于 X-API-Key 的简单认证机制，保护公开API端点不被未授权调用。

使用方式:
    from src.api.auth import require_auth
    app.before_request(require_auth)
"""

import os
import logging
from functools import wraps
from flask import request, jsonify, current_app

logger = logging.getLogger("Namian.Auth")


class APIAuth:
    """
    API密钥认证管理器。
    从环境变量 API_KEY 中加载有效密钥列表（逗号分隔）。
    若未配置任何密钥，则允许所有请求（开发模式）。
    """

    def __init__(self):
        self._valid_keys: set = set()
        self._enabled: bool = False
        self._load_keys()
        self._public_paths: set = {"/health", "/"}
        self._public_prefixes: tuple = ("/static/",)

    def _load_keys(self):
        """从环境变量加载有效API密钥"""
        raw = os.environ.get("API_KEY", "").strip()
        if raw:
            self._valid_keys = {k.strip() for k in raw.split(",") if k.strip()}
            self._enabled = True
            logger.info(f"API认证已启用，已加载 {len(self._valid_keys)} 个有效密钥")
        else:
            self._enabled = False
            logger.warning("未配置 API_KEY 环境变量，API认证已禁用。"
                           "生产环境请务必设置 API_KEY。")

    def is_enabled(self) -> bool:
        return self._enabled

    def is_public_path(self, path: str) -> bool:
        """判断路径是否为公开路径（无需认证）"""
        if path in self._public_paths:
            return True
        if path.startswith(self._public_prefixes):
            return True
        return False

    def validate_key(self, api_key: str) -> bool:
        """验证API密钥是否有效"""
        if not self._enabled:
            return True
        return api_key in self._valid_keys

    def get_key_from_request(self) -> str:
        """从请求中提取API密钥"""
        # 优先从 X-API-Key 头部获取
        api_key = request.headers.get("X-API-Key", "")
        if api_key:
            return api_key.strip()
        # 其次从 Authorization: Bearer <key> 获取
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[7:].strip()
        # 最后从查询参数获取（不推荐，仅用于兼容）
        return request.args.get("api_key", "").strip()


# 全局单例
_auth_instance: APIAuth = None


def get_auth() -> APIAuth:
    """获取全局认证实例"""
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = APIAuth()
    return _auth_instance


def require_auth():
    """
    Flask before_request 钩子。
    对非公开路径进行API密钥验证。
    认证失败时返回温而厉的降级响应，而非冷冰冰的401。
    """
    auth = get_auth()

    # 如果认证未启用，跳过
    if not auth.is_enabled():
        return None

    # 公开路径跳过
    if auth.is_public_path(request.path):
        return None

    # 提取并验证API密钥
    api_key = auth.get_key_from_request()
    if api_key and auth.validate_key(api_key):
        return None

    # 认证失败 — 温而厉的降级响应
    logger.warning(f"API认证失败: path={request.path}, ip={request.remote_addr}")
    return jsonify({
        "response": (
            "南无那面感受到了一次未经邀请的叩门。\n\n"
            "这不是拒绝，而是一种守护——我需要确认来者是带着善意的。\n"
            "请在请求头中携带 X-API-Key，或联系社区获取访问密钥。\n\n"
            "凡我所算，以仁为界。凡我所向，南无那面。\n"
            "[状态：需要API密钥 | 请参阅文档]"
        ),
        "error": "unauthorized",
        "status": 401
    }), 401



