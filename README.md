# 🏀 WNBA V3.9 Predictor

> 用公开的 WNBA V3.9 工作流，把赛程、赔率和赛前信息整理成可复核的体育数据分析。一步一步来，不猜数据，不追求“神预测”。

[![Project](https://img.shields.io/badge/GitHub-MiroFish%20Sports%20Data%20Lab-181717?logo=github)](https://github.com/donghuali896-byte/MiroFish-Sports-Data-Lab)

## ⚠️ 请先阅读：用途与边界

本项目仅用于**学习、研究和体育数据分析**。它不是投注、赌博、金融、投资或法律建议；不保证比赛结果，不提供下注金额建议，不推荐投注平台，也不协助执行任何下注行为。

请自行遵守所在地法律、年龄限制、平台规则和数据来源条款。请勿利用本项目绕过地区、年龄、身份、支付或平台限制，也不要在提示词、Issue 或截图中提交账号、支付信息或私人投注记录。此说明不能替代合资格律师在你所在地提供的法律意见。🛡️

## 📚 目录

- [它能做什么](#-它能做什么)
- [开始前准备](#-开始前准备)
- [三分钟快速开始](#-三分钟快速开始)
- [方法一：在 Codex 中使用技能](#-方法一在-codex-中使用技能)
- [方法二：在终端运行公开引擎](#-方法二在终端运行公开引擎)
- [如何看懂输出](#-如何看懂输出)
- [赛后复盘](#-赛后复盘)
- [常见问题](#-常见问题)
- [反馈问题](#-反馈问题)

## ✨ 它能做什么

| 能做 | 不能做 |
| --- | --- |
| 整理两组赛前 decimal moneyline（十进制独赢）赔率 | 保证比赛结果或收益 |
| 结合赛前 Elo 快照输出市场与 Elo 方向分析 | 替你下注、推荐平台或计算下注金额 |
| 标记数据缺失、冲突、过时或比赛已开始的风险 | 用缺失或猜测的数据“补全”结论 |
| 在比赛全部结束后做可复核的赛后回顾 | 绕过任何地区、年龄、账号或支付限制 |

一句话：它是一个“把信息摆到桌面上”的分析助手，而不是比赛结果的水晶球。🔍

## 🧰 开始前准备

你需要：

1. 已安装 Python 3。
2. 本仓库的本地副本。
3. 一场尚未开始的 WNBA 比赛：官方日期、客队、主队、赔率抓取时间和时区。
4. 两个来源、双方都完整的 decimal moneyline 赔率。

建议用 WNBA 官方[赛程](https://www.wnba.com/schedule)确认对阵，用官方[伤病报告](https://www.wnba.com/wnba-injury-report)核对赛前可用性。伤病与阵容信息只能帮助解释、确认、降级或否决观察，不能凭空制造更强结论。

在终端确认 Python 可用：

```text
python --version
```

看到版本号即可继续；若提示找不到 `python`，请先安装 Python 3 并重新打开终端。

## 🚀 三分钟快速开始

### 第 1 步：准备比赛信息

请至少准备这一组信息：

```text
WNBA 官方日期：2026-06-08
对阵：Minnesota Lynx（客）vs Atlanta Dream（主）
抓取时间：2026-06-08 18:30，北京时间
来源 A：Lynx 1.75，Dream 2.16
来源 B：Lynx 1.69，Dream 2.22
```

注意：`1.75` 这类大于 `1.00` 的数字是 decimal odds。不要直接填写 `-133` 这类美式赔率。

### 第 2 步：选择使用方式

- 想用自然语言提问：选择[方法一](#-方法一在-codex-中使用技能)。
- 想亲手运行 CSV 与 Python：选择[方法二](#-方法二在终端运行公开引擎)。

### 第 3 步：保留原始信息

记录赔率来源、抓取时间和时区。信息不完整、来源互相冲突或比赛已经开始时，应接受 `NO_ACTION` 结论；这是负责任的数据分析，不是失败。✅

## 💬 方法一：在 Codex 中使用技能

### 1. 安装技能

将本仓库中的 `skills/wnba-v39-predictor` 文件夹复制到 Codex 的技能目录：

```text
$CODEX_HOME/skills/wnba-v39-predictor
```

重启或刷新 Codex 的技能列表。技能名称是：

```text
$wnba-v39-predictor
```

### 2. 直接发送这个提示词

把下面内容复制到 Codex，并替换为你的比赛和赔率：

```text
$wnba-v39-predictor

请仅作学习和体育数据分析，预测 WNBA 官方日期 2026-06-08 的比赛：
Minnesota Lynx（客）vs Atlanta Dream（主）
赔率抓取时间：2026-06-08 18:30，北京时间
来源 A decimal ML：Lynx 1.75，Dream 2.16
来源 B decimal ML：Lynx 1.69，Dream 2.22
伤病：已核对官方伤病报告；无冲突信息。
请标注数据质量、市场方向、Elo 方向和不确定性；若数据不足请输出 NO_ACTION。
```

### 3. 你会收到什么

每场比赛将得到一行紧凑摘要：

- 对阵与赔率抓取时间；
- 市场隐含方向与 Elo 方向/概率；
- V3.9 的观察标签；
- 数据质量状态与不确定性说明。

`WATCH` 与 `MICRO_CANDIDATE` 都只是模型观察标签，不是行动指令。🎯

## 💻 方法二：在终端运行公开引擎

适合希望保存自己的输入与输出 CSV 的用户。

### 1. 创建工作文件夹

在仓库根目录创建两个文件夹：

```text
inputs
outputs
```

### 2. 创建 `inputs/games.csv`

第一行字段名必须完全一致；球队名称必须与 `data/teams_elo_2025_based.csv` 中的名称一致。

```csv
game_id,date,away_team,home_team,polymarket_away_odds,polymarket_home_odds,xlite_away_odds,xlite_home_odds,notes
WNBA_2026-06-08_001,2026-06-08,Minnesota Lynx,Atlanta Dream,1.75,2.16,1.69,2.22,Odds captured 2026-06-08 18:30 BJT; official injury report checked
```

### 3. 运行预测

在仓库根目录执行：

```text
python wnba_math_engine.py predict inputs/games.csv data/teams_elo_2025_based.csv outputs/predictions.csv
```

成功后会生成：

```text
outputs/predictions.csv
```

请只使用比赛开始前的 Elo 文件。若你有更新后的 Elo，必须确认它来自这场比赛之前的最后一个已完成赛日；不要使用赛后才产生的评分。

## 🧭 如何看懂输出

| 输出内容 | 含义 | 正确理解 |
| --- | --- | --- |
| `pm_*_no_vig` | 去除该来源赔率水位后的隐含概率 | 是市场信息，不是结果保证 |
| `elo_*_p` | Elo 模型给出的胜率估计 | 基于历史评分，会有误差 |
| `*_ev_vs_pm` | 两个输入来源之间的概率/赔率差异指标 | 仅用于分析差异 |
| `predicted_winner_market` | 第二来源隐含概率更高的一方 | 不是推荐 |
| `predicted_winner_elo` | Elo 概率更高的一方 | 不是推荐 |
| `WATCH` / `MICRO_CANDIDATE` | 值得继续观察的数据标签 | 不是下注信号 |
| `SKIP` / `NO_ACTION` | 数据不足、风险较高或没有明确观察价值 | 应停止推断并保留记录 |

模型、市场和赛前信息出现分歧时，最好的处理通常是把原因记下来，而不是强行选择一方。🧠

## 📝 赛后复盘

只有当同一批次的比赛**全部完赛**后才做复盘。

### 1. 创建 `inputs/results.csv`

```csv
game_id,away_score,home_score
WNBA_2026-06-08_001,78,81
```

### 2. 运行复盘

```text
python wnba_math_engine.py review outputs/predictions.csv inputs/results.csv data/teams_elo_2025_based.csv outputs/updated_elo.csv outputs/review.csv
```

### 3. 查看结果

- `outputs/review.csv`：实际胜方、市场与 Elo 方向是否匹配、Brier 分数；
- `outputs/updated_elo.csv`：本次独立复盘产生的 Elo 文件。

将输出保留在自己的 `outputs` 文件夹中。除非项目维护者明确批准，不要用它覆盖任何历史数据或正式训练记录。

## 🧩 常见问题

### `python` 找不到

安装 Python 3 后重新打开终端，并再次执行 `python --version`。

### CSV 报错或没有输出

检查：字段名是否完全一致、每行是否同时拥有两队的两组 decimal odds、球队名称是否与 Elo 文件完全一致。

### 游戏已经开始，或赔率过时

不要把旧赔率伪装成赛前输入。记录抓取时间，并输出 `NO_ACTION` 或只做回顾性分析。

### 伤病信息不一致

保留来源和时间，标记冲突；不要把冲突信息转化为更强结论。

### 我想报告问题

请在 [GitHub Issues](https://github.com/donghuali896-byte/MiroFish-Sports-Data-Lab/issues) 中提供：技能版本、WNBA 官方日期、对阵、抓取时间/时区、已脱敏的 decimal odds、报错全文。不要提交密码、令牌、支付信息或私人账户数据。

## 📁 公开仓库结构

```text
.
├── README.md                         # 这份中文使用说明
├── wnba_math_engine.py               # 公开 V3.9 分析引擎
├── data/
│   └── teams_elo_2025_based.csv      # 基础 Elo 数据
└── skills/
    └── wnba-v39-predictor/           # Codex 技能与详细指南
```

## 🌟 下一步

现在你可以：

1. 用一场尚未开始的比赛，按“方法一”发送一条结构化提示词；
2. 或按“方法二”创建自己的 `games.csv` 并运行一次；
3. 结果出来后，先检查数据质量与不确定性，再把它作为学习笔记保存下来。

祝你在体育数据分析的路上越做越清楚、越看越冷静。📊

---

更多面向技能使用者的细节请查看：[完整用户指南](skills/wnba-v39-predictor/references/user-guide.md)。
