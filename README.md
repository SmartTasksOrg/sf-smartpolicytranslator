# SmartPolicyTranslator

**Translate natural-language regulation into REAL, schema-conformant [IAIso](https://github.com/SmartTasksOrg/IAIso) policy files — and wire them straight into your architecture.**

Regulation is prose. IAIso deployments run on *policy files*. SmartPolicyTranslator
closes that gap: it ingests regulatory text, parses each clause's deontic force
(MUST / SHOULD / MAY), and emits a valid **IAIso v1 policy document** — with full
provenance from every policy choice back to its source clause.

```
 ingest ─▶ parse (deontic) ─▶ translate ─▶ validate ─▶ audit
  text/PDF/URL   MUST/SHOULD/MAY   → IAIso policy   vs real schema   provenance
```

This is not an invented format. The IAIso policy schema, normative spec, and
official test vectors are vendored under `spec/iaiso/` directly from
[github.com/SmartTasksOrg/IAISO](https://github.com/SmartTasksOrg/IAISO)
(`IAIso-v5.0`). Every emitted policy is validated against them, and the loader
passes **all of IAIso's own policy test vectors**.

## Ready to run

The core needs **zero third-party packages** (stdlib only):

```bash
export PYTHONPATH=src
python3 -m smartpolicytranslator.cli examples/sample_regulation.txt
# → a valid IAIso policy: version "1", enforcement_mode, consent scopes, pressure…

# LLM-assisted parsing (LM Studio / Ollama / llama.cpp):
python3 -m smartpolicytranslator.cli --llm --provider lmstudio examples/sample_regulation.txt

# REST service:
bash scripts/run.sh          # → http://localhost:8000/docs   (or: docker build/run)
```

## What the translation produces

A regulation with MUST/high-risk obligations yields a **strict, fail-closed** IAIso
policy: `enforcement_mode: "strict"`, `consent.required_scopes` derived from the
data/access obligations (in IAIso's scope grammar, e.g. `data.pii.read`,
`model.invoke`, `decision.override`), a tightened `pressure` posture
(`escalation_threshold` lowered, `post_release_lock` on), a shorter consent TTL,
and a `metadata.provenance[]` trail mapping each choice to its clause. A permissive
regulation yields a permissive policy. See `private/notes/MAPPING.md`.

## Integrations & ports

SmartPolicyTranslator **produces** IAIso policy; IAIso **enforces** it.

- **LangChain (+ real IAIso SDK)** — `integrations/langchain/`:
  `bounded_execution_from_regulation()` translates regulation and loads the policy
  into IAIso's real `BoundedExecution` + `IAIsoCallbackHandler`, so a LangChain LLM
  is governed by the translated policy (`pip install iaiso[langchain]`).
- **n8n / Flowise** — `integrations/n8n/`, `integrations/flowise/`.
- **Language ports** — `ports/{node,react,java,go,php,ruby,rust,csharp,swift,c,cpp}`,
  mirroring every language IAIso itself ships (plus React and C/C++) so a policy can
  be generated and enforced in the language of your IAIso deployment. See
  `ports/README.md` for the port↔`iaiso-*` map.
- **Local LLMs** — `src/smartpolicytranslator/llm.py`: one OpenAI-compatible client
  for LM Studio, Ollama, and llama.cpp.

## Tests

```bash
python3 -m pytest tests/ -q                 # public: translation + IAIso vector conformance
python3 -m pytest ../private/tests/ -q      # private: core + LM Studio LLM framework
```

The private suite includes an LM Studio LLM test framework (offline-deterministic
always-on; a live tier gated behind `SPT_LLM_LIVE=1` that self-skips if the box is
unreachable) — the same pattern the other Smart-family repos use.

## License

Apache-2.0. IAIso: https://github.com/SmartTasksOrg/IAIso
