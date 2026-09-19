# HL Momentum Survey

Browser-based Hyperliquid momentum screener. Single static HTML file — open locally, no backend.

## Features

- Multi-timeframe momentum stack (15m → 3M)
- 4H SuperTrend confirmation
- Open interest Δ (~15m local cache)
- Attention layer: funding, premium, relative volume, CoinGecko search heat
- Conviction score (−100…+100) with ★ HP LONG / SHORT ranking
- **Push-only alerts**: all other alerts muted; browser notifications only on score ladder jumps **40 → 80 → 100** (and short −40 → −80 → −100). Perfect ±100 stays until dismissed.

## Quick start

1. Download / clone this repo
2. Open `index.html` (or `WORKINGHLSCAN.html`) in Chrome / Edge / Brave
3. Click **Enable score-jump push** and allow notifications
4. Leave the tab open — OI polls every 2m, full rescore every 5m

> Tip: serve over `http://localhost` if your browser restricts `file://` notifications:
> `python3 -m http.server 8080` then visit `http://localhost:8080`

## Score model (summary)

| Component | Role |
|-----------|------|
| TF stack | Aligned trend across horizons |
| SuperTrend 4H | Regime gate |
| OI confirm | Money following price |
| RS vs BTC | Relative strength for alts |
| Attention | Funding crowding, premium, RVol, CG heat |
| Stretch penalty | Avoid chasing parabolic extensions |

Default view: HP setups. Highest-conviction longs are bold + green-outlined at the top.

## Data

- Hyperliquid public `/info` API (meta, candles, funding, premium, OI)
- CoinGecko public trending search (retail attention proxy)

No API keys required for the default build. X / Google Trends need keys or a proxy — not included.

## Privacy

OI snapshots and score history stay in your browser `localStorage`. Nothing is sent to a third-party backend by this page.

## License

MIT
