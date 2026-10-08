"""SmartPolicyTranslator × IAIso × LangChain.

Two things live here:

1. `make_spt_tool()` — a LangChain Tool that turns regulation text into a REAL
   IAIso policy document (the translator output).

2. `bounded_execution_from_regulation()` — the full loop a company wants: take
   regulation, translate it to an IAIso policy, and hand that policy to the REAL
   IAIso SDK's `BoundedExecution` + `IAIsoCallbackHandler` so the resulting
   LangChain LLM/agent is governed by the translated policy. This uses the actual
   `iaiso` package (github.com/SmartTasksOrg/IAISO, `pip install iaiso[langchain]`)
   — SmartPolicyTranslator produces the policy; IAIso enforces it.
"""
from __future__ import annotations
import json


def _translate(source: str) -> dict:
    from sf_smartpolicytranslator.pipeline import translate_document
    return translate_document(source, persist=False)


def make_spt_tool(base_url: str | None = None):
    """A LangChain Tool that emits an IAIso policy from regulation text."""
    desc = ("Translate natural-language regulation into a REAL IAIso policy file "
            "(version, enforcement_mode, consent scopes, pressure thresholds, "
            "provenance). Input: regulation text / path / URL.")

    def _run(source: str) -> str:
        if base_url:
            import urllib.request
            body = json.dumps({"uri": source}).encode()
            req = urllib.request.Request(f"{base_url.rstrip('/')}/translate", data=body,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read().decode("utf-8", "replace")
        return json.dumps(_translate(source)["iaiso_policy"])

    try:
        from langchain_core.tools import Tool
        return Tool(name="smart_policy_translator", description=desc, func=_run)
    except Exception:
        _run.__name__ = "smart_policy_translator"; _run.description = desc
        return _run


def iaiso_pressure_config_from_policy(policy: dict):
    """Build a real IAIso PressureConfig from a translated policy's pressure block.
    Requires the iaiso package: pip install iaiso

    IAIso's PressureConfig fields (v0.2.0): escalation_threshold, release_threshold,
    dissipation_per_step, dissipation_per_second, token_coefficient,
    tool_coefficient, depth_coefficient, post_release_lock. We pass only the keys
    IAIso accepts, so forward/backward-compatible policies stay safe."""
    from iaiso import PressureConfig
    import inspect
    p = policy.get("pressure", {}) or {}
    try:
        allowed = set(inspect.signature(PressureConfig).parameters)
    except (ValueError, TypeError):
        allowed = set(p)
    return PressureConfig(**{k: v for k, v in p.items() if k in allowed})


def bounded_execution_from_regulation(source: str):
    """Translate regulation -> IAIso policy -> a live IAIso BoundedExecution +
    LangChain callback handler. Returns (execution, handler, policy).

        exec, handler, policy = bounded_execution_from_regulation("reg.txt")
        llm = ChatOpenAI(callbacks=[handler])   # now governed by the policy

    Targets the real IAIso 0.2.x API:
        BoundedExecution.start(*, execution_id=None, config=None,
                               consent=None, audit_sink=None)
    i.e. the PressureConfig is passed as `config=` (keyword-only). A small
    signature probe keeps this resilient if IAIso renames the parameter again.
    """
    from iaiso import BoundedExecution
    from iaiso.middleware.langchain import IAIsoCallbackHandler

    policy = _translate(source)["iaiso_policy"]
    pressure = iaiso_pressure_config_from_policy(policy)

    # IAIso 0.2.x: start(*, config=PressureConfig). Older stubs used `pressure=`.
    # Pick whichever keyword this build's signature actually exposes.
    import inspect
    try:
        params = set(inspect.signature(BoundedExecution.start).parameters)
    except (ValueError, TypeError):
        params = {"config"}
    kw = "config" if "config" in params else ("pressure" if "pressure" in params else None)

    if kw is not None:
        execution = BoundedExecution.start(**{kw: pressure})
    else:                       # last-resort: no pressure kw at all
        execution = BoundedExecution.start()

    handler = IAIsoCallbackHandler(execution)
    return execution, handler, policy