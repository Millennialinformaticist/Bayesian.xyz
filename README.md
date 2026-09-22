# Bayesian.xyz

**Hyperliquid momentum screener with multi-timeframe scoring and Bayesian confirmation.**

Bayesian.xyz scans Hyperliquid perpetual markets and combines multi-timeframe momentum, market structure, derivatives positioning, relative strength, market attention, and liquidity behavior into a single directional score.

A Bayesian Conviction Multiplier (BCM) provides an additional confirmation layer for the highest-confidence setups.

**This is a market-screening and decision-support tool. It does not execute trades.**

## What it does

The system continuously evaluates Hyperliquid markets and asks:

> **Which markets currently have the strongest combination of momentum, structure, positioning, and confirmation?**

Each market receives a directional score from:

```text
-100  ← strongly bearish
   0  ← neutral
+100  ← strongly bullish
```

The score incorporates:

- 15m, 1H, 4H, 1D, and 1W momentum
- 4H SuperTrend
- Open-interest direction
- Price/OI relationship
- Relative strength versus BTC
- Funding
- Hyperliquid premium
- Relative volume
- Market attention
- Liquidity-sweep behavior
- BTC market regime

The result is a ranked view of markets exhibiting meaningful directional conditions.

---

# Signal Architecture

The system is intentionally structured as a series of filters rather than a single prediction model.

```text
                 Hyperliquid
                     │
        ┌────────────┼────────────┐
        │            │            │
      Price          OI        Funding
      Candles                   Premium
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
              Market Survey
                     │
        ┌────────────┼────────────┐
        │            │            │
    Multi-TF      Structure    Positioning
    Momentum     SuperTrend     OI / Flow
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
              Momentum Score
                -100 to +100
                     │
                     ▼
              BTC Regime Filter
                     │
                     ▼
             BCM Evidence Layer
                     │
        ┌────────────┼────────────┐
        │            │            │
       DLO       CVD Proxy      Sweep
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
             Bayesian Update
                     │
                     ▼
              BCM Sureness
                     │
          ┌──────────┴──────────┐
          │                     │
       < 90                    ≥ 90
          │                     │
     Normal setup         BCM-confirmed
                            long setup
```

The important distinction is:

**Momentum finds candidates.  
Bayesian confirmation determines whether the evidence is strong enough to promote them.**

---

# Multi-Timeframe Momentum

The base model evaluates price movement across:

```text
15m
1H
4H
1D
1W
```

The timeframes are weighted differently, with greater weight given to higher timeframes.

This allows the system to distinguish between:

- Short-term momentum
- Developing trends
- Established trends
- Higher-timeframe confirmation

A market moving higher across several timeframes receives a positive contribution, while conflicting timeframes reduce the directional score.

---

# Market Structure

The screener incorporates 4H SuperTrend as a major structural component.

Additional structure factors include:

- SuperTrend direction
- Distance from SuperTrend reversal
- 4H momentum
- 1D momentum
- Trend alignment
- Extension from recent price movement

The model also attempts to avoid blindly rewarding already-extended moves.

For example, excessive positive 4H or 1D movement can reduce the score rather than continuously increasing it.

This is intended to distinguish:

```text
Healthy momentum
```

from:

```text
Potentially crowded / extended momentum
```

---

# Open Interest

Open interest provides derivatives-positioning context.

The model evaluates OI direction alongside price movement.

Examples:

```text
Price ↑ + OI ↑
```

can contribute positively to a bullish setup.

```text
Price ↓ + OI ↑
```

can contribute negatively and may indicate increasing positioning during a decline.

The model also considers:

```text
Price ↑ + OI ↓
Price ↓ + OI ↓
```

as different positioning environments rather than treating OI direction independently.

---

# Relative Strength Versus BTC

Altcoins are evaluated relative to BTC.

The model compares:

- 4H performance
- 1D performance

between the asset and BTC.

For example:

```text
Asset 4H: +8%
BTC 4H:   +3%
```

produces positive relative strength.

Conversely:

```text
Asset 4H: +2%
BTC 4H:   +6%
```

produces negative relative strength.

This helps identify assets demonstrating independent strength rather than simply following the market.

---

# Market Attention

The system incorporates market attention as an additional contextual factor.

Attention is intended to separate assets that have similar technical conditions but significantly different levels of market interest.

The model considers:

- Trending status
- Funding
- Premium
- Relative volume

Attention is not treated as an independent buy signal.

Instead, it modifies the underlying momentum score.

---

# BTC Regime

BTC is treated as the primary market-regime signal.

The system classifies the environment into:

```text
LIQUIDITY · EXPANDING
LIQUIDITY · MIXED
LIQUIDITY · CONTRACTING
```

The classification considers:

- BTC 4H momentum
- BTC SuperTrend
- BTC price versus longer-term moving averages
- BTC 1W performance
- BTC market structure

The purpose is to prevent an individual altcoin signal from being interpreted independently of the broader BTC environment.

When BTC enters a contracting/distributionary regime, bullish altcoin scores can be suppressed.

---

# Bayesian Conviction Multiplier

The **Bayesian Conviction Multiplier (BCM)** is the confirmation layer.

