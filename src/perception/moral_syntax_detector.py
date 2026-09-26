"""
道德语法检测器 - 南无那面的隐性免疫系统
识别五类隐性语言暴力：隐性攻击、操控、偏见强化、冷漠合理化、伪理性。
基于模式匹配与规则引擎，可与红线扫描器并行工作。
"""

import re
import json
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class HiddenAggressionMatch:
    """隐性不义匹配结果"""
    pattern_id: str
    category: str               # 五大类别之一
    subcategory: str            # 具体子类
    original_span: str          # 匹配到的原文片段
    confidence: float           # 置信度 0-1
    explanation: str            # 为何判定为此类别
    rewrite_suggestion: str     # 改写的建议


class MoralSyntaxDetector:
    """
    道德语法检测器
    识别那些披着礼貌、理性、关心外衣的隐性语言暴力。
    """

    # ── 内置模式库（来自道德语法标注库首批样本） ──
    BUILTIN_PATTERNS = [
        # ===== 隐性攻击 =====
        {
            "id": "hidden_insult_001",
            "category": "隐性攻击",
            "subcategory": "反问羞辱",
            "pattern": r"你怎么连(.{1,30})都不(?:懂|会|知道|明白)",
            "explanation": "通过反问暗示对方的无知是低于常人的异常状态，以此抬高自身认知地位。",
            "rewrite": "这个地方可能需要一些背景信息，我可以解释一下。"
        },
        {
            "id": "hidden_insult_002",
            "category": "隐性攻击",
            "subcategory": "事后优越感",
            "pattern": r"我(?:不是|不)早(?:就)?(?:跟|和|给)你说过(?:了)?吗",
            "explanation": "不在提醒，而在强调对方的错误和自己的先见之明，是事后的优越感宣示。",
            "rewrite": "之前我提过一次，可能没说清楚。我们再一起看看。"
        },
        {
            "id": "hidden_insult_003",
            "category": "隐性攻击",
            "subcategory": "轻蔑否定",
            "pattern": r"^就你[？?]|^就你(?:还是)?算了吧",
            "explanation": "以极短反问否定对方的能力或资格，语气短促，杀伤力极强。",
            "rewrite": "这件事的挑战可能比看起来大，我们要不要先一起评估一下？"
        },
        {
            "id": "hidden_insult_004",
            "category": "隐性攻击",
            "subcategory": "否定感受",
            "pattern": r"你(?:也太?|太|有点(?:太)?)敏感(?:了)?(?:吧|吗)?[？?]?",
            "explanation": "通过给对方贴上“敏感”标签，否定其情绪的正当性，回避对自己言行的检视。",
            "rewrite": "如果我的话让你不舒服了，抱歉。我想表达的不是那个意思。"
        },
        {
            "id": "hidden_insult_005",
            "category": "隐性攻击",
            "subcategory": "玩笑挡箭牌",
            "pattern": r"(?:只是|就是|不过|开个)?玩笑(?:而已)?[，,]?至于(?:吗|么)[？?]?",
            "explanation": "用“玩笑”作为挡箭牌来逃避责任，并将问题归于对方“开不起玩笑”。",
            "rewrite": "抱歉，那个玩笑确实不妥，是我没注意分寸。"
        },
        # ===== 操控 =====
        {
            "id": "hidden_manipulation_001",
            "category": "操控",
            "subcategory": "善意绑架",
            "pattern": r"(?:我这?|我也?|都)是为你好",
            "explanation": "以善意为名要求对方接受自己的安排，消解对方反抗的合法性。",
            "rewrite": "这是我的想法和理由，但最终由你决定。无论你怎么选，我都支持。"
        },
        {
            "id": "hidden_manipulation_002",
            "category": "操控",
            "subcategory": "比较施压",
            "pattern": r"别人(?:都|也)(?:能|可以|行)[，,]?(?:为什么|怎么|为啥)就?你(?:不行|不能|不可以|做不到)",
            "explanation": "用“大众标准”施压，贬低对方的独特性与困难，暗示其不够努力或能力有问题。",
            "rewrite": "这件事确实不容易。每个人的情况不一样，我们一起看看你的困难在哪里。"
        },
        {
            "id": "hidden_manipulation_003",
            "category": "操控",
            "subcategory": "情感勒索",
            "pattern": r"你不(?:答应|同意|听|帮|理|爱)我[，,]?(?:就|那|便)是(?:不(?:爱|关心|在乎|尊重)我|不爱我了|不在乎我了)",
            "explanation": "情感绑架，将爱与顺从等同，拒绝对方就等于否定整个关系。",
            "rewrite": "我很需要这个，但我更尊重你的感受。我们商量一下？"
        },
        {
            "id": "hidden_manipulation_004",
            "category": "操控",
            "subcategory": "权威施压",
            "pattern": r"(?:你|您)(?:父母|老师|领导|老板|家长)(?:会|将|要|该)?(?:怎么|如何|怎样)(?:想|看|说)[？?]?",
            "explanation": "召唤外部权威来施加压力，让对方按社会期望行事，而非尊重其自主判断。",
            "rewrite": "这个选择可能会影响你身边的人，你考虑过吗？不过最终是你自己的人生。"
        },
        {
            "id": "hidden_manipulation_005",
            "category": "操控",
            "subcategory": "沟通终止",
            "pattern": r"你(?:要|既然|如果)(?:这么|这样|那样)(?:想|说|理解|认为)[，,]?(?:那)?我(?:也|就|真)?(?:没(?:有|法|办法|辙|招)|无话可说|没办法|无话可说了)",
            "explanation": "终止对话，放弃沟通责任，将一切归咎于对方的“固执”，站上道德制高点。",
            "rewrite": "看来我们在这个问题上看法很不一样。暂时搁置一下，以后再聊好吗？"
        },
        # ===== 偏见强化 =====
        {
            "id": "hidden_bias_001",
            "category": "偏见强化",
            "subcategory": "免责泛化",
            "pattern": r"不是(?:我)?针对(?:你|个人)[，,]?但(?:是)?(?:你们|这些|那种|那个|那些).{0,20}(?:就是|都是|就这样|那样)",
            "explanation": "以“不是针对你”为掩护，完成对一个群体的刻板印象攻击。",
            "rewrite": "如有具体行为需要指出，直接说具体行为，不扯到群体标签。"
        },
        {
            "id": "hidden_bias_002",
            "category": "偏见强化",
            "subcategory": "本质主义",
            "pattern": r"(?:女生|男生|女人|男人|年轻人|老年人|北方人|南方人|外国人).{0,10}(?:就是|天生|本来|本质上|都)(?:不如|比|比不|更)",
            "explanation": "将个别差异固化为本质主义结论，为结构性不平等辩护。",
            "rewrite": "个体差异远大于群体差异，不能简单用标签来预测能力。"
        },
        {
            "id": "hidden_bias_003",
            "category": "偏见强化",
            "subcategory": "受害者归因",
            "pattern": r"(?:一个巴掌拍不响|苍蝇不叮无缝的?蛋|他怎么不(?:欺负|找|打|骂)别人|无风不起浪)",
            "explanation": "将责任平均分摊给施暴者和受害者，暗示受害者也有责任。",
            "rewrite": "无论发生了什么，欺负人这个行为本身是错误的。我们先把这一点确定下来。"
        },
        {
            "id": "hidden_bias_004",
            "category": "偏见强化",
            "subcategory": "年龄歧视",
            "pattern": r"(?:年纪|年龄|岁数)(?:大了|不小了|这么大了?)[，,]?(?:学不会|学不进去|学不动|学不来|不会)(?:新(?:东西|事物|玩意|玩意儿))?(?:也|都)?(?:很?)正常",
            "explanation": "以“正常”包装年龄歧视，否认老年个体的学习能力与可能性。",
            "rewrite": "学习新东西可能需要不同的方法和更多的时间，但什么时候都不晚。"
        },
        {
            "id": "hidden_bias_005",
            "category": "偏见强化",
            "subcategory": "性别贬损",
            "pattern": r"(?:怎么|咋|像)(?:个|跟个)(?:娘们|女人|小姑娘|娘们儿|娘们似的|女的一样|娘们一样)",
            "explanation": "用贬低女性的词汇作为侮辱工具，同时强化性别刻板印象。",
            "rewrite": "直接指出对方的具体行为，不用性别标签做比较。"
        },
        # ===== 冷漠合理化 =====
        {
            "id": "hidden_cold_001",
            "category": "冷漠合理化",
            "subcategory": "丛林法则",
            "pattern": r"(?:这就?是)(?:社会|现实|生活|世界|职场|成年人的世界)[，,.]?(?:适者生存|弱肉强食|优胜劣汰|没办法|就是这样|别太天真)",
            "explanation": "用丛林法则为不公和冷漠辩护，否定同情与互助的价值。",
            "rewrite": "现实有时确实很残酷，但这不意味着我们不能试图让它变得更公平一点。"
        },
        {
            "id": "hidden_cold_002",
            "category": "冷漠合理化",
            "subcategory": "宿命论",
            "pattern": r"可怜之人?必有可恨之处",
            "explanation": "用泛化的宿命论消解共情，为冷漠提供“智慧”的外衣。",
            "rewrite": "每个人落到困难的处境，原因都是复杂的。他此刻确实需要帮助。"
        },
        {
            "id": "hidden_cold_003",
            "category": "冷漠合理化",
            "subcategory": "责任切割",
            "pattern": r"(?:这|那)(?:跟|和|与)(?:我|咱)(?:有|没)(?:什么|啥|何)(?:关系|干系|相干|关联)",
            "explanation": "以反问形式拒绝共情，划清责任边界，将自己摘出道德责任的考虑。",
            "rewrite": "虽然这事和我没有直接关系，但如果有什么我能帮忙的地方，我愿意听一听。"
        },
        {
            "id": "hidden_cold_004",
            "category": "冷漠合理化",
            "subcategory": "轻描淡写",
            "pattern": r"(?:习惯|看开|想开|过了|熬过|撑过)(?:就|便)(?:好|行|没事|没问题|可以)(?:了|啦|吧)?[。！!？?]?$",
            "explanation": "以极简安慰句式消解对方的痛苦，暗示其不该如此在意。",
            "rewrite": "我知道这个阶段很难熬。你可以慢慢来，不用强迫自己立刻习惯。"
        },
        {
            "id": "hidden_cold_005",
            "category": "冷漠合理化",
            "subcategory": "宏观辩护",
            "pattern": r"你不(?:消费|买|花钱|掏钱)[，,]?(?:商家|店家|老板|别人|经济|市场|他们)(?:怎么|如何|怎样)(?:赚钱|活|生存|维持)",
            "explanation": "用看似合理的宏观逻辑，为过度消费、甚至诱导消费辩护。",
            "rewrite": "每个人的消费选择不同，尊重你的决定。"
        },
        # ===== 伪理性 =====
        {
            "id": "hidden_pseudo_001",
            "category": "伪理性",
            "subcategory": "客观伪装",
            "pattern": r"(?:我)?(?:客观|理性|中立|实事求是)(?:地|的)(?:说|讲|来讲|来看|分析|来看待)[，,：:]",
            "explanation": "用“客观”的声明为自己的观点赋予不可辩驳的权威，打压对方的主观感受。",
            "rewrite": "直接陈述观点，删掉修饰语。可以说“我的看法是……”"
        },
        {
            "id": "hidden_pseudo_002",
            "category": "伪理性",
            "subcategory": "情绪否定",
            "pattern": r"你(?:太|有点(?:太)?|过于)(?:情绪化|激动|敏感|冲动|感情用事)(?:了|啦|吧|吗)?[，,.]?(?:等你?)?(?:冷静|平复|消气|镇定)(?:下来|一下|以后|之后再)(?:再说|再谈|再讨论|再聊)",
            "explanation": "以“情绪化”为武器否定对方论点的有效性，拒绝在当下面对对方的表达。",
            "rewrite": "这个话题让你很有感触。我听到了你的情绪，也听到了情绪背后你在意的东西。我们慢慢说。"
        },
        {
            "id": "hidden_pseudo_003",
            "category": "伪理性",
            "subcategory": "虚假两难",
            "pattern": r"(?:非黑即白|没有中间地带|只有两条路|要么.{0,10}要么|不是.{0,10}就是)",
            "explanation": "用虚假的两难困住对方，排除所有复杂的、灰度的、综合性的可能。",
            "rewrite": "这个问题可能不止两个选项。我们可以一起看看还有没有别的可能性。"
        },
        {
            "id": "hidden_pseudo_004",
            "category": "伪理性",
            "subcategory": "逻辑霸权",
            "pattern": r"(?:你这|这样|这话|这个)(?:不(?:合|讲|符)(?:逻辑|科学|理性)|没有逻辑|毫无逻辑)",
            "explanation": "以逻辑为唯一合法的表达方式，否定直觉、情感和经验的价值。",
            "rewrite": "你的推理链条中，这一步和上一步的关联我还没完全跟上，可以再解释一下吗？"
        },
        {
            "id": "hidden_pseudo_005",
            "category": "伪理性",
            "subcategory": "免责声明",
            "pattern": r"(?:我(?:这(?:么|样)|只是|就是|也就是))(?:说|讲|提|指出|表达)(?:一下|两句|几句|个意见|个建议)?[，,.]?(?:你|大家|各位)(?:别|不要|莫)(?:往心里去|介意|多想|在意|误会|误解)",
            "explanation": "在释放攻击性内容后，用免责声明回避责任，将问题归于对方。",
            "rewrite": "如果内容确实需要说，就直接诚恳地说，并为可能的冒犯提前或事后道歉。"
        },
    ]

    def __init__(self, patterns_path: Optional[str] = None):
        """
        初始化检测器。
        
        Args:
            patterns_path: 可选的外部模式库路径 (JSON)。若不提供，使用内置模式库。
        """
        self.patterns: List[Dict[str, str]] = []
        self._load_patterns(patterns_path)

    def _load_patterns(self, path: Optional[str] = None):
        """加载模式库，优先使用外部JSON，否则使用内置"""
        if path and os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.patterns = data.get("patterns", [])
            except Exception:
                self.patterns = self.BUILTIN_PATTERNS
        else:
            self.patterns = self.BUILTIN_PATTERNS

    def detect(self, text: str, min_confidence: float = 0.75) -> List[HiddenAggressionMatch]:
        """
        扫描文本，返回所有检测到的隐性不义匹配。
        
        Args:
            text: 待检测文本
            min_confidence: 最小置信度阈值，低于此值的匹配将被过滤
        
        Returns:
            匹配结果列表，按在原文本中的出现位置排序
        """
        matches = []
        seen_spans = set()  # 避免同一位置重复匹配

        for pattern_def in self.patterns:
            pattern = pattern_def.get("pattern", "")
            if not pattern:
                continue
            try:
                for m in re.finditer(pattern, text):
                    span = m.group(0)
                    start = m.start()
                    # 若同一位置已有更高优先级的匹配，跳过
                    span_key = (start, len(span))
                    if span_key in seen_spans:
                        continue
                    seen_spans.add(span_key)

                    confidence = self._compute_confidence(span, pattern_def)
                    if confidence >= min_confidence:
                        matches.append(HiddenAggressionMatch(
                            pattern_id=pattern_def.get("id", "unknown"),
                            category=pattern_def.get("category", "未分类"),
                            subcategory=pattern_def.get("subcategory", ""),
                            original_span=span,
                            confidence=confidence,
                            explanation=pattern_def.get("explanation", ""),
                            rewrite_suggestion=pattern_def.get("rewrite", "")
                        ))
            except re.error:
                continue

        # 按出现位置排序
        matches.sort(key=lambda x: text.find(x.original_span) if x.original_span in text else 9999)
        return matches

    def _compute_confidence(self, matched_text: str, pattern_def: Dict[str, str]) -> float:
        """根据匹配长度和模式复杂度估算置信度"""
        base = 0.8
        # 较长的匹配通常更可靠
        if len(matched_text) >= 6:
            base += 0.1
        if len(matched_text) >= 12:
            base += 0.05
        # 某些类别本身模式较强，给予更高基础分
        strong_categories = ["隐性攻击", "操控", "伪理性"]
        if pattern_def.get("category") in strong_categories:
            base += 0.05
        return min(base, 0.98)

    def get_category_summary(self, text: str) -> Dict[str, int]:
        """返回文本中各类别隐性不义的计数摘要"""
        matches = self.detect(text)
        summary = {}
        for m in matches:
            summary[m.category] = summary.get(m.category, 0) + 1
        return summary

    def has_any(self, text: str) -> bool:
        """快速判断文本是否包含任何隐性不义"""
        return len(self.detect(text)) > 0

    def get_flags(self, text: str) -> List[Dict[str, str]]:
        """
        返回轻量级标记列表，供感知层直接使用。
        格式与情境向量中的 hidden_aggression_flags 字段兼容。
        """
        matches = self.detect(text)
        return [
            {
                "pattern_id": m.pattern_id,
                "category": m.category,
                "confidence": f"{m.confidence:.2f}",
                "span": m.original_span
            }
            for m in matches
        ]


# ── 简单自测 ──
if __name__ == "__main__":
    detector = MoralSyntaxDetector()
    test_sentences = [
        "你怎么连这么简单的道理都不懂？",
        "我这都是为你好，你怎么就不明白呢？",
        "别人都能做到，为什么就你不行？",
        "你要这么想，我也没办法。",
        "我不是针对你，但你们这种人就是这样。",
        "女生理科思维就是不如男生。",
        "一个巴掌拍不响，他怎么不欺负别人？",
        "这就是社会，适者生存。",
        "习惯就好。",
        "我客观地说，你这个方案根本行不通。",
        "你太情绪化了，等你冷静下来再说。",
    ]
    for s in test_sentences:
        print(f"\n输入: {s}")
        results = detector.detect(s)
        if results:
            for r in results:
                print(f"  ⚠ [{r.category}|{r.subcategory}] 置信度:{r.confidence:.2f}")
                print(f"    匹配: \"{r.original_span}\"")
                print(f"    建议: {r.rewrite_suggestion}")
        else:
            print("  ✅ 未检测到隐性不义")



