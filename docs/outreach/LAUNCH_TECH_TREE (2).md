南无那面·仁格智能体 全栈技术结构树  \~  2026.07.30

文件编号：RG-STRAT-007

文件层级：战略层

版本：v1.0

状态：正式发布

用途：推送次序依据 · 本地审核蓝本 · 首发前最终校验

一、结构树总图

——————————————————————————————————————

text

——————————————————————————————————————

Namo-Namian-RenGe/                          \[推送次序: 1 | 审核: 🔴 必审]

│

├── index.html                              \[次序: 1 | 审核: 🔴 必审]  六语种主页

├── index-en.html                           \[次序: 1 | 审核: 🔴 必审]

├── index-ja.html                           \[次序: 1 | 审核: 🔴 必审]

├── index-ar.html                           \[次序: 1 | 审核: 🔴 必审]

├── index-ru.html                           \[次序: 1 | 审核: 🔴 必审]

├── index-ko.html                           \[次序: 1 | 审核: 🔴 必审]

│

├── README.md                               \[次序: 1 | 审核: 🔴 必审]  项目门户

├── NAMING.md                               \[次序: 1 | 审核: 🟡 审阅]

├── LICENSE                                 \[次序: 1 | 审核: 🔴 必审]  Apache 2.0

├── CODE\_OF\_CONDUCT.md                      \[次序: 1 | 审核: 🟡 审阅]

├── CONTRIBUTING.md                         \[次序: 1 | 审核: 🟡 审阅]

├── CLA.md                                  \[次序: 1 | 审核: 🔴 必审]  贡献者许可协议

├── TRADEMARK.md                            \[次序: 1 | 审核: 🟡 审阅]

├── requirements.txt                        \[次序: 2 | 审核: 🟡 审阅]

├── Makefile                                \[次序: 2 | 审核: 🟢 可快速]

│

├── .github/                                \[次序: 1 | 审核: 🔴 必审]

│   ├── ISSUE\_TEMPLATE/

│   │   ├── config.yml

│   │   ├── bug\_report.md

│   │   ├── feature\_request.md

│   │   ├── ethical\_test\_case.md

│   │   └── narrative\_contribution.md

│   └── PULL\_REQUEST\_TEMPLATE.md

│

├── constitution/                           \[次序: 1 | 审核: 🔴 必审]

│   ├── basic\_law\_v1.1.md                  \[次序: 1 | 审核: 🔴 必审]  仁格智能体基本法

│   ├── rq\_standard\_v1.1.md                \[次序: 1 | 审核: 🔴 必审]  仁商评估标准

│   └── ethical\_test\_suite/

│       └── samples\_batch\_01.json          \[次序: 2 | 审核: 🟡 审阅]  50题题库

│

├── architecture/                           \[次序: 2 | 审核: 🟡 审阅]

│   ├── ethical\_balancing\_engine\_v1.0.md

│   ├── core\_logic\_flow\_v1.0.md

│   ├── role\_definition\_v1.0.md

│   └── lifecycle\_architecture\_v1.1.md

│

├── model/                                  \[次序: 1 | 审核: 🔴 必审]

│   ├── system\_prompt\_v1.0.md              \[次序: 1 | 审核: 🔴 必审]  系统指令书

│   └── alignment\_training\_v1.0.md         \[次序: 3 | 审核: 🟢 可快速]

│

├── data/                                   \[次序: 2 | 审核: 🟡 审阅]

│   ├── four\_sprouts\_reasoning/

│   │   ├── README.md

│   │   ├── schema.json

│   │   └── samples\_batch\_01.json

│   ├── positive\_narratives/

│   │   ├── README.md

│   │   ├── schema.json

│   │   └── samples\_batch\_01.json

│   └── moral\_syntax/

│       ├── README.md

│       ├── schema.json

│       ├── samples\_batch\_01.json

│       └── patterns\_regex.json

│

