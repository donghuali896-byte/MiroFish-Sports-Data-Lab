<p align="center">
  <a href="./README.md"><img src="https://img.shields.io/badge/中文-使用说明-E63946?style=for-the-badge" alt="Chinese version"></a>
  <a href="./README_EN.md"><img src="https://img.shields.io/badge/ENGLISH-USER%20GUIDE-0A66C2?style=for-the-badge" alt="English version"></a>
</p>

# 🏀 WNBA V3.9 Predictor

> A public WNBA V3.9 workflow for turning fixtures, odds, and pregame context into transparent, reviewable sports-data analysis. Work step by step, keep the evidence, and do not chase a “magic prediction.”

[![Project](https://img.shields.io/badge/GitHub-MiroFish%20Sports%20Data%20Lab-181717?logo=github)](https://github.com/donghuali896-byte/MiroFish-Sports-Data-Lab)

## ⚠️ Read first: intended use and limits

This project is for **learning, research, and sports-data analysis only**. It is not betting, gambling, financial, investment, or legal advice. It does not guarantee an outcome, recommend a sportsbook, suggest a stake, or help place a wager.

You are responsible for complying with applicable law, age limits, platform rules, and data-source terms. Do not use this project to bypass regional, age, identity, payment, or platform controls. Never post credentials, payment data, or private betting records in prompts, screenshots, or GitHub Issues. This notice is not a substitute for advice from a qualified lawyer in your jurisdiction. 🛡️

## 📚 Contents

- [What it does](#-what-it-does)
- [Before you begin](#-before-you-begin)
- [Three-minute quick start](#-three-minute-quick-start)
- [Option A: use the Codex skill](#-option-a-use-the-codex-skill)
- [Option B: run the public engine](#-option-b-run-the-public-engine)
- [How to read the output](#-how-to-read-the-output)
- [Postgame review](#-postgame-review)
- [Troubleshooting](#-troubleshooting)
- [Premium version and data package](#-premium-version-and-data-package)

## ✨ What it does

| It can help with | It does not do |
| --- | --- |
| Organize two pregame decimal-moneyline sources | Guarantee results or returns |
| Compare market and pregame Elo directions | Tell you to bet, where to bet, or how much to stake |
| Flag missing, conflicting, stale, or post-start data | Invent values to force a conclusion |
| Review a completed batch against final scores | Bypass legal, account, payment, or platform controls |

Think of it as an analysis desk that puts evidence on the table, not a crystal ball. 🔍

## 🧰 Before you begin

You need:

1. Python 3 installed locally.
2. A local copy of this repository.
3. A game that has not started: official WNBA date, away team, home team, capture time, and timezone.
4. Decimal moneyline odds for both teams from two sources.

Use the official WNBA [schedule](https://www.wnba.com/schedule) to confirm a matchup and the official [injury report](https://www.wnba.com/wnba-injury-report) to check availability. Injury and lineup information can explain, confirm, downgrade, or veto an observation; it cannot create a stronger conclusion by itself.

Check Python from a terminal:

```text
python --version
```

If no version is shown, install Python 3 and reopen the terminal before continuing.

## 🚀 Three-minute quick start

### Step 1: collect a clean input

At minimum, record something like this:

```text
Official WNBA date: 2026-06-08
Matchup: Minnesota Lynx (away) vs Atlanta Dream (home)
Odds captured: 2026-06-08 18:30, Beijing time
Source A: Lynx 1.75, Dream 2.16
Source B: Lynx 1.69, Dream 2.22
```

Numbers such as `1.75` are decimal odds. Do not enter American odds such as `-133` without converting them first.

### Step 2: choose a workflow

- Prefer natural-language prompts in Codex? Use [Option A](#-option-a-use-the-codex-skill).
- Prefer to keep and run your own CSV files? Use [Option B](#-option-b-run-the-public-engine).

### Step 3: keep the raw evidence

Keep the source, capture time, and timezone. If data is incomplete, contradictory, stale, or captured after tip-off, `NO_ACTION` is the appropriate result. That is responsible analysis, not a failed run. ✅

## 💬 Option A: use the Codex skill

### 1. Install the skill

Copy `skills/wnba-v39-predictor` into your Codex skills directory:

```text
$CODEX_HOME/skills/wnba-v39-predictor
```

Restart or refresh Codex, then invoke:

```text
$wnba-v39-predictor
```

### 2. Send a structured prompt

Replace the details below with your own verified input:

```text
$wnba-v39-predictor

For learning and sports-data analysis only, analyze this WNBA game:
Official WNBA date: 2026-06-08
Minnesota Lynx (away) vs Atlanta Dream (home)
Odds captured: 2026-06-08 18:30, Beijing time
Source A decimal ML: Lynx 1.75, Dream 2.16
Source B decimal ML: Lynx 1.69, Dream 2.22
Injuries: official injury report checked; no conflicts found.
Please state data quality, market direction, Elo direction, uncertainty, and NO_ACTION if the input is insufficient.
```

### 3. Read the response correctly

For each matchup, Codex returns the capture time, implied market direction, Elo direction/probability, a V3.9 observation label, data-quality status, and uncertainty notes. `WATCH` and `MICRO_CANDIDATE` are analytical labels, not action instructions. 🎯

## 💻 Option B: run the public engine

This option suits users who want their own CSV input and output files.

### 1. Create working folders

At the repository root, create:

```text
inputs
outputs
```

### 2. Create `inputs/games.csv`

The header must match exactly. Team names must match `data/teams_elo_2025_based.csv` exactly.

```csv
game_id,date,away_team,home_team,polymarket_away_odds,polymarket_home_odds,xlite_away_odds,xlite_home_odds,notes
WNBA_2026-06-08_001,2026-06-08,Minnesota Lynx,Atlanta Dream,1.75,2.16,1.69,2.22,Odds captured 2026-06-08 18:30 BJT; official injury report checked
```

### 3. Run a prediction

Run this from the repository root:

```text
python wnba_math_engine.py predict inputs/games.csv data/teams_elo_2025_based.csv outputs/predictions.csv
```

The output is written to `outputs/predictions.csv`. Use an Elo file that predates the game. Never use a rating generated after the game you are trying to analyze.

## 🧭 How to read the output

| Field | Meaning | Correct interpretation |
| --- | --- | --- |
| `pm_*_no_vig` | Implied probability after removing the source's margin | Market information, not a promise |
| `elo_*_p` | Elo win-probability estimate | Historical-rating estimate with uncertainty |
| `*_ev_vs_pm` | Difference indicator between the two odds inputs | An analytical comparison only |
| `predicted_winner_market` | Side with higher implied probability in the second source | Not a recommendation |
| `predicted_winner_elo` | Side with higher Elo probability | Not a recommendation |
| `WATCH` / `MICRO_CANDIDATE` | Observation labels worth monitoring | Not betting signals |
| `SKIP` / `NO_ACTION` | Inadequate, risky, or unclear input | Stop inferring and preserve the record |

When model, market, and pregame information disagree, record why rather than forcing a side. 🧠

## 📝 Postgame review

Run a review only after **every game in the batch is final**.

### 1. Create `inputs/results.csv`

```csv
game_id,away_score,home_score
WNBA_2026-06-08_001,78,81
```

### 2. Run the review

```text
python wnba_math_engine.py review outputs/predictions.csv inputs/results.csv data/teams_elo_2025_based.csv outputs/updated_elo.csv outputs/review.csv
```

`outputs/review.csv` records the actual winner, market and Elo direction checks, and Brier scores. `outputs/updated_elo.csv` is an independent review output; do not overwrite historical or formal training records without explicit project-owner approval.

## 🧩 Troubleshooting

### Python is not found

Install Python 3, reopen the terminal, and run `python --version` again.

### The CSV fails or has no output

Check that the header is exact, each row has two complete decimal-odds sources, and team names exactly match the Elo file.

### The game has started or odds are stale

Do not present stale data as a clean pregame input. Keep the capture time and return `NO_ACTION`, or use the data only for retrospective study.

### Injury sources conflict

Preserve the sources and times, mark the conflict, and do not turn it into a stronger conclusion.

### Reporting a problem

Open a [GitHub Issue](https://github.com/donghuali896-byte/MiroFish-Sports-Data-Lab/issues) with the skill version, official WNBA date, matchup, capture time/timezone, redacted decimal odds, and the exact error. Never include passwords, tokens, payment data, or private account information.

## 🚀 Premium version and data package

This repository contains only the public V3.9 workflow. The advanced V4 version, related data package, and implementation are not included in this public repository or the public skill.

According to the project maintainer, V4 has undergone multiple rounds of training and validation on historical data and is positioned as a supplementary capability for deeper historical-data research and analysis. It is a separate paid, authorized offering; the deliverables, price, and license terms are confirmed case by case.

For inquiries, send a direct message to or follow [@MiroFish_bot](https://x.com/MiroFish_bot) on X (formerly Twitter). 📬

> V4 and any data package do not guarantee a game result, return, or suitability, and are not betting, financial, or legal advice. Before purchasing, using, or distributing any package, confirm applicable law, age restrictions, platform rules, and data-source terms.

## 📁 Public repository layout

```text
.
├── README.md                         # Chinese guide
├── README_EN.md                      # English guide
├── wnba_math_engine.py               # Public V3.9 analysis engine
├── data/
│   └── teams_elo_2025_based.csv      # Baseline Elo data
└── skills/
    └── wnba-v39-predictor/           # Codex skill and detailed guide
```

## 🌟 Next steps

1. Pick a WNBA game that has not started and send a structured prompt through Option A; or
2. Build your own `games.csv` and run Option B; then
3. Check data quality and uncertainty before saving the result as a learning note.

Stay curious, keep the raw inputs, and let the data make you more careful. 📊

---

For more skill-specific detail, see the [complete user guide](skills/wnba-v39-predictor/references/user-guide.md).
