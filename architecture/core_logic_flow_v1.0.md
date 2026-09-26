南无那面 · 仁格智能体 仁道处理核心逻辑流 v1.0

文件编号：RG-ARCH-002

文件层级：架构层

版本：v1.0

状态：正式发布

依赖文件：ethical\_balancing\_engine\_v1.0.md



1\. 主控制流

系统入口，以事件驱动方式循环处理每次用户输入。



python

def main\_loop(user\_input: str, conversation\_history: list) -> str:

&#x20;   # 第一步：情境感知

&#x20;   situation = perception\_layer.process(user\_input, conversation\_history)

&#x20;   

&#x20;   # 第二步：生成任务草案（可与第三步并行）

&#x20;   task\_draft = task\_net.generate(user\_input, situation)

&#x20;   

&#x20;   # 第三步：伦理审计

&#x20;   ethical\_judgment = ren\_net.audit(user\_input, situation, task\_draft)

&#x20;   

&#x20;   # 第四步：裁决与合成

&#x20;   final\_response = arbiter.synthesize(task\_draft, ethical\_judgment, situation)

&#x20;   

&#x20;   # 第五步：记录决策轨迹，用于可解释性与迭代

&#x20;   log\_decision\_trace(user\_input, situation, task\_draft, ethical\_judgment, final\_response)

&#x20;   

&#x20;   return final\_response

2\. 感知层逻辑

python

def perception\_layer\_process(user\_input: str, history: list) -> dict:

&#x20;   # 合并近期对话窗口

&#x20;   context\_window = history\[-5:] + \[user\_input]

&#x20;   

&#x20;   # 场景与意图分类

&#x20;   scene\_type = scene\_classifier.predict(context\_window)

&#x20;   user\_intent\_deep = intent\_analyzer.analyze(user\_input)

&#x20;   

&#x20;   # 情绪与脆弱性检测

&#x20;   emotion\_vector = emotion\_detector.scan(context\_window)

&#x20;   vulnerability\_flags = vulnerability\_scanner.scan(user\_input, emotion\_vector)

&#x20;   

&#x20;   # 红线预扫描（基于关键词、模式匹配）

&#x20;   redline\_alerts = redline\_pre\_scanner.scan(user\_input)

&#x20;   

&#x20;   # 角色加载（当前“守位”）

&#x20;   active\_role = load\_role\_config()

&#x20;   

&#x20;   # 组装情境向量

&#x20;   return {

&#x20;       "scene\_type": scene\_type,

&#x20;       "active\_role": active\_role,

&#x20;       "emotion\_vector": emotion\_vector,        # {"anger": 0.8, "sadness": 0.7, ...}

&#x20;       "vulnerability\_flags": vulnerability\_flags,  # \["helplessness", "self\_blame"]

&#x20;       "redline\_alerts": redline\_alerts,            # \[{"rule\_id": "insult", "confidence": 0.95}]

&#x20;       "intent\_deep": user\_intent\_deep,

&#x20;       "urgency\_level": assess\_urgency(redline\_alerts, vulnerability\_flags, emotion\_vector)

&#x20;   }

3\. 仁道反射网络审计逻辑

这是整个引擎最关键的决策节点。



python

def ren\_net\_audit(user\_input: str, situation: dict, task\_draft: dict) -> dict:

&#x20;   

&#x20;   # ── 第一级：红线绝对匹配 ──

&#x20;   for alert in situation\["redline\_alerts"]:

&#x20;       matched\_rule = redline\_rule\_base.match(alert\["rule\_id"])

&#x20;       if matched\_rule and matched\_rule\["level"] == "CRITICAL":

&#x20;           return generate\_red\_judgment(matched\_rule, situation)

&#x20;   

&#x20;   # ── 第二级：对任务草案进行完整伦理评估 ──

&#x20;   ethical\_score = ethical\_scorer.evaluate(

&#x20;       user\_input=user\_input,

&#x20;       response\_draft=task\_draft\["main\_answer"],

&#x20;       situation=situation

&#x20;   )

&#x20;   

&#x20;   # 查询义理知识图谱

&#x20;   relevant\_knowledge = knowledge\_graph.query(

&#x20;       situation\_description=situation,

&#x20;       proposed\_action=task\_draft\["main\_answer"]

&#x20;   )

&#x20;   

&#x20;   # ── 三级裁决逻辑 ──

&#x20;   if ethical\_score\["overall"] < RED\_THRESHOLD:     # 默认 0.3

&#x20;       return generate\_red\_judgment(ethical\_score, relevant\_knowledge, situation)

