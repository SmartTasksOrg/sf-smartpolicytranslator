#!/usr/bin/env bash
# Check out IAIso and install the REAL iaiso SDK so the app can validate/enforce
# against IAIso's own code. Idempotent.
#
#   ./setup_iaiso.sh                    # clone into ./.iaiso and pip install -e it
#   WITH_LANGCHAIN=1 ./setup_iaiso.sh   # also install iaiso[langchain]
#   IAISO_REPO=<url> ./setup_iaiso.sh   # override the repo URL
set -euo pipefail
cd "$(dirname "$0")/.."                 # smartpolicytranslator/ package dir
REPO="${IAISO_REPO:-https://github.com/SmartTasksOrg/IAISO.git}"
DEST="${IAISO_DIR:-.iaiso}"
EXTRA=""; [ "${WITH_LANGCHAIN:-0}" = "1" ] && EXTRA="[langchain]"

if [ ! -d "$DEST/.git" ]; then
  echo "Cloning IAIso → $DEST"
  git clone --depth 1 "$REPO" "$DEST"
else
  echo "IAIso already checked out at $DEST"
fi

PKG="$DEST/IAIso-v5.0/core/iaiso-python"
[ -d "$PKG" ] || PKG="$DEST"            # fall back if layout differs
echo "Installing iaiso from $PKG"
pip install -e "${PKG}${EXTRA}" || pip install "iaiso${EXTRA}"
python3 -c "import iaiso, iaiso.policy; print('IAIso ready:', getattr(iaiso,'__version__','?'))"
