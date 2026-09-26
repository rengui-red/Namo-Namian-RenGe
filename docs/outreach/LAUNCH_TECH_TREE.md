南无那面·仁格智能体 技术结构树推送清单

文件编号：RG-STRAT-005

文件层级：战略层

版本：v1.0

状态：正式发布

依赖文件：LAUNCH\_SEQUENCE.md、PUSH\_STRATEGY.md



说明

本清单以项目完整技术结构树为骨架，逐项标注：



推送层级：公共广场 / 庭院 / 茶室 / 内室



首次亮相阶段：种子期 / 首发日 / 首发周 / 沉淀期 / 长期



当前状态：就绪 / 待完成 / 持续迭代



未标注推送层级或阶段的项目，默认随父目录同步公开。



技术结构树推送清单

text

Namo-Namian-RenGe/                          \[公共广场 | 首发日]

│

├── index.html                              \[公共广场 | 首发日 | 就绪]

├── index-en.html                           \[公共广场 | 首发日 | 就绪]

├── index-ja.html                           \[公共广场 | 首发日 | 就绪]

├── index-ar.html                           \[公共广场 | 首发日 | 就绪]

├── index-ru.html                           \[公共广场 | 首发日 | 就绪]

├── index-ko.html                           \[公共广场 | 首发日 | 就绪]

│

├── README.md                               \[公共广场 | 首发日 | 就绪]

├── NAMING.md                               \[庭院     | 种子期预热 | 就绪]

├── LICENSE                                 \[公共广场 | 首发日 | 就绪]

├── CODE\_OF\_CONDUCT.md                      \[公共广场 | 首发日 | 就绪]

├── CONTRIBUTING.md                         \[公共广场 | 首发日 | 就绪]

├── CLA.md                                  \[公共广场 | 首发日 | 就绪]

├── TRADEMARK.md                            \[公共广场 | 首发日 | 就绪]

├── requirements.txt                        \[公共广场 | 首发日 | 就绪]

├── Makefile                                \[公共广场 | 首发日 | 就绪]

│

├── constitution/                           \[公共广场 | 首发日]

│   ├── basic\_law\_v1.0.md                  \[公共广场 | 首发日 | 就绪]

│   ├── rq\_standard\_v1.0.md                \[庭院     | 首发周 | 就绪]

│   └── ethical\_test\_suite/                \[庭院     | 首发周]

│       └── samples\_batch\_01.json          \[庭院     | 首发周 | 就绪]

│

├── architecture/                           \[公共广场 | 首发日]

│   ├── ethical\_balancing\_engine\_v1.0.md   \[庭院     | 首发日 | 就绪]

│   ├── core\_logic\_flow\_v1.0.md            \[茶室     | 首发周 | 就绪]

│   ├── role\_definition\_v1.0.md            \[庭院     | 首发周 | 就绪]

│   └── lifecycle\_architecture\_v1.0.md     \[庭院     | 沉淀期 | 就绪]

│

├── model/                                  \[公共广场 | 首发日]

│   ├── system\_prompt\_v1.0.md              \[庭院     | 首发日 | 就绪]

│   └── alignment\_training\_v1.0.md         \[茶室     | 沉淀期 | 就绪]

│

├── data/                                   \[公共广场 | 首发日]

│   ├── four\_sprouts\_reasoning/            \[庭院     | 首发周 | 就绪]

│   │   ├── README.md

│   │   ├── schema.json

│   │   └── samples\_batch\_01.json

│   ├── positive\_narratives/              \[庭院     | 首发周 | 就绪]

│   │   ├── README.md

│   │   ├── schema.json

│   │   └── samples\_batch\_01.json

│   └── moral\_syntax/                     \[庭院     | 首发周 | 就绪]

│       ├── README.md

│       ├── schema.json

│       ├── samples\_batch\_01.json

│       └── patterns\_regex.json

│

├── knowledge/                              \[庭院     | 沉淀期]

│   └── benevolent\_governance/            \[庭院     | 沉淀期]

│       ├── README.md

│       ├── spectrum\_model.md

│       └── historical\_cases/

│           ├── cases\_index.json

│           ├── zichan\_township\_school.json

│           ├── wang\_anshi\_sima\_guang.json

│           ├── ashoka\_dharma.json

│           └── liyun\_datong.json

│

├── src/                                    \[公共广场（目录）/ 茶室（讨论）]

│   ├── \_\_init\_\_.py

│   ├── run\_namian.py                      \[庭院     | 首发日 | 就绪]

│   ├── run\_perception\_demo.py             \[茶室     | 首发周 | 就绪]

│   ├── run\_engine\_demo.py                 \[茶室     | 首发周 | 就绪]

│   ├── run\_knowledge\_demo.py              \[茶室     | 首发周 | 就绪]

│   │

│   ├── perception/                        \[内室     | 持续迭代]

│   │   ├── redline\_scanner.py             \[内室     | 首发周]

│   │   ├── emotion\_analyzer.py            \[内室     | 首发周]

│   │   ├── scene\_classifier.py            \[内室     | 首发周]

│   │   └── moral\_syntax\_detector.py       \[内室     | 首发周]

│   │

│   ├── engine/                            \[内室     | 持续迭代]

│   │   ├── task\_network.py

│   │   ├── ren\_network.py

│   │   └── arbiter.py

│   │

│   ├── llm/                               \[内室     | 首发周]

│   │   ├── \_\_init\_\_.py

│   │   ├── base.py

│   │   ├── openai\_adapter.py

