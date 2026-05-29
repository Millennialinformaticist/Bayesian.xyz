
- Node.js v18+
- A Hyperliquid account with USDC deposited
- A Hyperliquid API wallet (generated in the Hyperliquid UI under Settings → API)
- The wallet address of the trader you want to copy

---

### 1. Clone the Repository

```bash
git clone https://github.com/zkOSAI/hyperliquid-copy-trading-bot.git
cd hyperliquid-copy-trading-bot
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Copy the example env file:

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
TRADER_ADDRESS=       # Address to copy trade
USER_ADDRESS=         # Your Hyperliquid address (not the API address)
USER_PRIVATE_KEY=     # Your wallet private key
COPY_VALUE=250        # USDC amount to copy with each trade
MAX_LEVERAGE=10       # Maximum leverage to use
```

> **Security Note:** Never share your `.env` file or commit it to Git. `USER_PRIVATE_KEY` is your API/agent wallet private key only — not your main wallet.

### 4. Start the Bot

```bash
npm start
```

The bot will connect to Hyperliquid's WebSocket, begin monitoring the target trader, and log all activity to your console.

---

## Environment Variables Reference

| Variable | Description |
|---|---|
| `TRADER_ADDRESS` | The Hyperliquid wallet address you want to mirror |
| `USER_ADDRESS` | Your own Hyperliquid account address (not the API key address) |
| `USER_PRIVATE_KEY` | Private key of your wallet |
| `COPY_VALUE` | USDC amount per copied trade (e.g. `250`) |
| `MAX_LEVERAGE` | Hard cap on leverage (e.g. `10` = max 10x) |




---

## How It Works

1. Bot connects to Hyperliquid WebSocket and watches the `TRADER_ADDRESS`
2. When a new position opens, the bot calculates your mirrored position using `COPY_VALUE` and caps leverage at `MAX_LEVERAGE`
3. Bot places the same trade on your account via the Hyperliquid API
4. When the trader closes or modifies the position, your position is updated to match

---

## Risk Disclaimer

Copy trading does **not** guarantee profits. Past performance of any trader is not indicative of future results. Crypto perpetuals trading involves significant risk including total loss of capital. Start with small `COPY_VALUE` amounts and never trade with money you cannot afford to lose. This software is provided as-is for educational and personal use.

---

## Contributing

PRs and issues are welcome. If you've found a bug fix or profitable improvement, open a pull request.

---

## Contact

Tg: @soladity

## Support

If this bot has been useful to you, drop a ⭐ on GitHub — it helps others find the project.

---

*Built for the Hyperliquid community. Trade smart. Manage risk.*
