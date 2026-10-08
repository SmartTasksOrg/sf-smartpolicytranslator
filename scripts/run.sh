#!/usr/bin/env bash
set -euo pipefail; cd "$(dirname "$0")/.."
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
pip install -q -r requirements.txt
export PYTHONPATH="$(pwd)/src"
echo "SmartPolicyTranslator → http://localhost:8000/docs"
uvicorn sf_smartpolicytranslator.api:app --reload --port 8000