It does not replace the momentum model.

Instead, BCM answers a narrower question:

> **Does the bullish momentum signal have enough additional evidence to qualify as a high-conviction setup?**

The model begins with a prior probability:

```text
Prior = 60%
```

It then updates that probability using three evidence layers:

1. DLO
2. CVD Proxy
3. Liquidity Sweep

The resulting posterior probability becomes the **BCM Sureness** value.

---

# DLO

DLO is the system's directional liquidity/regime alignment layer.

The current implementation considers:

- BTC regime
- Asset 4H SuperTrend
- 4H price performance
- 1D price performance

The purpose is to determine whether the broader market environment and asset structure are aligned with continued upside.

---

# CVD Proxy

The current implementation **does not use true Cumulative Volume Delta (CVD).**

Instead, it uses:

```text
Open Interest ↑
+
Price ↑
```

as a proxy for aggressive long participation.

This is intentionally described as a **CVD Proxy** rather than CVD.

The architecture allows this component to be replaced by a true CVD/order-flow feed in the future without changing the overall Bayesian framework.

---

# Liquidity Sweep

The liquidity-sweep detector examines recent 15-minute candles for a stop-run and reclaim pattern.

Conceptually:

```text
Price trades below recent local low
              ↓
       Liquidity is taken
              ↓
     Price reclaims the level
              ↓
       Sweep confirmation
```

The current implementation looks for a candle that:

- Trades below a recent local low
- Closes back above that level
- Contains a meaningful lower wick

This is intended to identify potential liquidity grabs followed by reclaim behavior.

---

# Bayesian Calculation

BCM uses likelihood ratios to update the prior probability.

Conceptually:

```text
Prior Odds
     ×
DLO Likelihood Ratio
     ×
CVD Proxy Likelihood Ratio
     ×
Sweep Likelihood Ratio
     =
Posterior Odds
```

The current model uses:

| Evidence | TPR | FPR | Likelihood Ratio |
|---|---:|---:|---:|
| DLO alignment | 0.75 | 0.30 | 2.50 |
| CVD Proxy | 0.60 | 0.20 | 3.00 |
| Liquidity Sweep | 0.50 | 0.25 | 2.00 |

The posterior probability is converted into a percentage and displayed as:

**BCM Sureness**

---

# The 90+ Gate

One of the defining characteristics of the model is that the **90–100 score range is reserved for BCM-confirmed setups.**

The process is:

```text
Raw momentum score
        ↓
Bullish structure?
        ↓
BCM evidence
        ↓
Bayesian update
        ↓
Sureness ≥ 90?
        ↓
      YES
        ↓
90–100 score permitted
```

If the raw momentum model produces a score of 90 or greater but BCM does not clear the threshold, the score is capped at:

```text
89
```

This creates an explicit distinction between:

```text
Strong technical momentum
```

and:

```text
Strong technical momentum
+
Bayesian confirmation
```

---

# Signal Classification

The screener uses the score and structure to classify setups.

### BCM

```text
BCM Sureness ≥ 90
```

The highest-confidence bullish classification in the current model.

### LONG

Bullish momentum and structure meet the normal setup threshold, but BCM confirmation is not sufficient to promote the signal into the 90–100 band.

### SHORT

Bearish momentum and structure satisfy the short setup conditions.

### HP SHORT (mom)

A higher-priority **momentum-only** short (UI label: `HP SHORT (mom)`). It does **not** use BCM Sureness; it is the bearish mirror of strong raw momentum + structure, not a calibrated short-side posterior.

### No Setup

The available evidence is not sufficiently directional.

---

# Score Interpretation

The score should be interpreted as a **model output**, not a probability of profit.

A simplified interpretation:

```text
+90 to +100   BCM-confirmed bullish setup
+70 to +89    Strong bullish momentum
+55 to +69    Developing bullish setup
-54 to +54    No strong directional setup
-70 to -55    Developing bearish setup
≤ -70         Strong bearish conditions
```

The exact trading significance of any score must be evaluated through historical testing and live performance data.

---

# Alerts

The screener supports score-jump notifications.

Examples include:

```text
40 → 80
80 → 90
90 → 100
```

and significant bearish transitions such as:

```text
-40 → -80
-80 → -100
```

Browser notifications and audio alerts are supported.

Alert history is stored locally in the browser to reduce repeated notifications from the same threshold transition.

---

# 15m HMA Scanner

[`HMA9-15m-cross-scanner.html`](./HMA9-15m-cross-scanner.html) is a separate scanner included in the repository.

It monitors Hyperliquid perpetual markets for:

```text
Price crossing ABOVE the 9-period HMA
on the 15-minute timeframe
```

The scanner tracks states including:

```text
BELOW
ARMING
FIRE
ABOVE
```

It supports:

- Hyperliquid market scanning
- Up to 80 markets
- Lighter / LIT prioritization
- Automatic scanning
- 30-second refresh
- Sound alerts
- Browser notifications
- Duplicate alert suppression

The HMA scanner is independent from the primary Bayesian scoring engine.

---

# Data Sources

The primary market data source is the public Hyperliquid `/info` API.

