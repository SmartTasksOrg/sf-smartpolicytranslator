"""Thin remote Python client for SmartPolicyTranslator (stdlib only).

The engine itself is Python (../../src/sf_smartpolicytranslator) — import that for
in-process use. This client is for calling a *running* SPT service over HTTP,
matching the other language ports."""
from __future__ import annotations
import json
import urllib.request


class SptClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

    def translate(self, uri: str, use_llm: bool = False, provider: str = "lmstudio") -> dict:
        body = json.dumps({"uri": uri, "use_llm": use_llm, "provider": provider}).encode()
        req = urllib.request.Request(f"{self.base_url}/translate", data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
