#!/usr/bin/env bash
# Start llama-server for A01. Not run in the collection round.
set -euo pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
KIT=$(cd "$HERE/../.." && pwd)
# shellcheck disable=SC1091
set -a
[ -f "$HERE/config/env.local" ] && . "$HERE/config/env.local" || . "$HERE/config/env.example"
set +a
BIN="${LLAMA_SERVER_BIN:-}"
if [ ! -x "$BIN" ]; then
  # official archive extracts to a bin/ directory; search without executing the server here
  CAND=$(find "$KIT/runtimes/linux_x86_64/llama_cpp" -maxdepth 3 -type f -name 'llama-server' 2>/dev/null | head -n1 || true)
  BIN=${CAND:-$BIN}
fi
GGUF="${LLAMA_GGUF:-$KIT/models/cpu_baseline/qwen2.5-1.5b-instruct-q4_k_m.gguf}"
URLF="${GGUF}.url.txt"
echo "binary=$BIN"
echo "gguf=$GGUF"
if [ ! -f "$GGUF" ]; then
  echo "missing GGUF (weights are URL-only; see $URLF)" >&2
  [ -f "$URLF" ] && cat "$URLF" >&2
  exit 1
fi
if [ ! -x "$BIN" ]; then echo "missing llama-server binary (extract the runtime tar first)" >&2; exit 1; fi
exec "$BIN" -m "$GGUF" --port 8080 --host 127.0.0.1 -c "${LLAMA_CTX:-4096}" -t "${LLAMA_THREADS:-4}" --alias "${AGENT_LLM_MODEL:-qwen2.5-1.5b-instruct}"
