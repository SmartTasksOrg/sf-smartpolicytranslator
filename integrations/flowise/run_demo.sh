#!/usr/bin/env bash
# flowise integration demo. The flowise node/tool calls the SmartPolicyTranslator REST
# service; this script reproduces that exact HTTP call for every regulation in the
# dataset (so you can verify the data path headlessly), then validates the emitted
# policies against IAIso. Import the node into flowise to use it interactively.
#   ./run_demo.sh                 # checkout IAIso, serve, emulate node, validate
#   SETUP_IAISO=0 ./run_demo.sh   # skip IAIso (validate falls back to native)
set -euo pipefail
cd "$(dirname "$0")"
PKG="$(cd ../.. && pwd)"
DS="$PKG/examples/dataset"; OUT="$(pwd)/out"; mkdir -p "$OUT"
URL="${SPT_URL:-http://localhost:8000}"
if [ "${SETUP_IAISO:-1}" = "1" ]; then bash "$PKG/scripts/setup_iaiso.sh" || true; fi
bash "$PKG/scripts/serve.sh"
echo "Emulating the flowise node's POST /translate for each regulation…"
for f in "$DS"/*.txt; do
  n=$(basename "$f" .txt)
  payload=$(python3 -c "import json,sys;print(json.dumps({'uri':open(sys.argv[1],encoding='utf-8').read()}))" "$f")
  curl -s -X POST "$URL/translate" -H 'Content-Type: application/json' -d "$payload" > "$OUT/$n.policy.json"
  echo "  $n"
done
python3 "$PKG/scripts/validate_against_iaiso.py" "$OUT/*.policy.json"
bash "$PKG/scripts/stop.sh"
echo
echo "To use interactively: import flowise node (see flowise/README.md)."
