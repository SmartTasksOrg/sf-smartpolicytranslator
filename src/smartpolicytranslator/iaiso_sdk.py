"""Bridge to the REAL IAIso Python SDK (github.com/SmartTasksOrg/IAISO,
core/iaiso-python, `pip install iaiso`).

SmartPolicyTranslator does not vendor IAIso's SDK source; it *integrates* with it
two ways:

  * VALIDATION — when `iaiso` is installed, `validate_with_iaiso()` runs the policy
    we emit through IAIso's own `iaiso.policy` loader/validator, so the document is
    blessed by IAIso's actual code, not only our spec-conformant reimplementation.
  * ENFORCEMENT — the LangChain integration (integrations/langchain) loads the
    emitted policy into IAIso's real `BoundedExecution`/`PressureConfig`/
    `IAIsoCallbackHandler`.

With `iaiso` absent, everything degrades to the vendored spec + native validator
(which passes all of IAIso's official policy vectors), so the core stays
dependency-free.
"""
from __future__ import annotations
import json
import os
import tempfile


def sdk_available() -> bool:
    try:
        import iaiso.policy  # noqa: F401
        return True
    except Exception:
        return False


def validate_with_iaiso(doc: dict) -> list[str]:
    """Validate `doc` with IAIso's OWN loader. Returns [] if valid, a list with a
    single error string if IAIso rejects it, or [] with a marker if the SDK isn't
    present (caller should check sdk_available())."""
    if not sdk_available():
        return []
    from iaiso.policy import _validate, PolicyError  # IAIso's real validator
    try:
        _validate(doc)
        return []
    except PolicyError as e:
        return [f"iaiso-sdk: {e}"]
    except Exception as e:  # pragma: no cover
        return [f"iaiso-sdk: {type(e).__name__}: {e}"]


def load_as_iaiso_policy(doc: dict):
    """Return IAIso's real `Policy` dataclass built from our emitted document.
    Requires `iaiso`. Useful to hand straight to the runtime."""
    from iaiso.policy import load_policy
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(doc, f)
        path = f.name
    try:
        return load_policy(path)
    finally:
        os.unlink(path)
