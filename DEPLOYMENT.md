\# 南无那面 · 仁格智能体 — 完整项目部署指南



\*\*凡我所算，以仁为界。凡我所向，南无那面。\*\*



本指南面向项目维护者、核心贡献者及部署人员，帮助你在本地及 GitHub 上完整搭建“南无那面”项目，并配置自动化测试与持续集成。



\---



\## 一、前置准备



在开始之前，请确保你的电脑具备以下环境：



| 工具 | 版本要求 | 用途 |

|------|----------|------|

| Python | 3.8 或更高 | 运行伦理决策原型 |

| Git | 最新版 | 版本控制与推送到 GitHub |

| GitHub 账号 | 免费注册 | 托管代码与 CI 测试 |

| PowerShell / Terminal | 系统自带 | 执行命令 |



\---



\## 二、本地环境搭建



\### 2.1 克隆项目到本地（如果已有仓库）



```bash

git clone https://github.com/Namo-Namian-RenGe/renge.git

cd renge



2.2 若从零开始初始化项目

bash

mkdir renge

cd renge

git init

2.3 验证本地测试

将 renge\_test.py 放入项目根目录后，运行：



bash

python renge\_test.py

预期看到“总用例数：12，通过率：100.0%”。



三、配置 GitHub Actions 自动化测试

3.1 创建目录与文件

在项目根目录下创建 .github/workflows/ 文件夹，并新建 ci.yml 文件：



text

renge/

├── .github/

│   └── workflows/

│       └── ci.yml

├── renge\_test.py

└── README.md

3.2 写入工作流配置

将以下内容粘贴进 ci.yml：



yaml

name: 伦理决策测试 CI



on:

&#x20; push:

&#x20;   branches: \[ "main", "master", "dev" ]

&#x20; pull\_request:

&#x20;   branches: \[ "main", "master", "dev" ]



jobs:

&#x20; test:

&#x20;   runs-on: ubuntu-latest

&#x20;   

&#x20;   steps:

&#x20;   - name: 检出代码

&#x20;     uses: actions/checkout@v4



&#x20;   - name: 设置 Python 环境

&#x20;     uses: actions/setup-python@v5

&#x20;     with:

&#x20;       python-version: '3.10'



&#x20;   - name: 运行概念验证测试 (12个用例)

&#x20;     run: python renge\_test.py

3.3 提交并推送到 GitHub

bash

git add .

git commit -m "chore: 初始化项目与 GitHub Actions 自动化测试"

git branch -M main

git remote add origin https://github.com/你的用户名/renge.git

git push -u origin main

3.4 验证 CI 运行

推送成功后，打开 GitHub 仓库页面，点击 Actions 标签，你会看到 伦理决策测试 CI 正在运行，几秒后会显示绿色的对勾 ✅。



四、补充社区与开源治理文件

为了让项目更加规范，建议在根目录下补充以下文件：



文件名	用途	来源

LICENSE	声明开源许可证（Apache 2.0）	从 GitHub 仓库界面一键生成

CODE\_OF\_CONDUCT.md	约束社区行为，倡导“仁”的风气	已随项目提供

CONTRIBUTING.md	指导外部贡献者提交代码与内容	已随项目提供

TEST\_REPORT.md	记录当前测试结果与核心机制验证	已随项目提供

DEPLOYMENT.md	本文档	已随项目提供

五、推荐的项目结构总览

完整部署后，项目根目录应如下所示：



text

renge/

├── .github/

│   └── workflows/

│       └── ci.yml              # 自动化测试 CI

├── renge\_test.py              # 核心伦理决策原型

├── TEST\_REPORT.md             # 测试报告

├── TEST\_REPORT.html           # 可打印版测试报告（可选）

├── CODE\_OF\_CONDUCT.md         # 行为准则

├── CONTRIBUTING.md            # 贡献指南

├── DEPLOYMENT.md              # 部署指南

├── README.md                  # 项目首页

└── LICENSE                    # Apache 2.0

六、常见问题排查

Q1: 运行 python renge\_test.py 提示“无法将 python 识别为命令”

原因：Python 未加入系统环境变量。



解决：尝试使用 py renge\_test.py，或重新安装 Python 并勾选 “Add Python to PATH”。



Q2: GitHub Actions 显示红色 ❌

原因：测试代码未通过。



解决：点击 Actions 中的失败记录，查看报错日志，根据失败用例调整 renge\_test.py 中的规则或测试预期。



Q3: 推送代码时提示 remote origin already exists

原因：已经添加过远程仓库。



解决：



bash

git remote set-url origin https://github.com/你的用户名/renge.git

Q4: 如何在本地合并到已有仓库

如果你已有一个 GitHub 仓库，只需将上述文件复制到本地克隆目录，然后执行：



bash

git add .

git commit -m "feat: 集成自动化测试与项目文档"

git push

七、下一步展望

完成基础部署与 CI 配置后，你可以：



将 renge\_test.py 扩展为真正的 API 服务，接入义理库与叙事链库



开发管理面板与审计日志（见商业版规划）



将测试报告打包为 PDF，用于学术基金或文化部门申报



南无那面不是一个已经完成的答案。

她是一场正在进行的实验。

我们邀请你，加入这场实验。



南无那面·仁格智能体项目组



上海易通和维科技有限责任公司保留所有权力



2026年9月25日













