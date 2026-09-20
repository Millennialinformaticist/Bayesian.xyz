# Bayesian Screener

Hyperliquid momentum screener whose **edge is Bayesian, not just momentum**.

## What makes this unique

Most screeners print a high score when price + OI + trend look hot. That is necessary — and not sufficient for leveraged risk.

**Bayesian Screener reserves the entire 90–100 band for one thing only: BCM clearance.**

| Score | How you get there |
|------:|-------------------|
| −100…89 | Momentum stack + attention (multi-TF, SuperTrend, OI Δ, RS, funding / premium / RVol / retail heat) |
| **90–100** | **BCM only** — Bayesian *Sureness* ≥ 90. Raw momentum is hard-capped at **89** without it. |

If you see **90–100** or **BCM ★**, the model has updated a prior with evidence and cleared an actionable leveraged-long threshold — not a cosmetics boost on a hot tape.

That gate is the product.

## Bayesian Conviction Multiplier (BCM)

**Prior** — Hyperliquid momentum long trigger (~60% base win rate).

**Evidence** (likelihood ratios, naive Bayes / conditional independence):

1. **DLO** — macro / regime alignment (BTC liquidity env + asset SuperTrend + 4H/1D structure)
2. **CVD** — aggressive long-flow proxy (OI↑ with price↑)
3. **Liquidity sweep** — 15m stop-run below local lows, then reclaim

```
posterior ∝ prior × LR(DLO) × LR(CVD) × LR(Sweep)
Sureness = posterior × 100
```

- **Sureness ≥ 90** → Actionable Leveraged Long (`BCM ★`), score printed in **90–100**
- **Otherwise** → momentum may look strong, but display score **cannot exceed 89**

Python reference: [`bayesian_engine.py`](./bayesian_engine.py)

```python
from bayesian_engine import BayesianConvictionEngine
engine = BayesianConvictionEngine(base_win_rate=0.60, threshold=90.0)
results = engine.process_signals(df)  # Sureness_Score, Actionable_Leveraged_Long
```

Refresh `evidence_metrics` TPR/FPR from your own trade logs so LRs track live regimes.

## Quick start

1. Open [`index.html`](./index.html) in Chrome / Edge / Brave  
   (or `python3 -m http.server 8080` → `http://localhost:8080`)
2. Click **Enable score-jump push** and allow notifications
3. Leave the tab open

Live preview:  
https://htmlpreview.github.io/?https://raw.githubusercontent.com/Millennialinformaticist/Bayesian.xyz/main/index.html

## Liquidity banner (BTC → alts)

Top chip frames BTC as liquidity for alt beta:

| Chip | Meaning |
|------|---------|
| **LIQUIDITY · EXPANDING** | BTC bid present — alt risk appetite open |
| **LIQUIDITY · MIXED** | BTC unstable / chop — require HP confirmation |
| **LIQUIDITY · CONTRACTING** | BTC distribution — alt longs suppressed |
| **LIQUIDITY · SCANNING** | Awaiting BTC flow & structure |

## Push alerts

Other alerts muted. Browser push only on ladder jumps:

`40 → 80 → 90 → 100` (shorts `−40 → −80 → −100`)

**90 / 100 require BCM clearance.** Perfect ±100 stays until dismissed.

## Keyboard (desk-first)

- `?` help · `/` filter · `j`/`k` move · `Enter` open on Hyperliquid
- `1`–`5` views (All / HP / Longs / Shorts / Setups) · `r` refresh · `p` push · `s` sort score · `h` legend
- Optimized **long** rows: green box · optimized **short** rows: red box
- Desk chrome aligned with Gambit Terminal (Archivo + Spline Sans Mono)

## Data

- Hyperliquid public `/info` (meta, candles, funding, premium, OI)
- CoinGecko trending (retail heat proxy)
- No API keys for the default build

## License

MIT
