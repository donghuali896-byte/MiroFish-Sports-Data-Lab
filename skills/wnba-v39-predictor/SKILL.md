---
name: wnba-v39-predictor
description: "Prepare V3.9 WNBA pregame predictions or postgame reviews from verified game, odds, and result inputs. Use for the project's public V3.9 workflow; exclude nonpublic premium-model requests."
---

# WNBA V3.9 Predictor

Use the public V3.9 workflow in this project to produce a clearly dated, evidence-based WNBA prediction or review. This is for learning and sports-data analysis only. Treat model output as analysis, not a promise of an outcome or a wagering instruction.

## Scope and access boundary

- Work only with the V3.9 engine at `wnba_math_engine.py`, the supplied V3.9 inputs, and data the user explicitly provides or authorizes to collect.
- Do not read, run, copy, summarize, reference, or infer anything from private, premium, or nonpublic files, directories, models, parameters, outputs, or documentation. Do not include them in generated artifacts.
- If the user requests any version other than the public V3.9 workflow, respond: "That version is a separate paid, authorized offering and is not available through this public skill. Please contact the owner for access." Do not disclose price, payment instructions, or implementation details, and do not continue unless the owner separately confirms access.
- Do not alter model logic, thresholds, historical inputs, or Elo ratings to make a preferred side win. Keep any prediction inputs and outputs in a new dated subfolder under `tmp/v39-predictions/`; never overwrite a historical record unless the user explicitly asks.
- Do not provide betting, gambling, financial, investment, or legal advice; stake sizing; a betting-platform recommendation; or instructions that facilitate placing a wager. Do not process payment, account, identity, or location-bypass information.
- Refuse requests to bypass age, regional, identity, payment, or platform controls. Remind users that they are responsible for following applicable laws and source/platform terms.
- Every prediction or review must state that it is for learning and data analysis only, is not betting or legal advice, and does not guarantee an outcome.

## Pregame prediction

For a request to predict one or more games:

1. Establish the WNBA official game date, away/home teams, and the odds capture time and timezone. Confirm that the game has not started. If current schedule, odds, injuries, or starters matter, obtain and cite the current primary sources; never invent missing figures.
2. Require decimal moneyline odds for both teams from each of two sources. Record unavailable optional context (spread, total, injuries, rest, travel, and lineup status) as context only. Missing or conflicting information may downgrade the conclusion but must not create a stronger recommendation.
3. Use the most recent valid pregame V3.9 Elo file from `current/updated_elo_after_MMDD.csv` that predates the game. If no suitable update exists, use `data/teams_elo_2025_based.csv` and label the result `ELO_BASELINE_FALLBACK`. Never use a postgame Elo for the game being predicted.
4. Create a new UTF-8 CSV named `games.csv` in `tmp/v39-predictions/YYYY-MM-DD/` with exactly these columns:

   ```csv
   game_id,date,away_team,home_team,polymarket_away_odds,polymarket_home_odds,xlite_away_odds,xlite_home_odds,notes
   ```

   Team names must match the chosen Elo file exactly. Use a stable game ID such as `WNBA_YYYY-MM-DD_001`. Preserve the raw odds and capture time in `notes`.

5. Run the public engine:

   ```powershell
   python wnba_math_engine.py predict tmp/v39-predictions/YYYY-MM-DD/games.csv PATH-TO-PREGAME-ELO.csv tmp/v39-predictions/YYYY-MM-DD/predictions.csv
   ```

6. Check that every requested game has exactly one row and that each probability, no-vig probability, EV, and decision field is populated. Report the relevant result values verbatim from the output, distinguish `WATCH` and `MICRO_CANDIDATE` from a bet, and default to `NO_ACTION` when data is incomplete, stale, conflicted, or the game has begun.

Present one compact row per game: matchup, capture time, market-implied direction, Elo direction/probability, V3.9 decision, data-quality status, and a short explanation. Include a concise uncertainty note and links to any current sources used.

## Postgame review

Run a review only after results for every game in the submitted batch are final. Create a UTF-8 `results.csv` in the same dated temporary folder with:

```csv
game_id,away_score,home_score
```

Then run:

```powershell
python wnba_math_engine.py review tmp/v39-predictions/YYYY-MM-DD/predictions.csv tmp/v39-predictions/YYYY-MM-DD/results.csv PATH-TO-PREGAME-ELO.csv tmp/v39-predictions/YYYY-MM-DD/updated_elo.csv tmp/v39-predictions/YYYY-MM-DD/review.csv
```

Verify every game was reviewed before describing aggregate accuracy. State the actual winner, the market and Elo direction outcomes, Brier scores, and whether the pregame data was clean. Keep the generated Elo file in the temporary review folder unless the user expressly authorizes promotion to the project's historical workflow.

## Detailed user instructions

When a user asks how to install or use this skill, read [the user guide](references/user-guide.md). It contains the public setup, input, prediction, and review procedures. Do not duplicate its contents here.
