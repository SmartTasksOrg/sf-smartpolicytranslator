"""Parse regulatory text into deontic clauses (MUST/SHOULD/MAY + subject/action/
condition). Rule-based and dependency-free; optional LLM parse via .llm."""
from __future__ import annotations
import re
from dataclasses import dataclass, field

_DEONTIC = [("MUST", r"\bmust\b|\bshall\b|\brequired to\b|\bmandatory\b|\bmust not\b"),
            ("SHOULD", r"\bshould\b|\brecommended\b"),
            ("MAY", r"\bmay\b|\bpermitted\b|\ballowed to\b|\bcan\b")]
_COND = re.compile(r"\b(if|when|where|unless|provided that)\b(.+)$", re.I)
_SENT = re.compile(r"(?<=[.;])\s+(?=[A-Z0-9(])")


@dataclass
class Clause:
    id: str
    text: str
    deontic: str
    subject: str = ""
    action: str = ""
    condition: str = ""
    obligations: list = field(default_factory=list)


def _deontic(t: str) -> str:
    low = t.lower()
    for label, pat in _DEONTIC:
        if re.search(pat, low):
            return label
    return "NONE"


def _split(text: str) -> list[str]:
    parts = re.split(r"\n\s*(?:\(?\d+[.)]|Article\s+\d+|Section\s+\d+|§\s*\d+)\s*", text)
    parts = [p for p in parts if p.strip()]
    if len(parts) <= 1:
        parts = _SENT.split(text)
    return [p.strip() for p in parts if len(p.strip()) > 20]


def parse_clauses(text: str, use_llm=False, llm=None) -> list[Clause]:
    if use_llm and llm is not None:
        try:
            return _parse_llm(text, llm)
        except Exception:
            pass
    out = []
    for i, seg in enumerate(_split(text), 1):
        m = _COND.search(seg)
        out.append(Clause(id=f"C{i:03d}", text=seg[:600], deontic=_deontic(seg),
                          subject=_subject(seg), action=_action(seg),
                          condition=(m.group(0).strip() if m else "")))
    return out


def _subject(seg):
    m = re.match(r"\s*(?:The\s+)?([A-Za-z][A-Za-z \-]{2,40}?)\s+(?:must|shall|should|may|is|are)\b", seg, re.I)
    return m.group(1).strip() if m else "system"


def _action(seg):
    m = re.search(r"\b(?:must|shall|should|may)\s+(?:not\s+|be\s+)?([a-z][a-z \-]{2,60})", seg, re.I)
    return m.group(1).strip() if m else ""


def _parse_llm(text, llm):
    prompt = ("Extract regulatory obligations. One JSON object per line with keys "
              "deontic (MUST/SHOULD/MAY), subject, action, condition:\n" + text[:6000])
    import json
    out = []
    for i, line in enumerate([l for l in llm.complete(prompt, max_tokens=1200).splitlines()
                              if l.strip().startswith("{")], 1):
        try:
            o = json.loads(line)
        except Exception:
            continue
        out.append(Clause(id=f"C{i:03d}", text=line[:600],
                          deontic=(o.get("deontic") or "NONE").upper(),
                          subject=o.get("subject", ""), action=o.get("action", ""),
                          condition=o.get("condition", "")))
    return out or parse_clauses(text, use_llm=False)
