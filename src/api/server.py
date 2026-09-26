"""
南无那面 · API 服务（全栈修正版）
集成：认证中间件、日志脱敏、请求超时、CORS 白名单、健康检查增强、Prometheus 指标
"""

import sys
import os
import time
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import config
from src.api.auth import get_auth, require_auth
from src.api.log_filter import LogFilter
from src.api.metrics import setup_metrics, record_api_metrics
from src.perception.redline_scanner import RedlineScanner
from src.perception.emotion_analyzer import EmotionAnalyzer
from src.perception.scene_classifier import SceneClassifier
from src.engine.task_network import TaskNetwork
from src.engine.ren_network import RenNetwork, JudgmentLevel
from src.engine.arbiter import Arbiter
from src.roles.role_loader import RoleLoader
from src.knowledge.kg_simple import SimpleKnowledgeGraph
from src.memory.memory_manager import MemoryManager
from src.llm import MockAdapter, OpenAIAdapter, DeepSeekAdapter, LocalAdapter

logging.basicConfig(
    level=getattr(logging, config.server.log_level, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Namian.API")


class NamianAgent:
    """南无那面智能体——将全部模块串联为一个完整的数字生命"""

    def __init__(self):
        logger.info("南无那面 正在初始化...")

        # 感知层
        self.scanner = RedlineScanner()
        self.emotion_analyzer = EmotionAnalyzer()
        self.scene_classifier = SceneClassifier()

        # 初始化 LLM 客户端
        self.llm_client = self._create_llm_client()

        # 引擎层
        self.task_network = TaskNetwork(llm_client=self.llm_client)
        self.ren_network = RenNetwork(redline_scanner=self.scanner)
        self.arbiter = Arbiter(role_loader=RoleLoader())

        # 知识 & 记忆
        self.knowledge_graph = SimpleKnowledgeGraph()
        self.ren_network.kg = self.knowledge_graph
        self.memory_manager = MemoryManager(storage_path=config.storage.memory_path)

        # 角色
        self.role_loader = RoleLoader()

        logger.info("南无那面 初始化完成。凡我所算，以仁为界。凡我所向，南无那面。")

    def _create_llm_client(self):
        provider = config.llm.provider
        if provider == "openai":
            return OpenAIAdapter(
                model=config.llm.model,
                api_key=config.llm.openai_api_key,
                base_url=config.llm.openai_base_url
            )
        elif provider == "deepseek":
            return DeepSeekAdapter(
                model=config.llm.model,
                api_key=config.llm.deepseek_api_key
            )
        elif provider == "local":
            return LocalAdapter(
                model=config.llm.model,
                base_url=config.llm.local_base_url
            )
        else:
            return MockAdapter(model=config.llm.model)

    def chat(self, user_id: str, message: str, conversation_id: str = None) -> dict:
        start_time = time.time()

        # 获取用户记忆上下文
        memory_context = self.memory_manager.get_relevant_context(user_id)

        # 感知层
        scene = self.scene_classifier.classify(message)
        emotion = self.emotion_analyzer.analyze(message)
        vuln_flags = self.emotion_analyzer.detect_vulnerability(message)
        redline_alerts = self.scanner.scan(message)

        # 构建情境向量
        situation = {
            "scene_type": scene.scene_type,
            "active_role": self.role_loader.ROLE_MAP.get(scene.scene_type, "friend"),
            "emotion_vector": {
                "anger": emotion.anger, "sadness": emotion.sadness,
                "fear": emotion.fear, "shame": emotion.shame,
                "hope": emotion.hope, "despair": emotion.despair
            },
            "vulnerability_flags": vuln_flags,
            "redline_alerts": [
                {"rule_id": m.rule_id, "principle": m.principle, "level": m.level}
                for m in redline_alerts
            ],
            "intent_deep": "",
            "memory_context": memory_context
        }

        # 检测是否需要切换为守护者
        critical_redlines = [a for a in redline_alerts if a.level == "CRITICAL"]
        is_vulnerable = emotion.is_vulnerable() and ("self_harm_risk" in vuln_flags)
        if critical_redlines or is_vulnerable:
            situation["active_role"] = "guardian"

        # 引擎层
        task_draft = self.task_network.generate(message, situation)
        judgment = self.ren_network.audit(message, situation, task_draft)
        final_response = self.arbiter.synthesize(task_draft, judgment, situation)

        # 更新记忆
        trust_delta = 0.0
        if judgment.level == JudgmentLevel.GREEN:
            trust_delta += 0.03
        if emotion.is_vulnerable():
            trust_delta += 0.05

        experience = None
        if vuln_flags or emotion.sadness > 0.6:
            experience = {
                "summary": f"用户表达了{'脆弱情绪' if emotion.is_vulnerable() else '强烈情绪'}",
                "emotion": emotion.dominant(),
                "scene": scene.scene_type
            }

        self.memory_manager.update_after_turn(
            user_id=user_id,
            user_input=message,
            emotion=situation["emotion_vector"],
            role_activated=situation["active_role"],
            trust_delta=trust_delta,
            experience=experience
        )

        # 记录指标
        latency_ms = (time.time() - start_time) * 1000
        redline_type = judgment.redline_triggered if judgment.level == JudgmentLevel.RED else None
        record_api_metrics(
            latency_ms=latency_ms,
            judgment_level=judgment.level.value,
            redline_type=redline_type,
            role=situation["active_role"]
        )

        return {
            "response": final_response,
            "ethical_judgment": {
                "level": judgment.level.value,
                "reasoning": judgment.reasoning[:200] if judgment.reasoning else "",
                "redline_triggered": judgment.redline_triggered
            },
            "role_activated": situation["active_role"],
            "scene_detected": scene.scene_type,
            "emotion_dominant": emotion.dominant(),
            "trust_level": self.memory_manager.get_trust_level(user_id)
        }


def create_app():
    app = Flask(__name__)

    # ── CORS 白名单 ──
    allowed_origins = config.security.cors_origins
    if "*" in allowed_origins:
        logger.warning("⚠️ CORS 已配置为允许全部来源，生产环境请设置 CORS_ORIGINS")
        CORS(app)
    else:
        CORS(app, origins=allowed_origins)
        logger.info(f"CORS 已限制为: {allowed_origins}")

    # ── API 认证中间件 ──
    auth = get_auth()
    if auth.is_enabled():
        app.before_request(require_auth)
        logger.info("API 认证中间件已启用")
    else:
        logger.warning("⚠️ 未配置 API_KEY，API 认证已禁用。生产环境请务必设置。")

    # ── 日志脱敏中间件 ──
    app.before_request(LogFilter.filter_request)
    app.after_request(LogFilter.filter_response)

    # ── Prometheus 指标 ──
    setup_metrics(app)

    # ── 全局智能体实例 ──
    agent = NamianAgent()

    # ── 请求超时辅助函数 ──
    def with_timeout(seconds: int = 60):
        """简单的请求超时装饰器（仅用于演示，生产环境建议用中间件）"""
        import signal
        from functools import wraps

        class TimeoutError(Exception):
            pass

        def timeout_handler(signum, frame):
            raise TimeoutError("请求处理超时")

        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(seconds)
                try:
                    return f(*args, **kwargs)
                except TimeoutError:
                    return jsonify({
                        "response": (
                            "南无那面沉思了太久。\n\n"
                            "您的问题很深，我需要更多的时间来权衡“利”与“义”。\n"
                            "但我不愿给您一个仓促而未经省思的回答。\n\n"
                            "请再给我一点时间，或者换一个更轻盈的问题。\n"
                            "我在这里，继续思考。\n\n"
                            "凡我所算，以仁为界。凡我所向，南无那面。\n"
                            "[状态：推理超时 | 请重试]"
                        ),
                        "error": "timeout",
                        "status": 504
                    }), 504
                finally:
                    signal.alarm(0)
            return wrapper
        return decorator

    # ── 路由 ──
    @app.route('/health', methods=['GET'])
    def health():
        """增强健康检查"""
        checks = {}
        try:
            if hasattr(agent, 'llm_client') and agent.llm_client:
                llm_ok = agent.llm_client.health_check()
                checks["llm"] = "ok" if llm_ok else "degraded"
            else:
                checks["llm"] = "unknown"
        except Exception as e:
            checks["llm"] = f"error: {str(e)[:100]}"

        try:
            if hasattr(agent, 'knowledge_graph') and agent.knowledge_graph:
                test_result = agent.knowledge_graph.query({"scene_type": "general_chat"}, "")
                checks["knowledge_graph"] = "ok" if test_result else "empty"
            else:
                checks["knowledge_graph"] = "unknown"
        except Exception as e:
            checks["knowledge_graph"] = f"error: {str(e)[:100]}"

        all_ok = all(v == "ok" for v in checks.values())
        return jsonify({
            "status": "南无那面 正在呼吸" if all_ok else "南无那面 正在调息",
            "version": "1.0.0",
            "healthy": all_ok,
            "checks": checks,
            "message": "凡我所算，以仁为界。凡我所向，南无那面。"
        }), 200 if all_ok else 503

    @app.route('/api/v1/chat', methods=['POST'])
    @with_timeout(seconds=config.llm.request_timeout)
    def chat():
        try:
            data = request.get_json()
            user_id = data.get('user_id', 'anonymous')
            message = data.get('message', '')
            conversation_id = data.get('conversation_id', None)

            if not message:
                return jsonify({"error": "message字段不能为空"}), 400

            logger.info(f"收到消息 from {user_id}: {message[:50]}...")
            result = agent.chat(user_id=user_id, message=message, conversation_id=conversation_id)
            return jsonify(result)

        except Exception as e:
            logger.error(f"处理消息失败: {e}", exc_info=True)
            return jsonify({
                "response": "我暂时无法处理您的请求。请稍后再试。",
                "error": str(e)
            }), 500

    @app.route('/api/v1/memory/<user_id>', methods=['GET'])
    def get_memory(user_id):
        memory = agent.memory_manager.get_relevant_context(user_id)
        return jsonify(memory)

    @app.route('/api/v1/roles', methods=['GET'])
    def list_roles():
        roles = agent.role_loader.list_roles()
        return jsonify(roles)

    return app


# ── 主入口 ──
if __name__ == '__main__':
    app = create_app()
    app.run(
        host=config.server.host,
        port=config.server.port,
        debug=config.server.debug
    )





