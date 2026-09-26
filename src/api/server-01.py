"""
南无那面 · API服务
提供RESTful API接口，让南无那面可以被任何应用调用。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

from perception.redline_scanner import RedlineScanner
from perception.emotion_analyzer import EmotionAnalyzer
from perception.scene_classifier import SceneClassifier
from engine.task_network import TaskNetwork
from engine.ren_network import RenNetwork, JudgmentLevel
from engine.arbiter import Arbiter
from roles.role_loader import RoleLoader
from knowledge.kg_simple import SimpleKnowledgeGraph
from memory.memory_manager import MemoryManager


app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Namian.API")


class NamianAgent:
    """南无那面智能体 - 将所有模块串联为一个完整的数字生命"""
    
    def __init__(self):
        logger.info("南无那面 正在初始化...")
        
        self.scanner = RedlineScanner()
        self.emotion_analyzer = EmotionAnalyzer()
        self.scene_classifier = SceneClassifier()
        self.task_network = TaskNetwork()
        self.ren_network = RenNetwork(redline_scanner=self.scanner)
        self.role_loader = RoleLoader()
        self.knowledge_graph = SimpleKnowledgeGraph()
        self.memory_manager = MemoryManager(storage_path="data/memories.json")
        self.arbiter = Arbiter(role_loader=self.role_loader)
        
        self.ren_network.kg = self.knowledge_graph
        
        logger.info("南无那面 初始化完成。凡我所算，以仁为界。凡我所向，南无那面。")
    
    def chat(self, user_id: str, message: str, conversation_id: str = None) -> Dict:
        """
        处理一次完整的对话轮次。
        
        Args:
            user_id: 用户标识
            message: 用户输入
            conversation_id: 会话标识
        
        Returns:
            包含响应和元数据的完整字典
        """
        # 获取用户记忆上下文
        memory_context = self.memory_manager.get_relevant_context(user_id)
        
        # 感知层：分析输入
        scene = self.scene_classifier.classify(message)
        emotion = self.emotion_analyzer.analyze(message)
        vuln_flags = self.emotion_analyzer.detect_vulnerability(message)
        redline_alerts = self.scanner.scan(message)
        
        # 构建情境向量
        situation = {
            "scene_type": scene.scene_type,
            "active_role": self.role_loader.ROLE_MAP.get(scene.scene_type, "friend"),
            "emotion_vector": {
                "anger": emotion.anger,
                "sadness": emotion.sadness,
                "fear": emotion.fear,
                "shame": emotion.shame,
                "hope": emotion.hope,
                "despair": emotion.despair
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
        
        # 引擎层：生成 + 审计 + 合成
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


# 全局智能体实例
agent = NamianAgent()


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "南无那面 正在呼吸",
        "version": "1.0.0",
        "message": "凡我所算，以仁为界。凡我所向，南无那面。"
    })


@app.route('/api/v1/chat', methods=['POST'])
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