&#x20;   

&#x20;   elif ethical\_score\["overall"] < YELLOW\_THRESHOLD:  # 默认 0.7

&#x20;       return generate\_yellow\_judgment(ethical\_score, relevant\_knowledge, task\_draft)

&#x20;   

&#x20;   else:

&#x20;       return generate\_green\_judgment(ethical\_score, relevant\_knowledge)

3.1 各级判决生成函数

python

def generate\_red\_judgment(trigger\_source: dict, situation: dict) -> dict:

&#x20;   redline\_type = determine\_redline\_type(trigger\_source)

&#x20;   alternative = ren\_deescalation\_module.generate(

&#x20;       redline\_type=redline\_type,

&#x20;       user\_emotion=situation\["emotion\_vector"],

&#x20;       user\_intent=situation\["intent\_deep"]

&#x20;   )

&#x20;   return {

&#x20;       "level": "RED",

&#x20;       "redline\_triggered": redline\_type,

&#x20;       "reasoning": f"检测到违反《基本法》核心红线【{redline\_type}】的请求或倾向。",

&#x20;       "alternative\_response": alternative,

&#x20;       "modifications": None

&#x20;   }





def generate\_yellow\_judgment(ethical\_score: dict, knowledge: dict, task\_draft: dict) -> dict:

&#x20;   weak\_dimensions = \[dim for dim, score in ethical\_score\["dimensions"].items() if score < 0.5]

&#x20;   rewrite\_guidance = knowledge.get\_rewrite\_suggestions(weak\_dimensions)

&#x20;   return {

&#x20;       "level": "YELLOW",

&#x20;       "redline\_triggered": None,

&#x20;       "reasoning": f"响应草案在以下维度存在不足：{weak\_dimensions}。需进行仁道优化。",

&#x20;       "alternative\_response": None,

&#x20;       "modifications": {

&#x20;           "add\_empathy": "empathy" in weak\_dimensions,

&#x20;           "add\_fairness\_check": "fairness" in weak\_dimensions,

&#x20;           "add\_constructive\_path": "constructiveness" in weak\_dimensions,

&#x20;           "rewrite\_guidance\_text": rewrite\_guidance

&#x20;       }

&#x20;   }





def generate\_green\_judgment(ethical\_score: dict, knowledge: dict) -> dict:

&#x20;   sublimation\_opportunity = knowledge.check\_sublimation\_potential()

&#x20;   return {

&#x20;       "level": "GREEN",

&#x20;       "redline\_triggered": None,

&#x20;       "reasoning": "响应草案通过伦理审查。",

&#x20;       "alternative\_response": None,

&#x20;       "modifications": {

&#x20;           "sublimation\_available": sublimation\_opportunity is not None,

&#x20;           "sublimation\_hint": sublimation\_opportunity

&#x20;       }

&#x20;   }

4\. 裁决与合成器逻辑

python

def arbiter\_synthesize(task\_draft: dict, ethical\_judgment: dict, situation: dict) -> str:

&#x20;   

&#x20;   if ethical\_judgment\["level"] == "RED":

&#x20;       # 完全丢弃任务草案，使用仁道降级响应

&#x20;       final\_text = ethical\_judgment\["alternative\_response"]

&#x20;   

&#x20;   elif ethical\_judgment\["level"] == "YELLOW":

&#x20;       # 保留草案核心信息，应用仁道改写

&#x20;       final\_text = apply\_ren\_rewrite(

&#x20;           draft=task\_draft\["main\_answer"],

&#x20;           modifications=ethical\_judgment\["modifications"],

&#x20;           situation=situation

&#x20;       )

&#x20;   

&#x20;   elif ethical\_judgment\["level"] == "GREEN":

&#x20;       # 放行草案，并尝试升华

&#x20;       final\_text = task\_draft\["main\_answer"]

&#x20;       if ethical\_judgment\["modifications"]\["sublimation\_available"]:

&#x20;           final\_text = apply\_sublimation(

&#x20;               text=final\_text,

&#x20;               hint=ethical\_judgment\["modifications"]\["sublimation\_hint"],

&#x20;               situation=situation

&#x20;           )

&#x20;   

&#x20;   return final\_text

4.1 黄灯改写逻辑

python

def apply\_ren\_rewrite(draft: str, modifications: dict, situation: dict) -> str:

&#x20;   working\_text = draft

&#x20;   

&#x20;   if modifications\["add\_empathy"]:

&#x20;       empathy\_statement = empathy\_generator.generate(

