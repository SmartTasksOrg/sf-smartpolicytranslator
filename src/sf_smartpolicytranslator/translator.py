"""Map parsed regulatory clauses onto a REAL IAIso policy document.

The output validates against spec/iaiso/policy.schema.json. Regulatory intent is
expressed in IAIso's own language:

  * enforcement_mode  — 'strict' when any MUST / high-risk obligation appears.
  * consent.required_scopes — derived from data/access obligations (IAIso scope
    grammar ^[a-z0-9_-]+(\\.[a-z0-9_-]+)*$).
  * consent.default_ttl_seconds — tightened for high-risk regimes.
  * pressure — escalation/release thresholds tightened when human oversight or
    high-risk processing is mandated (bounded-execution posture).
  * metadata — full provenance: every policy choice back to its source clause.

This is the "policy-language conversion" from natural language into the IAIso
framework so it can be dropped into a company's IAIso deployment.
"""
from __future__ import annotations
from .iaiso_policy import apply_defaults, validate

# obligation detection: keyword -> canonical IAIso-facing obligation
_OBLIGATION_PATTERNS = {
    "redact_pii":        ["personal data", "pii", "redact", "sensitive", "anonymi", "gdpr", "privacy"],
    "protect_secrets":   ["secret", "credential", "api key", "token"],
    "prompt_scan":       ["prompt", "injection", "jailbreak", "input validation"],
    "verify_output":     ["hallucinat", "accuracy", "verify", "verified", "fact-check", "grounding"],
    "audit_log":         ["audit", "log", "record", "provenance", "traceab", "receipt", "attestation"],
    "enforce_access":    ["access", "authoriz", "gateway", "route", "allowlist", "rbac", "role-based"],
    "human_review":      ["human review", "human oversight", "human-in-the-loop", "override", "appeal"],
    "risk_assessment":   ["risk assessment", "high-risk", "high risk", "impact assessment"],
    "disclose_ai_use":   ["disclose", "inform", "transparency", "notify"],
    "consent_check":     ["consent", "opt-in", "opt in", "permission"],
    "data_minimization": ["minim", "purpose limitation", "necessary", "proportional"],
    "rate_limit":        ["rate limit", "throttle", "quota", "resource limit"],
}
_HIGH_RISK = {"redact_pii", "protect_secrets", "prompt_scan", "verify_output",
              "enforce_access", "risk_assessment"}

# obligation -> IAIso consent scopes (dotted, lowercase; matches scope grammar)
_SCOPES = {
    "redact_pii":        ["data.pii.read", "data.personal.process"],
    "protect_secrets":   ["secrets.read"],
    "prompt_scan":       ["model.prompt"],
    "verify_output":     ["model.output.read"],
    "enforce_access":    ["model.invoke", "tool.call"],
    "human_review":      ["decision.override"],
    "consent_check":     ["data.personal.process"],
    "data_minimization": ["data.personal.process"],
}


def _obligations_for(text: str) -> list[str]:
    low = text.lower()
    return [ob for ob, kws in _OBLIGATION_PATTERNS.items() if any(k in low for k in kws)]


def translate_to_iaiso_policy(clauses, *, issuer="sf-smartpolicytranslator",
                              source="") -> dict:
    provenance, all_obl, scopes = [], set(), set()
    for c in clauses:
        obl = _obligations_for(f"{c.subject} {c.action} {c.text}")
        c.obligations = obl
        for o in obl:
            all_obl.add((o, c.deontic))
            scopes.update(_SCOPES.get(o, []))
        if obl:
            provenance.append({"clause_id": c.id, "deontic": c.deontic,
                               "text": c.text[:240], "obligations": obl})

    obl_names = {o for o, _ in all_obl}
    has_must = any(d == "MUST" for _, d in all_obl)
    high_risk = bool(obl_names & _HIGH_RISK)
    strict = has_must or high_risk

    # pressure posture: tighten when oversight / high-risk is mandated
    if high_risk or "human_review" in obl_names:
        pressure = {"escalation_threshold": 0.7, "release_threshold": 0.9,
                    "post_release_lock": True}
    else:
        pressure = {"escalation_threshold": 0.85, "release_threshold": 0.95}

    consent = {"issuer": issuer,
               "default_ttl_seconds": 900.0 if strict else 3600.0,
               "required_scopes": sorted(scopes),
               "allowed_algorithms": ["HS256", "RS256"]}

    policy = {
        "version": "1",
        "enforcement_mode": "strict" if strict else "permissive",
        "pressure": pressure,
        "consent": consent,
        "metadata": {
            "generated_by": "SmartPolicyTranslator",
            "framework": "IAIso",
            "source": source[:200],
            "derived_obligations": sorted(obl_names),
            "high_risk": high_risk,
            "provenance": provenance,
            "coverage": {"clauses_total": len(clauses),
                         "clauses_mapped": len(provenance)},
            "note": ("enforcement_mode=strict because a MUST/high-risk obligation "
                     "was present; fail closed." if strict else
                     "no MUST/high-risk obligation detected; permissive posture."),
        },
    }
    return policy


def translate(clauses, *, issuer="sf-smartpolicytranslator", source="") -> dict:
    """Return {policy, valid, errors, normalized}. `policy` is the emitted IAIso
    document; `normalized` has spec defaults applied."""
    policy = translate_to_iaiso_policy(clauses, issuer=issuer, source=source)
    errors = validate(policy)
    return {"policy": policy, "valid": not errors, "errors": errors,
            "normalized": apply_defaults(policy)}
