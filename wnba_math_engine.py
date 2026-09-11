#!/usr/bin/env python3
from __future__ import annotations
import csv, math, sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

SCALE = 400.0
K_FACTOR = 20.0
HCA = 0.0
DEFAULT_ELO = 1500.0

def implied_prob(odds: float) -> float:
    if odds <= 1.0:
        raise ValueError(f"Invalid decimal odds: {odds}")
    return 1.0 / odds

def no_vig_probs(odds_a: float, odds_b: float) -> Tuple[float, float]:
    pa, pb = implied_prob(odds_a), implied_prob(odds_b)
    total = pa + pb
    return pa / total, pb / total

def ev_edge(reference_p: float, available_odds: float) -> float:
    return reference_p * available_odds - 1.0

def probability_edge(reference_p: float, available_odds: float) -> float:
    return reference_p - implied_prob(available_odds)

def elo_win_prob(elo_a: float, elo_b: float, hca_for_a: float = 0.0, scale: float = SCALE) -> float:
    diff = elo_a + hca_for_a - elo_b
    return 1.0 / (1.0 + 10.0 ** (-diff / scale))

def market_implied_elo_diff(p_home: float, scale: float = SCALE) -> float:
    eps = 1e-9
    p = min(max(p_home, eps), 1 - eps)
    return scale * math.log10(p / (1.0 - p))

def brier(p: float, outcome: int) -> float:
    return (p - outcome) ** 2

def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows: List[Dict[str, object]], fieldnames: List[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})

def load_elos(path: Path) -> Dict[str, float]:
    return {r["team"]: float(r["elo"]) for r in read_csv(path)}

def save_elos(path: Path, elos: Dict[str, float]) -> None:
    rows = [{"team": t, "elo": round(e, 3)} for t, e in sorted(elos.items())]
    write_csv(path, rows, ["team", "elo"])

def parse_float(value: str, default: Optional[float] = None) -> Optional[float]:
    value = (value or "").strip()
    return default if value == "" else float(value)

def parse_int(value: str, default: Optional[int] = None) -> Optional[int]:
    value = (value or "").strip()
    return default if value == "" else int(float(value))

def make_decision(away: str, home: str, pm_away: float, pm_home: float, away_ev: float, home_ev: float) -> str:
    best_side = away if away_ev >= home_ev else home
    best_ev = max(away_ev, home_ev)
    best_odds = pm_away if best_side == away else pm_home
    if best_odds < 1.30:
        return "SKIP_LOW_ODDS"
    if best_ev > 0.10 and best_odds >= 2.50:
        return f"MICRO_CANDIDATE_{best_side}_HIGH_EV"
    if best_ev > 0.05:
        return f"WATCH_{best_side}_MEDIUM_EV"
    return "SKIP"

def init_elo_from_2025(baseline_csv: Path, output_csv: Path, alpha: float = 20.0, expansion_elo: float = 1450.0) -> None:
    """
    Build initial Elo from 2025 win-loss with regression to .500.

    Adjusted Win% = (Wins + alpha*0.5) / (Games + alpha)
    Elo = 1500 + 400*log10(AdjWin% / (1-AdjWin%))

    Expansion teams / missing W-L get expansion_elo.
    """
    rows = read_csv(baseline_csv)
    out = []
    for r in rows:
        team = r["team"]
        wins = parse_int(r.get("wins", ""), None)
        losses = parse_int(r.get("losses", ""), None)
        if wins is None or losses is None or wins + losses == 0:
            elo = expansion_elo
            method = "expansion_or_missing"
            adj_wp = ""
        else:
            games = wins + losses
            adj_wp_float = (wins + alpha * 0.5) / (games + alpha)
            adj_wp_float = min(max(adj_wp_float, 1e-6), 1 - 1e-6)
            elo = DEFAULT_ELO + SCALE * math.log10(adj_wp_float / (1 - adj_wp_float))
            method = f"2025_WL_alpha_{alpha:g}"
            adj_wp = round(adj_wp_float, 6)
        out.append({
            "team": team,
            "elo": round(elo, 3),
            "adjusted_win_pct": adj_wp,
            "method": method,
        })
    write_csv(output_csv, out, ["team", "elo", "adjusted_win_pct", "method"])
    print(f"Wrote 2025-based Elo: {output_csv}")

