#!/usr/bin/env bash
# The React port is a UI component (SptPolicyViewer). There's no headless "dataset"
# run for a visual component, so this script (1) proves the underlying data path by
# running the Node port's dataset demo (React imports that same client), then (2)
# tells you how to view the component.
set -euo pipefail
cd "$(dirname "$0")"
PKG="$(cd ../.. && pwd)"
echo "React uses the Node client. Running the Node port's dataset demo as the data-path proof…"
bash "$PKG/ports/node/run_demo.sh"
cat <<'MSG'

To see the component itself:
  1) keep the service running:  (cd .. /.. && bash scripts/serve.sh)
  2) in a React app:  import { SptPolicyViewer } from "./src/SptPolicyViewer";
     render <SptPolicyViewer baseUrl="http://localhost:8000" /> and paste a regulation.
  Note: allow your web origin via CORS, or proxy /translate through your backend.
MSG