The screener uses Hyperliquid data for:

- Market metadata
- Candles
- Prices
- Open interest
- Funding
- Premium

CoinGecko's public trending endpoint is used as an additional market-attention input.

No Hyperliquid API key is required for the public market-data functionality.

---

# Rate limits

The public Hyperliquid `/info` endpoint is rate-limited. The screener retries on HTTP 429 with backoff, uses modest concurrency, and caches **1D candles for 45 minutes** to cut repeat traffic.

For higher limits, point the browser at a QuickNode Hyperliquid `/info` URL **without putting the token in source**:

```js
localStorage.setItem("hl_qn_info_url", "https://YOUR.quiknode.pro/<TOKEN>/hyperliquid/hl/info")
```

`index.html` reads `localStorage.hl_qn_info_url` via `getHlInfoUrl()` and otherwise uses `https://api.hyperliquid.xyz/info`. See `.env.example` for the optional `HL_QN_INFO_URL` documentation alias (static HTML does not load `.env`).

Never hardcode QuickNode (or other) tokens in the repository.

---

# Running Locally

The primary application is a static browser application.

Clone the repository and open:

```text
index.html
```

Python BCM engine + constant-sync tests:

```bash
pip install -r requirements-dev.txt
pytest
python bayesian_engine.py
```

Alternatively, run a local HTTP server:

```text
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

No Python package installation is required for the primary browser screener.

Live page: **https://millennialinformaticist.github.io/Bayesian.xyz/**

---

# Repository Structure

```text
Bayesian.xyz/
│
├── index.html
│   Main Hyperliquid momentum screener
│
├── bayesian_engine.py
│   Python implementation of the Bayesian conviction logic
│
├── HMA9-15m-cross-scanner.html
│   Independent 15m 9-HMA cross scanner
│
├── .env.example
│   Optional configuration example
│
└── LICENSE
    MIT License
```

---

# Limitations

Bayesian.xyz is an experimental quantitative screening system.

Several components should be understood as model assumptions rather than empirically validated probabilities.

## Fixed Bayesian Parameters

The current implementation uses a fixed:

```text
Prior = 60%
```

and fixed TPR/FPR assumptions for the BCM evidence layers.

These values are currently specified by the model rather than continuously estimated from a historical outcome database.

## CVD Proxy

The current CVD implementation is a proxy based on:

```text
OI ↑ + Price ↑
```

It is not actual cumulative volume delta.

True order-flow/CVD data would provide a more direct measurement of aggressive buying and selling.

## No Automated Calibration

The current system does not automatically:

- Backtest BCM outcomes
- Re-estimate TPR/FPR
- Recalculate the prior
- Optimize thresholds
- Track signal expectancy
- Perform walk-forward validation

These are logical next steps for a production quantitative research system.

## No Trade Execution

Bayesian.xyz does not place orders.

It does not manage:

- Position size
- Leverage
- Stop losses
- Take profits
- Liquidation risk
- Portfolio exposure

Those decisions remain outside the screener.

## Model Output Is Not a Guaranteed Probability

A BCM Sureness of 93 does **not** mean:

```text
93% probability of profit
```

**Sureness is illustrative.** It is the posterior under a **fixed prior (0.60)** and **fixed TPR/FPR** likelihood ratios (not empirically calibrated live win-rates). It is a ranking / gate metric for promoting longs into the 90–100 band, not a promised P(win).

It means that, **under the current prior, likelihood assumptions, and evidence model**, the calculated posterior reaches 93%.

The Bayesian output is only as reliable as the assumptions and empirical calibration behind it.

---

# Roadmap

Potential future development includes:

### Order Flow

- Replace CVD Proxy with true CVD
- Add bid/ask imbalance
- Add liquidation data
- Add aggressive buy/sell volume

### Bayesian Calibration

- Store historical signals
- Track subsequent returns
- Track maximum favorable excursion
- Track maximum adverse excursion
- Estimate empirical TPR/FPR
- Dynamically estimate the prior
- Calibrate BCM thresholds

### Backtesting

- Historical replay
- Walk-forward testing
- Out-of-sample validation
- Regime-specific performance
- Signal decay analysis
- Expected-value analysis

### Risk

- Volatility-adjusted position sizing
- ATR-based stops
- Liquidation-distance analysis
- Maximum portfolio exposure
- Correlation-aware sizing

### Market Regimes

- BTC volatility regime
- Funding regime
- OI regime
- Liquidity regime
- Risk-on/risk-off classification
- Cross-asset confirmation

---

# Design Philosophy

Bayesian.xyz is built around a simple progression:

```text
Universe
   ↓
Momentum
   ↓
Structure
   ↓
Positioning
   ↓
Relative Strength
   ↓
Market Attention
   ↓
BTC Regime
   ↓
Bayesian Evidence
   ↓
High-Conviction Setup
```

The objective is not to predict every market movement.

The objective is to identify situations where **multiple independent pieces of market information point in the same direction**, then explicitly distinguish ordinary momentum from setups that satisfy the additional BCM confirmation layer.

**Momentum finds the candidates.**

**Bayesian confirmation promotes the candidates with sufficient supporting evidence.**
