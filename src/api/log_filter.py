"""
日志脱敏中间件 — 南无那面的慎独日志
自动过滤请求与响应中的敏感信息，确保用户输入内容和API密钥不进入日志系统。
实现“不器”原则在日志层的延伸——用户数据不是可被记录的客体，而是应被守护的数字人格。

使用方式:
    from src.api.log_filter import LogFilter
    app.before_request(LogFilter.filter_request)
    app.after_request(LogFilter.filter_response)
"""

import re
import logging
from flask import request

logger = logging.getLogger("Namian.LogFilter")


class LogFilter:
    """日志脱敏过滤器"""

    # 需要从请求头中移除的敏感字段
    SENSITIVE_HEADERS = {
        "x-api-key",
        "authorization",
        "cookie",
        "set-cookie",
    }

    # 需要从请求体中移除的敏感字段
    SENSITIVE_BODY_FIELDS = {
        "api_key",
        "password",
        "token",
        "secret",
        "message",
        "user_input",
    }

    # 用户输入内容的最大记录长度（超过部分截断）
    MAX_BODY_LOG_LENGTH = 100

    @classmethod
    def filter_request(cls):
        """在请求处理前，清洗日志中的敏感信息"""
        # 记录最简请求信息，不含敏感头
        safe_headers = {
            k: v for k, v in request.headers
            if k.lower() not in cls.SENSITIVE_HEADERS
        }
        logger.debug(
            f"[请求] {request.method} {request.path} "
            f"from={request.remote_addr} "
            f"content_type={request.content_type}"
        )
        # 不记录请求体内容——用户的话语是私密的
        return None

    @classmethod
    def filter_response(cls, response):
        """在响应返回前，确保日志中不记录用户数据"""
        status_code = response.status_code
        logger.debug(
            f"[响应] {request.method} {request.path} → {status_code}"
        )
        # 不记录响应体内容
        return response

    @classmethod
    def sanitize_body_for_log(cls, body: dict, max_length: int = None) -> dict:
        """
        对请求体进行脱敏处理，返回可安全记录的版本。
        用于需要记录部分请求信息（如错误排查）的场景。
        """
        if max_length is None:
            max_length = cls.MAX_BODY_LOG_LENGTH

        if not isinstance(body, dict):
            # 非字典类型，截断后返回
            safe = str(body)[:max_length]
            return {"_truncated": safe}

        safe = {}
        for key, value in body.items():
            if key in cls.SENSITIVE_BODY_FIELDS:
                safe[key] = "[已脱敏]"
            elif isinstance(value, str) and len(value) > max_length:
                safe[key] = value[:max_length] + "..."
            else:
                safe[key] = value
        return safe



