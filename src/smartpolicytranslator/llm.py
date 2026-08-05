"""OpenAI-compatible LLM client for LM Studio / Ollama / llama.cpp (stdlib)."""
from __future__ import annotations
import json, os, urllib.request
PROVIDERS = {"lmstudio": "http://localhost:1234/v1",
             "ollama": "http://localhost:11434/v1",
             "llamacpp": "http://localhost:8080/v1"}


class LLM:
    def __init__(self, provider=None, base_url=None, model=None, api_key=""):
        provider = provider or os.environ.get("SPT_LLM_PROVIDER", "lmstudio")
        self.base_url = (base_url or os.environ.get("SPT_LLM_URL")
                         or PROVIDERS.get(provider, PROVIDERS["lmstudio"])).rstrip("/")
        self.model = model or os.environ.get("SPT_LLM_MODEL", "local-model")
        self.api_key = api_key or os.environ.get("SPT_LLM_API_KEY", "")

    def complete(self, prompt, system="", max_tokens=800, temperature=0.2):
        body = {"model": self.model, "temperature": temperature, "max_tokens": max_tokens,
                "stream": False, "messages": ([{"role": "system", "content": system}] if system else [])
                + [{"role": "user", "content": prompt}]}
        req = urllib.request.Request(f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json",
                     **({"Authorization": f"Bearer {self.api_key}"} if self.api_key else {})})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode("utf-8", "replace"))["choices"][0]["message"]["content"]

    def available(self):
        try:
            urllib.request.urlopen(urllib.request.Request(f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}), timeout=5).read()
            return True
        except Exception:
            return False