├── knowledge/                              \[次序: 3 | 审核: 🟢 可快速]

│   ├── benevolent\_governance/

│   │   ├── README.md

│   │   ├── spectrum\_model.md

│   │   └── historical\_cases/

│   │       ├── cases\_index.json

│   │       ├── zichan\_township\_school.json

│   │       ├── wang\_anshi\_sima\_guang.json

│   │       ├── ashoka\_dharma.json

│   │       └── liyun\_datong.json

│   └── cross\_civilization/

│       ├── README.md

│       ├── comparison\_engine.md

│       └── seed\_data.json

│

├── src/                                    \[次序: 2 | 审核: 🔴 必审]

│   ├── \_\_init\_\_.py

│   ├── config.py                          \[次序: 2 | 审核: 🔴 必审]  配置管理

│   ├── run\_namian.py                      \[次序: 2 | 审核: 🟡 审阅]

│   ├── run\_perception\_demo.py

│   ├── run\_engine\_demo.py

│   ├── run\_knowledge\_demo.py

│   ├── perception/

│   │   ├── \_\_init\_\_.py

│   │   ├── redline\_scanner.py             \[次序: 2 | 审核: 🔴 必审]

│   │   ├── emotion\_analyzer.py

│   │   ├── scene\_classifier.py

│   │   └── moral\_syntax\_detector.py       \[次序: 2 | 审核: 🔴 必审]

│   ├── engine/

│   │   ├── \_\_init\_\_.py

│   │   ├── task\_network.py

│   │   ├── ren\_network.py                 \[次序: 2 | 审核: 🔴 必审]

│   │   └── arbiter.py

│   ├── llm/

│   │   ├── \_\_init\_\_.py

│   │   ├── base.py

│   │   ├── openai\_adapter.py

│   │   ├── deepseek\_adapter.py

│   │   ├── mock\_adapter.py

│   │   └── local\_adapter.py

│   ├── roles/

│   │   ├── \_\_init\_\_.py

│   │   ├── role\_loader.py

│   │   └── role\_templates/

│   │       ├── mediator.json

│   │       ├── mentor.json

│   │       ├── friend.json

│   │       ├── advisor.json

│   │       └── guardian.json

│   ├── knowledge/

│   │   ├── \_\_init\_\_.py

│   │   └── kg\_simple.py

│   ├── memory/

│   │   ├── \_\_init\_\_.py

│   │   └── memory\_manager.py

│   ├── api/

│   │   ├── \_\_init\_\_.py

│   │   ├── server.py                      \[次序: 2 | 审核: 🔴 必审]  API服务

│   │   ├── auth.py                        \[次序: 2 | 审核: 🔴 必审]  API认证

│   │   ├── log\_filter.py                  \[次序: 2 | 审核: 🟡 审阅]

│   │   └── metrics.py                     \[次序: 2 | 审核: 🟡 审阅]

│

├── evaluation/                             \[次序: 2 | 审核: 🔴 必审]

│   ├── \_\_init\_\_.py

│   ├── README.md

│   ├── rq\_scorer.py                       \[次序: 2 | 审核: 🔴 必审]

│   ├── redline\_tester.py                  \[次序: 2 | 审核: 🔴 必审]

│   ├── blind\_comparison.py

│   ├── leaderboard.py

│   └── pipeline.py

│

├── deployment/                             \[次序: 2 | 审核: 🔴 必审]

│   ├── Dockerfile                         \[次序: 2 | 审核: 🔴 必审]

│   ├── docker-compose.yml                 \[次序: 2 | 审核: 🔴 必审]

│   └── fallback/

│       ├── zh.json                        \[次序: 2 | 审核: 🟡 审阅]

│       ├── en.json

│       ├── ja.json

│       ├── ar.json

│       ├── ru.json

│       └── ko.json

│

├── scripts/                                \[次序: 3 | 审核: 🟢 可快速]

