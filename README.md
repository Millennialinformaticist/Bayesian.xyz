# Bayesian.xyz

Browser-based Hyperliquid momentum screener with a **Bayesian Conviction Multiplier (BCM)** gate for the 90–100 score band (actionable leveraged longs).

## Quick start

1. Clone / download
2. Open `index.html` in Chrome / Edge / Brave  
   (or `python3 -m http.server 8080` → `http://localhost:8080`)
3. Click **Enable score-jump push** and allow notifications
4. Leave the tab open

## Scoring

| Band | Meaning |
|------|---------|
| −100…89 | Momentum stack + attention (TF, SuperTrend, OI, RS, funding/prem/RVol/CG heat) |
| **90–100** | **BCM only** — Sureness from Bayesian update; not reachable by raw momentum |

### BCM (Bayesian Conviction Multiplier)

Prior = HL momentum long trigger (~60% base win rate).  
Likelihood ratios from three evidence layers (naive Bayes / conditional independence):

1. **DLO** — macro regime alignment (BTC env + asset SuperTrend + 4H/1D)
2. **CVD** — aggressive long flow proxy (OI↑ with price↑)
3. **Liquidity Sweep** — 15m stop-run wick below locals then reclaim

`Sureness_Score = posterior × 100`. **≥ 90 → Actionable Leveraged Long** (`BCM ★`).

Python reference implementation: [`bayesian_engine.py`](./bayesian_engine.py)

```python
from bayesian_engine import BayesianConvictionEngine
engine = BayesianConvictionEngine(base_win_rate=0.60, threshold=90.0)
results = engine.process_signals(df)  # Sureness_Score, Actionable_Leveraged_Long
```

Refresh `evidence_metrics` TPR/FPR from your trade logs so LRs track live regimes.

## Push alerts

All other alerts muted. Browser push only on ladder jumps:

`40 → 80 → 90 → 100` (and short `−40 → −80 → −100`)

90 / 100 require BCM clearance. Perfect ±100 stays until dismissed.

## Data

- Hyperliquid public `/info` (meta, candles, funding, premium, OI)
- CoinGecko trending (retail heat proxy)
- No API keys for the default build

## License

MIT