def predict(games_csv: Path, elo_csv: Path, output_csv: Path) -> None:
    games = read_csv(games_csv)
    elos = load_elos(elo_csv)
    rows = []
    for g in games:
        game_id, date = g["game_id"], g["date"]
        away, home = g["away_team"], g["home_team"]
        pm_away = parse_float(g["polymarket_away_odds"])
        pm_home = parse_float(g["polymarket_home_odds"])
        x_away = parse_float(g["xlite_away_odds"])
        x_home = parse_float(g["xlite_home_odds"])

        pm_away_nv, pm_home_nv = no_vig_probs(pm_away, pm_home)
        x_away_nv, x_home_nv = no_vig_probs(x_away, x_home)

        away_prob_edge = probability_edge(x_away_nv, pm_away)
        home_prob_edge = probability_edge(x_home_nv, pm_home)
        away_ev = ev_edge(x_away_nv, pm_away)
        home_ev = ev_edge(x_home_nv, pm_home)

        away_elo = elos.get(away, DEFAULT_ELO)
        home_elo = elos.get(home, DEFAULT_ELO)
        elo_home_p = elo_win_prob(home_elo, away_elo, HCA)
        elo_away_p = 1.0 - elo_home_p

        market_elo_diff = market_implied_elo_diff(x_home_nv)
        model_elo_diff = home_elo + HCA - away_elo
        elo_market_gap = market_elo_diff - model_elo_diff

        decision = make_decision(away, home, pm_away, pm_home, away_ev, home_ev)
        rows.append({
            "game_id": game_id, "date": date, "away_team": away, "home_team": home,
            "pm_away_odds": pm_away, "pm_home_odds": pm_home,
            "xlite_away_odds": x_away, "xlite_home_odds": x_home,
            "pm_away_no_vig": round(pm_away_nv, 6), "pm_home_no_vig": round(pm_home_nv, 6),
            "xlite_away_no_vig": round(x_away_nv, 6), "xlite_home_no_vig": round(x_home_nv, 6),
            "away_prob_edge_vs_pm": round(away_prob_edge, 6), "home_prob_edge_vs_pm": round(home_prob_edge, 6),
            "away_ev_vs_pm": round(away_ev, 6), "home_ev_vs_pm": round(home_ev, 6),
            "away_elo_pre": round(away_elo, 3), "home_elo_pre": round(home_elo, 3),
            "elo_away_p": round(elo_away_p, 6), "elo_home_p": round(elo_home_p, 6),
            "market_implied_elo_diff_home_minus_away": round(market_elo_diff, 3),
            "model_elo_diff_home_minus_away": round(model_elo_diff, 3),
            "elo_market_gap": round(elo_market_gap, 3),
            "market_disagreement_away": round(abs(pm_away_nv - x_away_nv), 6),
            "market_disagreement_home": round(abs(pm_home_nv - x_home_nv), 6),
            "predicted_winner_market": home if x_home_nv >= x_away_nv else away,
            "predicted_winner_elo": home if elo_home_p >= elo_away_p else away,
            "decision": decision,
            "notes": g.get("notes", ""),
        })
    write_csv(output_csv, rows, list(rows[0].keys()) if rows else [])
    print(f"Wrote predictions: {output_csv}")

