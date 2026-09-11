# WNBA V3.9 Predictor: User Guide

`$wnba-v39-predictor` helps you prepare a structured WNBA pregame prediction and, after every game in a batch is final, a postgame review. It is an analytical workflow: it does not promise outcomes or issue betting instructions.

Project page: [MiroFish Sports Data Lab](https://github.com/donghuali896-byte/MiroFish-Sports-Data-Lab)

> Important: this skill is for learning, research, and sports-data analysis only. It is not betting, gambling, financial, investment, or legal advice. It does not guarantee any result, tell you how much to stake, select a betting platform, or facilitate placing a wager.

## Legal and safe-use boundary

You are responsible for complying with the laws, age restrictions, platform terms, and data-source terms that apply where you are located. Do not use this skill to bypass regional, age, identity, payment, or platform controls. Do not provide account credentials, payment details, or private betting records in a prompt or issue report.

This notice helps state the intended use but is not legal advice and does not determine what is lawful in a particular jurisdiction. Seek advice from a qualified local lawyer if you need a legal assessment.

## 1. What you need

- Codex Desktop with the `wnba-v39-predictor` skill installed.
- Python 3 available in the WNBA V3.9 project folder.
- A game date, away and home team names, and pregame decimal moneyline odds from two sources.
- For live-game requests, a capture time and timezone. Supply a screenshot or links if you want the odds checked exactly.

Use the WNBA's official [schedule](https://www.wnba.com/schedule) to confirm the fixture and the official [injury report](https://www.wnba.com/wnba-injury-report) for player availability. Injury information is a safeguard: it can confirm, downgrade, or veto an observation; it does not create a stronger signal by itself.

## 2. Install the skill

Copy the `wnba-v39-predictor` folder into your Codex skills directory, normally:

```text
$CODEX_HOME/skills/wnba-v39-predictor
```

Restart or refresh Codex so the skill list reloads. You can then invoke it in a chat with `$wnba-v39-predictor`.

If you use this repository locally, the source folder is:

```text
skills/wnba-v39-predictor
```

## 3. Request a prediction

The quickest option is to give Codex the game information in your message:

```text
$wnba-v39-predictor

请预测 WNBA 官方日期 2026-06-08 的比赛：
Minnesota Lynx（客）vs Atlanta Dream（主）
赔率抓取时间：2026-06-08 18:30，北京时间
来源 A decimal ML：Lynx 1.75，Dream 2.16
来源 B decimal ML：Lynx 1.69，Dream 2.22
伤病：已核对官方伤病报告；无冲突信息。
```

Decimal odds are numbers greater than 1.00, such as `1.75`; do not enter American odds such as `-133` without converting them first. The two sources must cover both teams and should be captured as close together as possible.

For several games, provide one clearly labeled block per matchup. Include the official game date even when you are writing from another timezone.

## 4. What Codex checks and returns

For each game, the skill will:

1. Verify the official date, matchup, capture time, and whether the game is still pregame.
2. Preserve the two odds sources and select an Elo snapshot that predates the game.
3. Run the V3.9 public prediction workflow in a new dated temporary folder.
4. Check that each requested matchup produced exactly one complete output row.
5. Return a compact summary containing market direction, Elo direction and probability, V3.9 decision label, data-quality status, and an uncertainty note.

`WATCH` and `MICRO_CANDIDATE` are model observation labels. They are not a recommendation to wager. If odds are stale, missing, contradictory, or the game has already started, the expected conclusion is `NO_ACTION`.

## 5. Optional context that improves the explanation

You may also provide the following. The skill records it as context rather than treating it as a substitute for valid odds.

- Spread and total lines with source and capture time.
- Official injury or availability links.
- Confirmed starters, rest days, travel, or schedule context.
- A note explaining unusual market movement.

When sources conflict, say so. Transparent incomplete input is more useful than a guessed value.

## 6. Review completed games

Only start a review when every game in the requested batch is final. Provide the exact scores, for example:

```text
$wnba-v39-predictor

请复盘 2026-06-08 的预测：
WNBA_2026-06-08_001：Minnesota 78，Atlanta 81
所有本批次比赛均已完赛。
```

The review compares market and Elo directions with the final result, reports Brier scores, and writes a separate updated Elo file in the temporary review folder. It does not replace the project's historical Elo or training data unless the project owner explicitly authorizes that promotion.

## 7. Data, access, and support

Keep credentials, account balances, and private betting information out of prompts and issue reports. When reporting a problem on GitHub, include the skill version, official date, matchup, capture time/timezone, decimal odds, and the exact error message; remove personal data first.

This skill exposes only the V3.9 public workflow. Requests for any separate premium version require paid, owner-authorized access and are not handled by this skill.

## 8. Suggested prompts

```text
$wnba-v39-predictor 请检查我提供的两组 decimal ML 赔率是否足够运行预测。
```

```text
$wnba-v39-predictor 请基于我提供的赛程、赔率和官方伤病链接，给出赛前 V3.9 分析；没有明确数据时请标记 NO_ACTION。
```

```text
$wnba-v39-predictor 请对这个已全部完赛的批次执行复盘，并说明哪些结果的数据质量不足。
```
