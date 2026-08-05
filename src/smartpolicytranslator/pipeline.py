"""End-to-end: ingest -> parse -> translate to IAIso policy -> validate -> audit."""
from __future__ import annotations
import hashlib, time
from .ingestion import extract_text
from .parser import parse_clauses
from .translator import translate
from . import audit


def translate_document(source, *, use_llm=False, llm=None, issuer="smartpolicytranslator",
                       persist=True) -> dict:
    text = extract_text(source)
    clauses = parse_clauses(text, use_llm=use_llm, llm=llm)
    result = translate(clauses, issuer=issuer, source=source)
    pid = "pol_" + hashlib.sha1((source + str(time.time())).encode()).hexdigest()[:12]
    out = {"policy_id": pid, "source": source[:200], "framework": "IAIso",
           "clauses": [c.__dict__ for c in clauses],
           "iaiso_policy": result["policy"], "valid": result["valid"],
           "validation_errors": result["errors"], "normalized": result["normalized"]}
    if persist:
        audit.save_policy(pid, source, result["policy"], result["valid"])
    return out