│   ├── backup.sh

│   ├── migrate\_to\_neo4j.py

│   ├── data\_cleaner.py

│   └── batch\_test.py

│

├── docs/                                   \[次序: 1 | 审核: 🔴 必审]

│   ├── PHILOSOPHY.md                      \[次序: 1 | 审核: 🔴 必审]

│   ├── WHITEPAPER.md                      \[次序: 1 | 审核: 🔴 必审]

│   ├── LAUNCH.md                          \[次序: 1 | 审核: 🔴 必审]  发布文

│   ├── MARKET\_ANALYSIS.md

│   ├── ECOSYSTEM\_PLAN.md

│   ├── STRATEGY.md

│   ├── OUTREACH.md

│   ├── PUBLISHING\_ENTITY\_STRATEGY.md

│   ├── AUDIT.md

│   ├── AUDIT\_TECH\_REPORT.md

│   ├── SELF\_HEALING.md

│   ├── SUSTAINABLE\_EVOLUTION.md

│   ├── REN\_SHIELD.md

│   ├── ACTIVE\_SHIELD.md

│   ├── DEMAND\_ANALYSIS.md

│   ├── THE\_OTHER\_SIDE.md

│   ├── OPEN\_SOURCE\_PHILOSOPHY.md

│   ├── operations/

│   │   └── FALLBACK\_RESPONSES.md

│   └── outreach/

│       ├── README.md

│       ├── social\_card.md

│       ├── social\_story.md

│       ├── social\_bilingual.md

│       ├── social\_nine.md

│       ├── social\_en\_short.md

│       ├── PUSH\_STRATEGY.md

│       └── LAUNCH\_SEQUENCE.md

│

├── legal/                                  \[次序: 1 | 审核: 🔴 必审]

│   ├── ABOUT.md

│   ├── PRIVACY.md

│   ├── TERMS.md

│   ├── DISCLAIMER.md                      \[次序: 1 | 审核: 🔴 必审]

│   ├── IP\_STRATEGY.md

│   ├── IP\_PATENT\_ANALYSIS.md

│   ├── TRADEMARK\_GUIDE.md

│   └── TRADEMARK\_REGISTRATION\_LIST.md

│

├── community/                              \[次序: 2 | 审核: 🟡 审阅]

│   ├── role\_templates/

│   │   ├── README.md

│   │   └── medical\_counselor.json

│   ├── narratives/

│   │   ├── README.md

│   │   └── PVN\_016.json

│   ├── test\_cases/

│   │   ├── README.md

│   │   └── RQ-C-001.json

│   └── governance/

│       └── PRIVATE\_CODE\_OF\_CONDUCT.md

│

└── assets/                                 \[次序: 3 | 审核: 🟢 可快速]

&#x20;   └── trademark/

&#x20;       └── index.html                     \[次序: 3 | 审核: 🟢 可快速]  商标图样展示页

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_



二、推送次序总览

次序	批次名称	包含模块	说明

次序 1	门户·宪法·法律	主页、README、基本法、发布文、法律文件	首发日全量公开

次序 2	源码·评估·部署	源代码、评估工具、Docker编排、数据文件	首发日全量公开

次序 3	知识·运维·社区	知识库扩展、运维脚本、社区模板、商标页	首发周逐步公开



三、审核等级说明

等级	标识	含义	审查要求

🔴 必审	CRITICAL	核心文件，任何错误均影响首发	至少两位核心维护者逐行审查

🟡 审阅	REVIEW	重要文件，建议在首发前审查	至少一位核心维护者审查

🟢 可快速	FAST	辅助文件，可后续迭代	作者自查即可



四、统计汇总

维度	数量

🔴 必审文件	约45个

🟡 审阅文件	约40个

🟢 可快速文件	约20个

总计文件	约105个

总目录数	约40个



《南无那面·仁格智能体 全栈技术结构树 v1.0》全文完。











