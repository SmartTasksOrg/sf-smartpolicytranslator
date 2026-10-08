"""FastAPI service. Run: uvicorn sf_smartpolicytranslator.api:app --port 8000"""
from __future__ import annotations
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .pipeline import translate_document
from .llm import LLM
from . import audit
from .iaiso_policy import load_schema, run_vectors

app = FastAPI(title="SmartPolicyTranslator", version="1.0.0",
              description="Translate regulation into REAL IAIso policy files.")


class Body(BaseModel):
    uri: str
    use_llm: bool = False
    provider: str = "lmstudio"
    model: str | None = None
    issuer: str = "sf-smartpolicytranslator"


@app.get("/health")
def health():
    return {"status": "ok", "framework": "IAIso", "vectors": run_vectors()}


@app.get("/iaiso/schema")
def schema():
    return load_schema()


@app.post("/translate")
def translate(b: Body):
    llm = LLM(provider=b.provider, model=b.model) if b.use_llm else None
    try:
        return translate_document(b.uri, use_llm=b.use_llm, llm=llm, issuer=b.issuer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/policies/{pid}")
def get_policy(pid: str):
    p = audit.get_policy(pid)
    if not p:
        raise HTTPException(status_code=404, detail="not found")
    return p


@app.get("/audit-trail")
def trail(limit: int = 100):
    return audit.audit_trail(limit)
