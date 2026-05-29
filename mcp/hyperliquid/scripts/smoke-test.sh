#!/usr/bin/env bash
set -euo pipefail

IMAGE="${IMAGE:-hyperliquid-mcp:0.0.1-vetted}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

run_mcp() {
  docker run -i --rm \
    --read-only \
    --tmpfs /tmp:rw,noexec,nosuid,size=16m \
    --cap-drop=ALL \
    --security-opt no-new-privileges \
    "$IMAGE" < /dev/stdin
}

handshake() {
  cat <<'EOF'
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke-test","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
EOF
}

call_method() {
  local id="$1"
  local method="$2"
  local params="$3"
  printf '{"jsonrpc":"2.0","id":%s,"method":"%s","params":%s}\n' "$id" "$method" "$params"
}

assert_ok() {
  local label="$1"
  local resp="$2"
  local pattern="$3"
  echo "$resp" | grep -q "$pattern" || {
    echo "$label failed:"
    echo "$resp"
    exit 1
  }
}

echo "==> Building image"
docker build -t "$IMAGE" "$ROOT_DIR"

echo "==> List tools"
LIST_RESP="$( (handshake; call_method 2 "tools/list" "{}") | run_mcp )"
assert_ok "tools/list" "$LIST_RESP" "get_all_mids"
assert_ok "tools/list" "$LIST_RESP" "get_candle_snapshot"
assert_ok "tools/list" "$LIST_RESP" "get_l2_book"

echo "==> Call get_all_mids"
MIDS_RESP="$( (handshake; call_method 3 "tools/call" '{"name":"get_all_mids","arguments":{}}') | run_mcp )"
assert_ok "get_all_mids" "$MIDS_RESP" '"result"'

echo "==> Call get_l2_book"
BOOK_RESP="$( (handshake; call_method 4 "tools/call" '{"name":"get_l2_book","arguments":{"symbol":"BTC"}}') | run_mcp )"
assert_ok "get_l2_book" "$BOOK_RESP" '"result"'

echo "==> Call get_candle_snapshot"
NOW=$(($(date +%s) * 1000))
START=$((NOW - 86400000))
CANDLE_PARAMS='{"name":"get_candle_snapshot","arguments":{"coin":"BTC","interval":"1h","startTime":'"$START"',"endTime":'"$NOW"'}}'
CANDLE_RESP="$( (handshake; call_method 5 "tools/call" "$CANDLE_PARAMS") | run_mcp )"
assert_ok "get_candle_snapshot" "$CANDLE_RESP" '"result"'

echo "==> All smoke tests passed"
