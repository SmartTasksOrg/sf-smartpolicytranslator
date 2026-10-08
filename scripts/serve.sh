#!/usr/bin/env bash
# Start the SmartPolicyTranslator REST service in the background and wait until
# it's healthy. Writes the PID to .spt.pid. Install iaiso first (setup_iaiso.sh)
# if you want server-side validation to route through IAIso's own code.
set -euo pipefail
cd "$(dirname "$0")/.."                 # package dir
PORT="${SPT_PORT:-8000}"
if curl -sf "http://localhost:${PORT}/health" >/dev/null 2>&1; then
  echo "service already up on :${PORT}"; exit 0
fi
# install deps only if they're not already importable (respects venvs / managed envs)
if ! python3 -c "import fastapi, uvicorn" >/dev/null 2>&1; then
  pip install -q -r requirements.txt || pip install -q --break-system-packages -r requirements.txt || {
    echo "Could not install fastapi/uvicorn. Use a venv (bash scripts/run.sh) or install them, then retry." >&2
    exit 1; }
fi
export PYTHONPATH="$(pwd)/src"
nohup uvicorn sf_smartpolicytranslator.api:app --host 0.0.0.0 --port "$PORT" >/tmp/spt-service.log 2>&1 &
echo $! > .spt.pid
for i in $(seq 1 40); do
  curl -sf "http://localhost:${PORT}/health" >/dev/null 2>&1 && { echo "service up on :${PORT} (pid $(cat .spt.pid))"; exit 0; }
  sleep 0.5
done
echo "service failed to start; see /tmp/spt-service.log" >&2; exit 1
