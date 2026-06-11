# Security Review: Hyperliquid MCP Server

This document records the security review of the upstream
[`@mektigboy/server-hyperliquid`](https://github.com/mektigboy/server-hyperliquid)
package and the hardening applied in this vetted fork.

## Threat Model

| Asset | Risk if compromised |
|-------|---------------------|
| Wallet / private keys | **Not applicable** — server uses read-only `PublicClient` only |
| Local filesystem | Low — container runs read-only with no file I/O in server code |
| Network egress | Medium — server makes HTTPS requests; limited to Hyperliquid API |
| Cursor / MCP host | Medium — malicious server could exfiltrate prompts via tool responses |

## Scope

**In scope:** Public market data (mid prices, candles, L2 book) via Hyperliquid info API.

**Out of scope:** Trading, order placement, wallet signing, account queries requiring authentication.

## Upstream Audit Findings

Reviewed: GitHub source (Mar 2025) and npm package `@mektigboy/server-hyperliquid@0.0.1`.

| Severity | Finding | Status in vetted fork |
|----------|---------|----------------------|
| Low | No `fs`, `child_process`, or `eval` usage | Unchanged (safe) |
| Low | No secrets or env vars read by upstream | Added allowlisted `HYPERLIQUID_API_URL` only |
| Low | Zod `.strict()` input validation | Preserved + fixed schema mismatches |
| Medium | `npx -y` unpinned supply chain | **Mitigated** — vendored source, pinned lockfile, Docker image |
| Medium | Abandoned upstream (single author, no updates) | **Mitigated** — fork maintained locally |
| Low | Verbose stderr logging of full requests | **Fixed** — logs tool name only |
| Bug | `get_all_mids` fails (requires args) | **Fixed** |
| Bug | `get_candle_snapshot` coin vs symbol mismatch | **Fixed** |
| Bug | Malformed L2 book tool JSON schema | **Fixed** |

## Hardening Applied

### Container

- Multi-stage build (`node:22-alpine`)
- Non-root user (`nodeapp`, uid 1000)
- Read-only root filesystem at runtime
- tmpfs for `/tmp` (16 MB, noexec, nosuid)
- All Linux capabilities dropped
- `no-new-privileges` security option
- No secrets mounted

### Network

- Default: mainnet only (`https://api.hyperliquid.xyz`)
- Optional testnet via `HYPERLIQUID_API_URL=https://api.hyperliquid-testnet.xyz`
- URL allowlist enforced at startup — other hosts rejected

### Dependencies

Pinned in `package-lock.json`:

- `@modelcontextprotocol/sdk@1.29.0`
- `@nktkas/hyperliquid@0.16.0`
- `zod@3.24.2`

Run `npm audit` before each release and rebuild the Docker image if advisories affect runtime dependencies.

## Verification Steps

1. **Build image**
   ```bash
   docker build -t hyperliquid-mcp:0.0.1-vetted .
   ```

2. **Smoke test tools**
   ```bash
   ./scripts/smoke-test.sh
   ```

3. **Confirm egress** — server code only calls Hyperliquid via `@nktkas/hyperliquid` `HttpTransport`. No other HTTP clients or DNS lookups beyond Node fetch to the configured API URL.

4. **Cursor integration** — add `.cursor/mcp.json`, restart Cursor, verify green status in Settings → MCP.

## Residual Risks

- **Dependency vulnerabilities** in transitive npm packages (check `npm audit` output).
- **Hyperliquid API availability** — server depends on external API; no data integrity guarantees beyond what the API provides.
- **Docker escape** — standard container boundary; not a substitute for full VM isolation.
- **Prompt injection** — MCP tools return API data to the model; treat responses as untrusted input.

## Do Not

- Add private keys or trading capabilities without a separate security review.
- Run via `npx -y @mektigboy/server-hyperliquid` in production.
- Mount host filesystem or Docker socket into the container.

## Provenance

- Upstream: [mektigboy/server-hyperliquid](https://github.com/mektigboy/server-hyperliquid) (MIT)
- SDK: [@nktkas/hyperliquid](https://github.com/nktkas/hyperliquid) (MIT)
- Vetted fork: `mcp/hyperliquid/` in this repository