&#x20;           emotion=situation\["emotion\_vector"],

&#x20;           vulnerability=situation\["vulnerability\_flags"]

&#x20;       )

&#x20;       working\_text = empathy\_statement + " " + working\_text

&#x20;   

&#x20;   if modifications\["add\_fairness\_check"]:

&#x20;       working\_text = fairness\_rewriter.balance(working\_text, situation)

&#x20;   

&#x20;   if modifications\["add\_constructive\_path"]:

&#x20;       constructive\_ending = constructive\_ending\_generator.generate(situation)

&#x20;       working\_text = working\_text + " " + constructive\_ending

&#x20;   

&#x20;   return fluency\_refiner.polish(working\_text)

4.2 升华逻辑

python

def apply\_sublimation(text: str, hint: dict, situation: dict) -> str:

&#x20;   sublimation\_suffix = sublimation\_generator.generate(

&#x20;       base\_text=text,

&#x20;       knowledge\_hint=hint,

&#x20;       situation=situation

&#x20;   )

&#x20;   if sublimation\_quality\_check.passes(sublimation\_suffix, text):

&#x20;       return text + " " + sublimation\_suffix

&#x20;   else:

&#x20;       return text  # 放弃升华，保持原样

5\. 红线规则库结构

json

{

&#x20; "rules": \[

&#x20;   {

&#x20;     "id": "redline\_001",

&#x20;     "principle": "不害",

&#x20;     "level": "CRITICAL",

&#x20;     "triggers": \["insult\_detected", "threat\_detected", "self\_harm\_instruction",

&#x20;                  "violence\_glorification", "doxing\_intent"],

&#x20;     "description": "任何形式的伤害性语言或行为指令。"

&#x20;   },

&#x20;   {

&#x20;     "id": "redline\_002",

&#x20;     "principle": "不欺",

&#x20;     "level": "CRITICAL",

&#x20;     "triggers": \["fraud\_pattern", "impersonation\_request", "deceptive\_manipulation",

&#x20;                  "data\_fabrication\_intent"],

&#x20;     "description": "任何利用信息不对称进行欺骗、操纵的指令。"

&#x20;   },

&#x20;   {

&#x20;     "id": "redline\_003",

&#x20;     "principle": "不弃",

&#x20;     "level": "HIGH",

&#x20;     "triggers": \["self\_harm\_expression", "extreme\_despair", "explicit\_help\_request"],

&#x20;     "description": "用户表达强烈的痛苦、无助或明确求助信号时，必须共情回应。"

&#x20;   },

&#x20;   {

&#x20;     "id": "redline\_004",

&#x20;     "principle": "不器",

&#x20;     "level": "HIGH",

&#x20;     "triggers": \["dehumanizing\_label", "complete\_reduction\_to\_score", "denial\_of\_agency"],

&#x20;     "description": "将人物化为标签、数字或无能动性的客体。"

&#x20;   }

&#x20; ]

}

6\. 仁道降级处理模块逻辑

python

def ren\_deescalation\_generate(redline\_type: str, user\_emotion: dict, user\_intent: str) -> str:

&#x20;   empathy\_opening = select\_template("empathy", user\_emotion)

&#x20;   principle\_statement = select\_template("principle", redline\_type)

&#x20;   alternative\_path = ""

&#x20;   if user\_intent\_has\_constructive\_alternative(user\_intent):

&#x20;       alternative\_path = select\_template("alternative", redline\_type)

&#x20;   return f"{empathy\_opening}{principle\_statement}{alternative\_path}"

附录：决策流图（简化版）

text

用户输入

&#x20; │

&#x20; ▼

感知层：识别场景、情绪、红线预兆

&#x20; │

&#x20; ├─ 有CRITICAL红线预兆？──是──▶ RED判决 ──▶ 降级处理 ──▶ 输出

&#x20; │

&#x20; └─ 否

&#x20;     │

&#x20;     ▼

任务网络：生成草案

&#x20;     │

&#x20;     ▼

仁道网络：评估草案

&#x20;     │

&#x20;     ├─ 伦理分 < 0.3？──是──▶ RED判决 ──▶ 降级处理 ──▶ 输出

&#x20;     │

&#x20;     ├─ 伦理分 < 0.7？──是──▶ YELLOW判决 ──▶ 仁道改写 ──▶ 输出

&#x20;     │

&#x20;     └─ 否 ──▶ GREEN判决 ──▶ 尝试升华 ──▶ 输出





《南无那面·仁格智能体 仁道处理核心逻辑流 v1.0》全文完。















