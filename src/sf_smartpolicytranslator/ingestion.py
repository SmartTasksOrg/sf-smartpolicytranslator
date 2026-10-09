"""Extract clean text from raw text, a file (.txt/.md, optional PDF/DOCX), or URL."""
from __future__ import annotations
import os, re, urllib.request


def extract_text(source: str) -> str:
    s = source or ""
    if s.startswith(("http://", "https://")):
        try:
            req = urllib.request.Request(s, headers={"User-Agent": "SmartPolicyTranslator/1.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return _clean(re.sub(r"<[^>]+>", " ", r.read().decode("utf-8", "replace")))
        except Exception as e:
            return f"[ingestion error for {s}: {e}]"
    if os.path.exists(s):
        ext = os.path.splitext(s)[1].lower()
        if ext == ".pdf":
            try:
                import fitz
                return _clean("\n".join(pg.get_text() for pg in fitz.open(s)))
            except Exception as e:
                return f"[PDF needs pymupdf: {e}]"
        if ext == ".docx":
            try:
                import docx
                return _clean("\n".join(p.text for p in docx.Document(s).paragraphs))
            except Exception as e:
                return f"[DOCX needs python-docx: {e}]"
        with open(s, encoding="utf-8", errors="replace") as f:
            return _clean(f.read())
    return _clean(s)


def _clean(t: str) -> str:
    return re.sub(r"[ \t]+", " ", re.sub(r"\r\n?", "\n", t)).strip()
