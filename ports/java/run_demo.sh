#!/usr/bin/env bash
# End-to-end demo for the Java port: checkout IAIso → serve → translate dataset → validate vs IAIso.
#   ./run_demo.sh   (SETUP_IAISO=0 to skip the IAIso checkout)
set -euo pipefail
cd "$(dirname "$0")"
PKG="$(cd ../.. && pwd)"
DS="$PKG/examples/dataset"; OUT="$(pwd)/out"; mkdir -p "$OUT/classes"
if [ "${SETUP_IAISO:-1}" = "1" ]; then bash "$PKG/scripts/setup_iaiso.sh" || true; fi
bash "$PKG/scripts/serve.sh"
javac src/main/java/cloud/smarttasks/spt/SptClient.java Demo.java -d "$OUT/classes"
echo "Translating dataset via the Java port…"
java -cp "$OUT/classes" Demo "$DS" "$OUT"
python3 "$PKG/scripts/validate_against_iaiso.py" "$OUT/*.policy.json"
bash "$PKG/scripts/stop.sh"