│   │   ├── deepseek\_adapter.py

│   │   ├── mock\_adapter.py

│   │   └── local\_adapter.py

│   │

│   ├── roles/                             \[庭院     | 首发日]

│   │   ├── \_\_init\_\_.py

│   │   ├── role\_loader.py

│   │   └── role\_templates/

│   │       ├── mediator.json

│   │       ├── mentor.json

│   │       ├── friend.json

│   │       ├── advisor.json

│   │       └── guardian.json

│   │

│   ├── knowledge/                         \[茶室     | 沉淀期]

│   │   └── kg\_simple.py

│   │

│   ├── memory/                            \[茶室     | 沉淀期]

│   │   └── memory\_manager.py

│   │

│   └── api/                               \[庭院     | 首发日]

│       └── server.py                      \[庭院     | 首发日 | 需LLM适配器]

│

├── evaluation/                             \[庭院     | 首发周]

│   ├── README.md

│   ├── rq\_scorer.py                       \[庭院     | 首发周 | 就绪]

│   ├── redline\_tester.py                  \[茶室     | 首发周 | 就绪]

│   ├── blind\_comparison.py                \[茶室     | 沉淀期 | 就绪]

│   ├── leaderboard.py                     \[庭院     | 沉淀期 | 就绪]

│   └── pipeline.py                        \[茶室     | 沉淀期 | 就绪]

│

├── deployment/                             \[内室     | 首发日]

│   ├── Dockerfile                         \[内室     | 首发日 | 就绪]

│   ├── docker-compose.yml                 \[内室     | 首发周 | 待创建]

│   └── fallback/                          \[内室     | 首发日]

│       ├── zh.json                        \[内室     | 首发日 | 就绪]

│       ├── en.json                        \[内室     | 首发日 | 就绪]

│       ├── ja.json                        \[内室     | 首发日 | 就绪]

│       ├── ar.json                        \[内室     | 首发日 | 就绪]

│       ├── ru.json                        \[内室     | 首发日 | 就绪]

│       └── ko.json                        \[内室     | 首发日 | 就绪]

│

├── docs/                                   \[公共广场 | 首发日]

│   ├── PHILOSOPHY.md                      \[庭院     | 首发日 | 就绪]

│   ├── WHITEPAPER.md                      \[庭院     | 首发日 | 就绪]

│   ├── LAUNCH.md                          \[公共广场 | 首发日 | 就绪]

│   ├── MARKET\_ANALYSIS.md                 \[茶室     | 沉淀期 | 就绪]

│   ├── ECOSYSTEM\_PLAN.md                  \[茶室     | 沉淀期 | 就绪]

│   ├── STRATEGY.md                        \[内室     | 种子期 | 就绪]

│   ├── OUTREACH.md                        \[内室     | 种子期 | 就绪]

│   ├── PUBLISHING\_ENTITY\_STRATEGY.md      \[内室     | 种子期 | 就绪]

│   ├── AUDIT.md                           \[内室     | 种子期 | 就绪]

│   ├── SELF\_HEALING.md                    \[庭院     | 首发周 | 就绪]

│   ├── operations/

│   │   └── FALLBACK\_RESPONSES.md          \[内室     | 首发日 | 就绪]

│   └── outreach/

│       ├── README.md                      \[内室     | 种子期 | 就绪]

│       ├── social\_card.md                 \[庭院     | 首发日 | 就绪]

│       ├── social\_story.md                \[庭院     | 首发日 | 就绪]

│       ├── social\_bilingual.md            \[庭院     | 首发日 | 就绪]

│       ├── social\_nine.md                 \[庭院     | 首发日 | 就绪]

│       ├── social\_en\_short.md             \[庭院     | 首发日 | 就绪]

│       ├── PUSH\_STRATEGY.md               \[内室     | 种子期 | 就绪]

│       └── LAUNCH\_SEQUENCE.md             \[内室     | 种子期 | 就绪]

│

├── legal/                                  \[公共广场 | 首发日]

│   ├── ABOUT.md

│   ├── PRIVACY.md

│   ├── TERMS.md

│   ├── DISCLAIMER.md

│   ├── IP\_STRATEGY.md                     \[内室     | 种子期]

│   └── TRADEMARK\_GUIDE.md                 \[内室     | 种子期]

│

├── community/                              \[茶室     | 首发周开放]

│   ├── role\_templates/

│   ├── narratives/

│   ├── test\_cases/

│   └── governance/

│       └── PRIVATE\_CODE\_OF\_CONDUCT.md     \[茶室     | 种子期 | 就绪]

│

└── .github/                                \[内室     | 种子期]

&#x20;   ├── ISSUE\_TEMPLATE/

&#x20;   └── PULL\_REQUEST\_TEMPLATE.md

——————————————————————————————————————

快速索引：当前状态速查

状态	标识	数量

就绪	✅	绝大多数文件

待完成	🔶	docker-compose.yml

持续迭代	🔄	src/perception/、src/engine/

快速索引：推送层级速查

层级	标识	主要文件范围

公共广场	🔓	根目录文档、constitution/、六语种主页、README、LICENSE

庭院	📢	model/、data/、roles/、evaluation/（排行榜）、docs/PHILOSOPHY、社交素材

茶室	🍵	src/ 讨论与反馈、community/、evaluation/（测试工具）

内室	🔒	deployment/fallback/、docs/STRATEGY、legal/IP\_STRATEGY、.github/





《南无那面·仁格智能体 技术结构树推送清单 v1.0》全文完。













