"""Regex-sync BCM constants between index.html (JS) and bayesian_engine.py."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

METRIC_KEYS = ("dlo_alignment", "cvd_divergence", "liquidity_sweep")


def _parse_js_metrics(text: str) -> dict[str, dict[str, float]]:
    # BCM_METRICS = { ... liquidity_sweep: { tpr: 0.60, fpr: 0.25 }, ...}
    block = re.search(r"const\s+BCM_METRICS\s*=\s*\{(.*?)\};", text, re.S)
    assert block, "BCM_METRICS not found in index.html"
    body = block.group(1)
    out = {}
    for key in METRIC_KEYS:
        m = re.search(
            rf"{key}\s*:\s*\{{\s*tpr\s*:\s*([0-9.]+)\s*,\s*fpr\s*:\s*([0-9.]+)\s*\}}",
            body,
        )
        assert m, f"JS metric {key} not found"
        out[key] = {"tpr": float(m.group(1)), "fpr": float(m.group(2))}
    return out


def _parse_py_metrics(text: str) -> dict[str, dict[str, float]]:
    out = {}
    for key in METRIC_KEYS:
        m = re.search(
            rf'"{key}"\s*:\s*\{{\s*"tpr"\s*:\s*([0-9.]+)\s*,\s*"fpr"\s*:\s*([0-9.]+)\s*\}}',
            text,
        )
        assert m, f"Py metric {key} not found"
        out[key] = {"tpr": float(m.group(1)), "fpr": float(m.group(2))}
    return out


def test_bcm_metrics_js_py_sync():
    js = (ROOT / "index.html").read_text(encoding="utf-8")
    py = (ROOT / "bayesian_engine.py").read_text(encoding="utf-8")
    js_m = _parse_js_metrics(js)
    py_m = _parse_py_metrics(py)
    assert js_m == py_m


def test_bcm_prior_and_threshold_sync():
    js = (ROOT / "index.html").read_text(encoding="utf-8")
    py = (ROOT / "bayesian_engine.py").read_text(encoding="utf-8")
    js_prior = float(re.search(r"const\s+BCM_PRIOR\s*=\s*([0-9.]+)", js).group(1))
    js_thr = float(re.search(r"const\s+BCM_THRESHOLD\s*=\s*([0-9.]+)", js).group(1))
    # Python defaults in __init__
    m_prior = re.search(r"base_win_rate\s*:\s*float\s*=\s*([0-9.]+)", py)
    m_thr = re.search(r"threshold\s*:\s*float\s*=\s*([0-9.]+)", py)
    assert m_prior and m_thr
    assert js_prior == float(m_prior.group(1))
    assert js_thr == float(m_thr.group(1))


def test_sweep_lr_comment_mentions_2_4():
    js = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "LR 2.4" in js or "LR ≈ 2.4" in js or "LR 2.4" in js
    py = (ROOT / "bayesian_engine.py").read_text(encoding="utf-8")
    assert "2.4" in py
