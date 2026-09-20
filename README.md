# Bayesian Screener

Hyperliquid momentum screener. Display scores **90–100** only when BCM Sureness clears 90.

## The gate

| Band | Rule |
|------|------|
| −100…89 | Momentum + attention (multi-TF, SuperTrend, OI Δ, RS, funding / premium / RVol / retail heat) |
| **90–100** | **BCM only** — Sureness ≥ 90. Momentum alone is capped at **89**. |

`BCM ★` / green HP long box = prior updated with evidence and cleared for leveraged-long risk. Red box = optimized short.

## BCM (Bayesian Conviction Multiplier)

**Prior:** Hyperliquid momentum long trigger (~60% base).

**Evidence** (likelihood ratios):

1. **DLO** — macro / regime (BTC liquidity + SuperTrend + 4H/1D structure)
2. **CVD** — aggressive long flow (OI↑ with price↑)
3. **Sweep** — 15m stop-run below locals, then reclaim

```
posterior ∝ prior × LR(DLO) × LR(CVD) × LR(Sweep)
Sureness = posterior × 100
```

Reference: [`bayesian_engine.py`](./bayesian_engine.py)

## Run

Open the live page (no install):

**https://millennialinformaticist.github.io/Bayesian.xyz/**

Or locally: open `index.html`, or `python3 -m http.server 8080` → http://localhost:8080

Optional: **Enable score-jump push** in the page (ladder `40 → 80 → 90 → 100`; 90/100 need BCM).

## Keyboard

`?` help · `/` filter · `j`/`k` rows · `Enter` open on Hyperliquid · `1`–`5` views · `r` refresh · `p` push · `s` sort

## Data

Hyperliquid public `/info` + CoinGecko trending. No API keys.

## License

MIT