def review(predictions_csv: Path, results_csv: Path, elo_csv: Path, updated_elo_csv: Path, review_csv: Path) -> None:
    preds = read_csv(predictions_csv)
    results = {r["game_id"]: r for r in read_csv(results_csv)}
    elos = load_elos(elo_csv)
    rows = []
    for p in preds:
        if p["game_id"] not in results:
            continue
        r = results[p["game_id"]]
        if not r.get("away_score") or not r.get("home_score"):
            print(f"Skip {p['game_id']}: result not filled yet")
            continue

        away, home = p["away_team"], p["home_team"]
        away_score, home_score = int(r["away_score"]), int(r["home_score"])
        away_win = 1 if away_score > home_score else 0
        home_win = 1 - away_win
        actual_winner = away if away_win else home

        x_away_p = float(p["xlite_away_no_vig"])
        pm_away_p = float(p["pm_away_no_vig"])
        elo_away_p = float(p["elo_away_p"])

        brier_xlite = brier(x_away_p, away_win)
        brier_pm = brier(pm_away_p, away_win)
        brier_elo = brier(elo_away_p, away_win)

        away_elo_pre = float(p["away_elo_pre"])
        home_elo_pre = float(p["home_elo_pre"])
        expected_away = float(p["elo_away_p"])
        expected_home = float(p["elo_home_p"])

        away_elo_post = away_elo_pre + K_FACTOR * (away_win - expected_away)
        home_elo_post = home_elo_pre + K_FACTOR * (home_win - expected_home)

        elos[away] = away_elo_post
        elos[home] = home_elo_post

        rows.append({
            "game_id": p["game_id"], "date": p["date"], "away_team": away, "home_team": home,
            "away_score": away_score, "home_score": home_score, "actual_winner": actual_winner,
            "predicted_winner_market": p["predicted_winner_market"],
            "predicted_winner_elo": p["predicted_winner_elo"],
            "market_direction_correct": int(p["predicted_winner_market"] == actual_winner),
            "elo_direction_correct": int(p["predicted_winner_elo"] == actual_winner),
            "brier_1xlite": round(brier_xlite, 6),
            "brier_polymarket": round(brier_pm, 6),
            "brier_elo": round(brier_elo, 6),
            "away_elo_pre": round(away_elo_pre, 3), "home_elo_pre": round(home_elo_pre, 3),
            "away_elo_post": round(away_elo_post, 3), "home_elo_post": round(home_elo_post, 3),
            "decision": p["decision"],
        })

    if rows:
        write_csv(review_csv, rows, list(rows[0].keys()))
    else:
        print("No completed results found. Review file not written.")
    save_elos(updated_elo_csv, elos)
    print(f"Wrote review: {review_csv}")
    print(f"Wrote updated Elo: {updated_elo_csv}")

def main(argv):
    if len(argv) < 2:
        print("Usage:")
        print("  python wnba_math_engine.py init_elo_from_2025 team_baseline_2025.csv teams_elo_2025_based.csv")
        print("  python wnba_math_engine.py predict games.csv teams_elo.csv predictions.csv")
        print("  python wnba_math_engine.py review predictions.csv results.csv teams_elo.csv updated_elo.csv review.csv")
        raise SystemExit(1)

    cmd = argv[1].lower()
    if cmd == "init_elo_from_2025":
        if len(argv) not in (4, 5, 6):
            raise SystemExit("Usage: python wnba_math_engine.py init_elo_from_2025 baseline.csv output_elo.csv [alpha] [expansion_elo]")
        alpha = float(argv[4]) if len(argv) >= 5 else 20.0
        expansion_elo = float(argv[5]) if len(argv) >= 6 else 1450.0
        init_elo_from_2025(Path(argv[2]), Path(argv[3]), alpha=alpha, expansion_elo=expansion_elo)
    elif cmd == "predict":
        if len(argv) != 5:
            raise SystemExit("Usage: python wnba_math_engine.py predict games.csv teams_elo.csv predictions.csv")
        predict(Path(argv[2]), Path(argv[3]), Path(argv[4]))
    elif cmd == "review":
        if len(argv) != 7:
            raise SystemExit("Usage: python wnba_math_engine.py review predictions.csv results.csv teams_elo.csv updated_elo.csv review.csv")
        review(Path(argv[2]), Path(argv[3]), Path(argv[4]), Path(argv[5]), Path(argv[6]))
    else:
        raise SystemExit(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main(sys.argv)
