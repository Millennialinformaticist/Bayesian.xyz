# Hyperliquid MCP Server (Vetted + Docker)

Sandboxed MCP server for read-only Hyperliquid market data. Vendored from
[`@mektigboy/server-hyperliquid`](https://github.com/mektigboy/server-hyperliquid)
with security fixes and Docker hardening.

See [SECURITY.md](./SECURITY.md) for the full audit and threat model.

## Tools

| Tool | Description |
|------|-------------|
| `get_all_mids` | Mid prices for all coins |
| `get_candle_snapshot` | Historical candlestick data |
| `get_l2_book` | L2 order book snapshot |

## Quick Start

### 1. Build the Docker image

```bash
cd mcp/hyperliquid
docker build -t hyperliquid-mcp:0.0.1-vetted .
```

### 2. Smoke test

Requires Docker Desktop running. If Docker is unavailable, use the local fallback:

```bash
./scripts/smoke-test-local.sh
```

With Docker:

```bash
./scripts/smoke-test.sh
```

### 3. Add to Cursor

Copy the example config into your project:

```bash
mkdir -p .cursor
cp mcp/hyperliquid/examples/mcp.json .cursor/mcp.json
```

Or merge the `hyperliquid` entry from `examples/mcp.json` into your existing
`.cursor/mcp.json`. Restart Cursor and confirm the server shows as connected in
Settings → MCP.

## Cursor Configuration

```json
{
  "mcpServers": {
    "hyperliquid": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--read-only",
        "--tmpfs", "/tmp:rw,noexec,nosuid,size=16m",
        "--cap-drop=ALL",
        "--security-opt", "no-new-privileges",
        "hyperliquid-mcp:0.0.1-vetted"
      ]
    }
  }
}
```

## Testnet (optional)

Add an environment variable to the docker args:

```json
"-e", "HYPERLIQUID_API_URL=https://api.hyperliquid-testnet.xyz"
```

Only mainnet and testnet URLs are allowed.

## Local Development (without Docker)

```bash
npm ci
npm run build
npm start
```

Use the MCP Inspector for interactive testing:

```bash
npm run inspect
```

## Changes from Upstream

1. Fixed `get_all_mids` — no longer requires empty args object
2. Fixed `get_candle_snapshot` — accepts `coin` param as documented
3. Fixed `get_l2_book` tool JSON schema
4. Reduced stderr logging (tool name only)
5. Allowlisted `HYPERLIQUID_API_URL` env var
6. Pinned dependencies, no `prepare` script on install
7. Docker sandbox with read-only root and dropped capabilities

## License

MIT (upstream and this fork)
