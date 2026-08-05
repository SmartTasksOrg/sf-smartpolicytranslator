#!/usr/bin/env bash
# LangChain integration demo: checkout IAIso → translate the dataset through the
# LangChain tool (in-process) → (optionally) start a real IAIso BoundedExecution →
# validate every emitted policy against IAIso.
#   ./run_demo.sh                 # installs iaiso[langchain] and runs the full loop
#   SETUP_IAISO=0 ./run_demo.sh   # skip IAIso; tool still emits+validates (native)
set -euo pipefail
cd "$(dirname "$0")"
PKG="$(cd ../.. && pwd)"
DS="$PKG/examples/dataset"; OUT="$(pwd)/out"; mkdir -p "$OUT"
if [ "${SETUP_IAISO:-1}" = "1" ]; then WITH_LANGCHAIN=1 bash "$PKG/scripts/setup_iaiso.sh" || true; fi
export PYTHONPATH="$PKG/src"
echo "Translating dataset via the LangChain tool…"
python3 demo.py "$DS" "$OUT"
python3 "$PKG/scripts/validate_against_iaiso.py" "$OUT/*.policy.json"
