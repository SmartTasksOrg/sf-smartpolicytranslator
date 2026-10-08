#!/usr/bin/env bash
# End-to-end demo for the go port:
#   check out IAIso  →  serve SmartPolicyTranslator  →  translate the test dataset
#   through this port  →  validate every emitted policy against IAIso.
#
#   ./run_demo.sh                 # full run (clones IAIso, installs the SDK)
#   SETUP_IAISO=0 ./run_demo.sh   # skip IAIso checkout (validate falls back to native)
set -euo pipefail
cd "$(dirname "$0")"
PKG="$(cd ../.. && pwd)"                       # sf-smartpolicytranslator/ package dir
DS="$PKG/examples/dataset"
OUT="$(pwd)/out"; mkdir -p "$OUT"

# 1) check out IAIso + install the real SDK (so the service validates via IAIso)
if [ "${SETUP_IAISO:-1}" = "1" ]; then bash "$PKG/scripts/setup_iaiso.sh" || true; fi

# 2) start the SmartPolicyTranslator service
bash "$PKG/scripts/serve.sh"

# 3) build this port
go mod tidy

# 4) run the go client over the dataset  →  writes out/*.policy.json
echo "Translating dataset via the go port…"
go run ./demo "$DS" "$OUT"

# 5) validate the emitted policies against IAIso's own validator
python3 "$PKG/scripts/validate_against_iaiso.py" "$OUT/*.policy.json"

# 6) stop the service
bash "$PKG/scripts/stop.sh"
