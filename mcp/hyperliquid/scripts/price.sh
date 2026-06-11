#!/usr/bin/env bash
set -euo pipefail

SYMBOL="${1:-}"
if [ -z "$SYMBOL" ]; then
  echo "Usage: $0 SYMBOL" >&2
  echo "Example: $0 BTC" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
IMAGE="${IMAGE:-hyperliquid-mcp:0.0.1-vetted}"

run_mcp() {
  if docker info >/dev/null 2>&1 && docker image inspect "$IMAGE" >/dev/null 2>&1; then
    docker run -i --rm \
      --read-only \
      --tmpfs /tmp:rw,noexec,nosuid,size=16m \
      --cap-drop=ALL \
      --security-opt no-new-privileges \
      "$IMAGE" < /dev/stdin
  else
    node "$ROOT_DIR/dist/index.js" < /dev/stdin
  fi
}

PAYLOAD=$(cat <<EOF
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"price-cli","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_mid","arguments":{"symbol":"$SYMBOL"}}}
EOF
)

RESP="$(printf '%s\n' "$PAYLOAD" | run_mcp 2>/dev/null)"

python3 - "$RESP" <<'PY'
import json, sys
resp = sys.argv[1]
for line in resp.splitlines():
    obj = json.loads(line)
    if obj.get("id") != 2:
        continue
    result = obj.get("result", {})
    text = result.get("content", [{}])[0].get("text", "")
    if result.get("isError"):
        print(text.replace("Error: ", ""))
        sys.exit(1)
    data = json.loads(text)
    print(f"{data['symbol']} mid: {data['mid']}")
    sys.exit(0)
print("No MCP response", file=sys.stderr)
sys.exit(1)
PY
