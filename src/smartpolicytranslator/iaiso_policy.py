"""Load, default, and validate REAL IAIso policy documents.

The schema + normative spec + official test vectors are vendored under
../spec/iaiso/ straight from github.com/SmartTasksOrg/IAISO (IAIso-v5.0). This
module applies the spec's defaults and validates a document against the real
schema — natively (zero deps) and, if `jsonschema` is installed, against the
JSON Schema itself. `run_vectors()` proves conformance against IAIso's own
valid/invalid vectors.
"""
from __future__ import annotations
import json, os

_SPEC = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "spec", "iaiso")
SCHEMA_PATH = os.path.join(_SPEC, "policy.schema.json")
VECTORS_PATH = os.path.join(_SPEC, "vectors.json")

# defaults straight from spec/policy/README.md §3-5
PRESSURE_DEFAULTS = {
    "token_coefficient": 0.015, "tool_coefficient": 0.08, "depth_coefficient": 0.05,
    "dissipation_per_step": 0.02, "dissipation_per_second": 0.0,
    "escalation_threshold": 0.85, "release_threshold": 0.95, "post_release_lock": True,
}
CONSENT_DEFAULTS = {
    "issuer": None, "default_ttl_seconds": 3600.0,
    "required_scopes": [], "allowed_algorithms": ["HS256", "RS256"],
}
_SCOPE_RE = __import__("re").compile(r"^[a-z0-9_-]+(\.[a-z0-9_-]+)*$")


class PolicyError(ValueError):
    pass


def load_schema() -> dict:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def validate(doc: dict) -> list[str]:
    """Return a list of error-path strings ([] means valid). Native validator
    covering the normative constraints; also runs jsonschema if available."""
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["/: document must be a JSON object (mapping)"]
    # version REQUIRED and const "1"
    if "version" not in doc:
        errors.append("/version: required")
    elif doc["version"] != "1":
        errors.append('/version: must be exactly "1"')
    # enforcement_mode enum
    em = doc.get("enforcement_mode", "permissive")
    if em not in ("permissive", "strict"):
        errors.append("/enforcement_mode: must be 'permissive' or 'strict'")
    # pressure numeric ranges + cross-field
    p = doc.get("pressure", {})
    if isinstance(p, dict):
        for k in ("token_coefficient", "tool_coefficient", "depth_coefficient",
                  "dissipation_per_step", "dissipation_per_second"):
            if k in p and (not _num(p[k]) or p[k] < 0):
                errors.append(f"/pressure/{k}: must be a number >= 0")
        for k in ("escalation_threshold", "release_threshold"):
            if k in p and (not _num(p[k]) or not 0 <= p[k] <= 1):
                errors.append(f"/pressure/{k}: must be in [0, 1]")
        if _num(p.get("escalation_threshold")) and _num(p.get("release_threshold")):
            if not p["release_threshold"] > p["escalation_threshold"]:
                errors.append("/pressure/release_threshold: must exceed escalation_threshold")
    # consent
    c = doc.get("consent", {})
    if isinstance(c, dict):
        for s in c.get("required_scopes", []) or []:
            if not _SCOPE_RE.match(str(s)):
                errors.append(f"/consent/required_scopes: '{s}' violates scope pattern")
        if "default_ttl_seconds" in c and (not _num(c["default_ttl_seconds"]) or c["default_ttl_seconds"] < 0):
            errors.append("/consent/default_ttl_seconds: must be a number >= 0")
    # coordinator aggregator enum
    co = doc.get("coordinator", {})
    if isinstance(co, dict) and "aggregator" in co:
        if co["aggregator"] not in ("sum", "mean", "max", "weighted_sum"):
            errors.append("/coordinator/aggregator: invalid enum")
    # cross-validate with the REAL IAIso SDK when it is installed
    try:
        from .iaiso_sdk import validate_with_iaiso, sdk_available
        if sdk_available():
            errors.extend(validate_with_iaiso(doc))
    except Exception:
        pass
    # optional strict validation via jsonschema
    try:
        import jsonschema
        try:
            jsonschema.validate(doc, load_schema())
        except jsonschema.ValidationError as e:
            path = "/" + "/".join(str(x) for x in e.absolute_path)
            errors.append(f"{path}: {e.message}")
    except Exception:
        pass
    return sorted(set(errors))


def apply_defaults(doc: dict) -> dict:
    """Return a normalized policy with spec defaults filled in (does not mutate)."""
    out = dict(doc)
    out["pressure"] = {**PRESSURE_DEFAULTS, **(doc.get("pressure") or {})}
    out["consent"] = {**CONSENT_DEFAULTS, **(doc.get("consent") or {})}
    out.setdefault("enforcement_mode", "permissive")
    out.setdefault("metadata", {})
    return out


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def run_vectors() -> dict:
    """Conformance against IAIso's own vectors: valid vectors must pass, invalid
    must fail with the expected error-path substring."""
    with open(VECTORS_PATH, encoding="utf-8") as f:
        vec = json.load(f)
    passed, failed = 0, []
    for v in vec.get("valid", []):
        errs = validate(v["document"])
        if errs:
            failed.append(f"valid '{v['name']}' rejected: {errs}")
        else:
            passed += 1
    for v in vec.get("invalid", []):
        errs = validate(v["document"])
        want = v.get("error_path") or v.get("expected_error") or ""
        if errs and (not want or any(want in e for e in errs)):
            passed += 1
        else:
            failed.append(f"invalid '{v.get('name')}' not caught (want '{want}', got {errs})")
    return {"passed": passed, "failed": failed,
            "total": len(vec.get("valid", [])) + len(vec.get("invalid", []))}
