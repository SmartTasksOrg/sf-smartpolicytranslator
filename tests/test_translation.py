"""Public tests — translation + REAL IAIso schema conformance (stdlib only)."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
os.environ["SPT_SQLITE_PATH"] = os.path.join(os.path.dirname(__file__), "_t.db")

from sf_smartpolicytranslator.pipeline import translate_document
from sf_smartpolicytranslator.parser import parse_clauses
from sf_smartpolicytranslator import iaiso_policy

SAMPLE = os.path.join(ROOT, "examples", "sample_regulation.txt")


def test_iaiso_official_vectors_pass():
    r = iaiso_policy.run_vectors()
    assert r["failed"] == [] and r["passed"] == r["total"] and r["total"] > 0


def test_translation_emits_valid_iaiso_policy():
    out = translate_document(SAMPLE, persist=False)
    pol = out["iaiso_policy"]
    assert out["valid"] is True and iaiso_policy.validate(pol) == []
    assert pol["version"] == "1"
    assert pol["enforcement_mode"] == "strict"          # MUST + high-risk present
    assert pol["consent"]["required_scopes"]             # derived scopes
    # scopes obey the IAIso scope grammar
    import re
    rx = re.compile(r"^[a-z0-9_-]+(\.[a-z0-9_-]+)*$")
    assert all(rx.match(s) for s in pol["consent"]["required_scopes"])
    # pressure tightened for high-risk and release_threshold > escalation_threshold
    p = pol["pressure"]
    assert p["release_threshold"] > p["escalation_threshold"]
    # provenance links policy back to clauses
    assert pol["metadata"]["provenance"] and pol["metadata"]["coverage"]["clauses_mapped"] > 0


def test_permissive_when_no_must():
    out = translate_document("Providers may log requests for analytics.", persist=False)
    assert out["iaiso_policy"]["enforcement_mode"] == "permissive"


def test_scopes_derive_from_obligations():
    out = translate_document("Personal data must be redacted before model use.", persist=False)
    assert "data.pii.read" in out["iaiso_policy"]["consent"]["required_scopes"]
