"""Unit tests for BayesianConvictionEngine."""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bayesian_engine import BayesianConvictionEngine  # noqa: E402


def test_no_prior_returns_zero():
    eng = BayesianConvictionEngine(base_win_rate=0.60, threshold=90.0)
    score, act = eng.evaluate_tick(False, True, True, True)
    assert score == 0.0
    assert act is False


def test_all_three_evidence_actionable():
    eng = BayesianConvictionEngine(base_win_rate=0.60, threshold=90.0)
    score, act = eng.evaluate_tick(True, True, True, True)
    # prior 0.6, LRs 2.5 * 3.0 * 2.4 = 18 → ~96.43
    assert act is True
    assert 96.0 <= score <= 97.0


def test_sweep_lr_is_2_4():
    eng = BayesianConvictionEngine()
    stats = eng.evidence_metrics["liquidity_sweep"]
    assert stats["tpr"] == 0.60
    assert stats["fpr"] == 0.25
    lr = eng._calculate_likelihood_ratio("liquidity_sweep", True)
    assert math.isclose(lr, 2.4)


def test_yes_only_two_of_three_clear_90():
    """Documented property: product of any two yes-LRs clears 90 at prior 0.60
    when absent evidence is treated as LR=1 (comment in BCM_METRICS)."""
    prior = 0.60
    odds = prior / (1 - prior)
    lrs = {
        "dlo": 0.75 / 0.30,
        "cvd": 0.60 / 0.20,
        "sweep": 0.60 / 0.25,
    }
    combos = [
        ("dlo", "cvd"),
        ("dlo", "sweep"),
        ("cvd", "sweep"),
    ]
    for a, b in combos:
        post_odds = odds * lrs[a] * lrs[b]
        sureness = 100 * post_odds / (1 + post_odds)
        assert sureness >= 90.0, (a, b, sureness)


def test_process_signals_requires_columns():
    eng = BayesianConvictionEngine()
    try:
        import pandas as pd
    except ImportError:
        return
    df = pd.DataFrame({"hl_momentum_trigger": [True]})
    try:
        eng.process_signals(df)
        assert False, "expected ValueError"
    except ValueError as e:
        assert "Missing required column" in str(e)
