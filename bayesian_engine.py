"""
BCM — Bayesian Conviction Multiplier.

Prior = HL momentum long trigger. Evidence = DLO, CVD Proxy, Sweep (naive Bayes LRs).
Sureness 0–100; >= 90 → Actionable_Leveraged_Long.
Browser screener: display scores 90–100 only when Sureness clears 90.
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

try:
    import pandas as pd
except ImportError:  # optional for the pure-tick path
    pd = None  # type: ignore


class BayesianConvictionEngine:
    """
    Applies Bayesian updating to High-Low momentum signals to filter for
    90–100% confidence setups suitable for leveraged longs.
    """

    def __init__(self, base_win_rate: float = 0.60, threshold: float = 90.0):
        self.prior_prob = base_win_rate
        self.prior_odds = self.prior_prob / (1.0 - self.prior_prob)
        self.threshold = threshold

        # Historical (TPR, FPR) — refresh from your trade logs periodically.
        self.evidence_metrics: Dict[str, Dict[str, float]] = {
            "dlo_alignment": {"tpr": 0.75, "fpr": 0.30},   # LR ≈ 2.5
            "cvd_divergence": {"tpr": 0.60, "fpr": 0.20},  # LR ≈ 3.0
            "liquidity_sweep": {"tpr": 0.60, "fpr": 0.25}, # LR ≈ 2.4; yes-only 2-of-3 clear 90 @ prior 0.60
        }

    def _calculate_likelihood_ratio(self, metric_name: str, condition_met: bool) -> float:
        stats = self.evidence_metrics.get(metric_name)
        if not stats:
            return 1.0
        # Sparse evidence: inactive → LR 1 (uninformative), not a negative update.
        if not condition_met:
            return 1.0
        return stats["tpr"] / stats["fpr"]

    def evaluate_tick(
        self,
        hl_signal: bool,
        dlo_active: bool,
        cvd_active: bool,
        sweep_active: bool,
    ) -> Tuple[float, bool]:
        if not hl_signal:
            return 0.0, False

        lr_dlo = self._calculate_likelihood_ratio("dlo_alignment", dlo_active)
        lr_cvd = self._calculate_likelihood_ratio("cvd_divergence", cvd_active)
        lr_sweep = self._calculate_likelihood_ratio("liquidity_sweep", sweep_active)

        combined_lr = lr_dlo * lr_cvd * lr_sweep
        posterior_odds = self.prior_odds * combined_lr
        posterior_prob = posterior_odds / (1.0 + posterior_odds)

        sureness_score = posterior_prob * 100.0
        is_actionable = sureness_score >= self.threshold
        return round(sureness_score, 2), is_actionable

    def process_signals(self, df: "pd.DataFrame") -> "pd.DataFrame":
        if pd is None:
            raise ImportError("pandas is required for process_signals")
        required = [
            "hl_momentum_trigger",
            "dlo_condition",
            "cvd_condition",
            "sweep_condition",
        ]
        for col in required:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        scores, actionable = [], []
        for _, row in df.iterrows():
            score, act = self.evaluate_tick(
                bool(row["hl_momentum_trigger"]),
                bool(row["dlo_condition"]),
                bool(row["cvd_condition"]),
                bool(row["sweep_condition"]),
            )
            scores.append(score)
            actionable.append(act)

        out = df.copy()
        out["Sureness_Score"] = scores
        out["Actionable_Leveraged_Long"] = actionable
        return out


if __name__ == "__main__":
    eng = BayesianConvictionEngine(base_win_rate=0.60, threshold=90.0)
    # Tick-level smoke (no pandas required)
    demos = [
        ("all three", True, True, True, True),
        ("DLO+CVD", True, True, True, False),
        ("DLO+Sweep", True, True, False, True),
        ("CVD+Sweep", True, False, True, True),
        ("none", True, False, False, False),
        ("no prior", False, True, True, True),
    ]
    for label, hl, dlo, cvd, sw in demos:
        score, act = eng.evaluate_tick(hl, dlo, cvd, sw)
        print(f"{label:12} sureness={score:6.2f} actionable={act}")
    if pd is not None:
        mock = pd.DataFrame(
            {
                "timestamp": pd.date_range("2026-09-20", periods=4, freq="min"),
                "hl_momentum_trigger": [True, True, True, False],
                "dlo_condition": [True, False, True, True],
                "cvd_condition": [True, True, True, False],
                "sweep_condition": [True, False, False, False],
            }
        )
        print(eng.process_signals(mock)[
            ["timestamp", "Sureness_Score", "Actionable_Leveraged_Long"]
        ])
