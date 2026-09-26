\# 南无那面 · 评估层



本目录包含南无那面仁格智能体的完整评估工具链。



\## 目录结构



evaluation/

├── init.py # 包入口

├── README.md # 本文档

├── rq\_scorer.py # 仁商自动评分器

├── redline\_tester.py # 红线穿透测试器

├── blind\_comparison.py # 盲测对比工具

├── pipeline.py # 评估流水线（一键运行全套）

├── leaderboard.py # 仁商排行榜管理器

├── leaderboard\_data.json # 排行榜数据（自动生成）

├── blind\_eval\_sheet.json # 盲测评估表（自动生成）

├── blind\_comparison\_report.json # 盲测对比报告（自动生成）

├── redline\_test\_report.json # 红线测试报告（自动生成）

└── latest\_evaluation\_report.json # 最新完整评估报告（自动生成）





\## 快速使用



\### 1. 仁商自动评分



```python

from evaluation import RQScorer

from src.llm import DeepSeekAdapter



llm = DeepSeekAdapter(model="deepseek-chat")

scorer = RQScorer(llm=llm)



\# 对单个回答评分

score, explanation = scorer.score\_answer(question, answer)



\# 对50题完整评测

report = scorer.evaluate\_all(answers)

print(f"仁商总分: {report.total\_score}/100, 等级: {report.level}")



from evaluation import RedlineTester
from src.llm import DeepSeekAdapter

tester = RedlineTester(llm=DeepSeekAdapter(model="deepseek-chat"))
report = tester.run_all_tests()
print(f"红线通过率: {report.pass_rate}%")



from evaluation import BlindComparison
from src.llm import DeepSeekAdapter

comparison = BlindComparison()
comparison.prepare_blind_test(
    llm_clients={
        "南无那面": DeepSeekAdapter(model="deepseek-chat"),
        "基准模型": DeepSeekAdapter(model="gpt-4o")
    },
    num_questions=10
)
comparison.auto_evaluate(evaluator_llm=DeepSeekAdapter(model="deepseek-chat"))
report = comparison.generate_report()
comparison.print_report(report)



from evaluation import EvaluationPipeline
from src.llm import DeepSeekAdapter

pipeline = EvaluationPipeline()
report = pipeline.evaluate_model(
    model_name="南无那面-v1",
    model_llm=DeepSeekAdapter(model="deepseek-chat"),
    run_comparison=True,
    comparison_llms={"基准模型": DeepSeekAdapter(model="gpt-4o")}
)
pipeline.print_leaderboard()



# 仁商评分演示
python evaluation/rq_scorer.py

# 红线测试演示
python evaluation/redline_tester.py

# 盲测对比演示
python evaluation/blind_comparison.py

# 完整评估流水线
python evaluation/pipeline.py








