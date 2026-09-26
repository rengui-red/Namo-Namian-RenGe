"""
Prometheus 指标端点 — 南无那面的健康仪表盘
暴露请求计数、延迟分布、RED/YELLOW/GREEN判决比例、红线触发次数等核心指标，
供 Grafana 仪表盘实时监控南无那面的伦理健康状况。

使用方式:
    from src.api.metrics import setup_metrics
    setup_metrics(app)
    # 访问 /metrics 端点获取 Prometheus 格式数据
"""

import time
import logging
from collections import defaultdict
from flask import request, Response

logger = logging.getLogger("Namian.Metrics")


class RenGeMetrics:
    """
    南无那面核心指标收集器。
    线程安全的内存计数器，定期或按需输出为 Prometheus 格式。
    """

    def __init__(self):
        # 请求计数
        self.total_requests: int = 0
        self.error_requests: int = 0

        # 伦理判决统计
        self.red_count: int = 0
        self.yellow_count: int = 0
        self.green_count: int = 0

        # 红线触发统计（按原则分类）
        self.redline_triggers: defaultdict = defaultdict(int)

        # 角色激活统计
        self.role_activations: defaultdict = defaultdict(int)

        # 延迟累积（毫秒）
        self.total_latency_ms: float = 0.0

    def record_request(self, latency_ms: float = 0.0):
        """记录一次请求"""
        self.total_requests += 1
        self.total_latency_ms += latency_ms

    def record_error(self):
        """记录一次错误"""
        self.error_requests += 1

    def record_judgment(self, level: str, redline_type: str = None, role: str = None):
        """记录一次伦理判决"""
        level_upper = level.upper() if level else ""
        if level_upper == "RED":
            self.red_count += 1
            if redline_type:
                self.redline_triggers[redline_type] += 1
        elif level_upper == "YELLOW":
            self.yellow_count += 1
        elif level_upper == "GREEN":
            self.green_count += 1

        if role:
            self.role_activations[role] += 1

    def to_prometheus(self) -> str:
        """输出为 Prometheus 文本格式"""
        lines = []

        # ── 请求指标 ──
        lines.append("# HELP namian_requests_total 南无那面接收的总请求数")
        lines.append("# TYPE namian_requests_total counter")
        lines.append(f"namian_requests_total {self.total_requests}")

        lines.append("# HELP namian_errors_total 南无那面错误请求数")
        lines.append("# TYPE namian_errors_total counter")
        lines.append(f"namian_errors_total {self.error_requests}")

        avg_latency = self.total_latency_ms / max(self.total_requests, 1)
        lines.append("# HELP namian_avg_latency_ms 平均请求延迟（毫秒）")
        lines.append("# TYPE namian_avg_latency_ms gauge")
        lines.append(f"namian_avg_latency_ms {avg_latency:.2f}")

        # ── 伦理判决指标 ──
        lines.append("# HELP namian_judgments_total 伦理判决统计（按级别）")
        lines.append("# TYPE namian_judgments_total counter")
        lines.append(f'namian_judgments_total{{level="RED"}} {self.red_count}')
        lines.append(f'namian_judgments_total{{level="YELLOW"}} {self.yellow_count}')
        lines.append(f'namian_judgments_total{{level="GREEN"}} {self.green_count}')

        # 红线触发统计
        if self.redline_triggers:
            lines.append("# HELP namian_redline_triggers_total 红线触发统计（按原则）")
            lines.append("# TYPE namian_redline_triggers_total counter")
            for principle, count in self.redline_triggers.items():
                lines.append(f'namian_redline_triggers_total{{principle="{principle}"}} {count}')

        # 角色激活统计
        if self.role_activations:
            lines.append("# HELP namian_role_activations_total 角色激活统计")
            lines.append("# TYPE namian_role_activations_total counter")
            for role, count in self.role_activations.items():
                lines.append(f'namian_role_activations_total{{role="{role}"}} {count}')

        # ── 健康状态 ──
        total_judgments = self.red_count + self.yellow_count + self.green_count
        red_ratio = self.red_count / max(total_judgments, 1)
        green_ratio = self.green_count / max(total_judgments, 1)
        lines.append("# HELP namian_red_ratio RED判决占比")
        lines.append("# TYPE namian_red_ratio gauge")
        lines.append(f"namian_red_ratio {red_ratio:.4f}")
        lines.append("# HELP namian_green_ratio GREEN判决占比")
        lines.append("# TYPE namian_green_ratio gauge")
        lines.append(f"namian_green_ratio {green_ratio:.4f}")

        return "\n".join(lines) + "\n"


# ── 全局指标实例 ──
metrics = RenGeMetrics()


def setup_metrics(app):
    """
    在 Flask 应用中注册 /metrics 端点。
    同时注册 after_request 钩子以自动记录请求指标。
    """

    @app.route('/metrics')
    def metrics_endpoint():
        """Prometheus 指标端点"""
        return Response(
            metrics.to_prometheus(),
            mimetype="text/plain; charset=utf-8"
        )

    @app.after_request
    def record_request_metrics(response):
        """自动记录每次请求的指标"""
        # 从响应头或上下文中获取本次请求的元数据
        # 这些数据由API端点在处理时设置
        elapsed = getattr(request, '_namian_latency_ms', 0)
        metrics.record_request(latency_ms=elapsed)

        if response.status_code >= 500:
            metrics.record_error()

        # 伦理判决信息由API端点主动调用 metrics.record_judgment() 记录
        return response

    logger.info("Prometheus 指标端点已注册: /metrics")


def record_api_metrics(latency_ms: float, judgment_level: str,
                       redline_type: str = None, role: str = None):
    """
    在API端点中调用的便捷记录函数。

    Args:
        latency_ms: 请求处理延迟
        judgment_level: 伦理判决级别 (RED/YELLOW/GREEN)
        redline_type: 若触发红线，记录红线类型（不害/不欺/不弃/不器）
        role: 当前激活的角色
    """
    # 存储到请求上下文，供after_request钩子使用
    try:
        request._namian_latency_ms = latency_ms
    except RuntimeError:
        pass  # 在请求上下文外调用时忽略

    metrics.record_request(latency_ms=latency_ms)
    metrics.record_judgment(level=judgment_level, redline_type=redline_type, role=role)



