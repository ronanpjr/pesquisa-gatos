#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${PORT:-8765}"
SERVER_PID=""
if python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 & then
  SERVER_PID=$!
  trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT
  sleep 0.3
fi

FLYER_URL="http://127.0.0.1:${PORT}/index.html" node scripts/diff.mjs
