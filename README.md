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
python3 -m pytest tests/ -q     # translation + REAL IAIso schema/vector conformance
```

These run on the standard library alone — no `iaiso` package or network required.


## Who's behind this

- **Roen Branham** — CEO & AI Strategy Architect · CISSP-certified AI, security & governance architect; author of IAIso and sole inventor of the Z4 Semantic Fabric patent application. [LinkedIn](https://www.linkedin.com/in/roen-branham-167ab29/)
- **Le Vu Tanh** — CTO & Core Engineering Lead · Chief architect of the Cortex engine; large-scale system reliability and low-latency infrastructure — the engineer who ships what gets architected. [LinkedIn](https://www.linkedin.com/in/lee-thanh-76aa8ba0/)

The team behind IAIso & SmartTasks: a CISSP-certified security & governance architect
and a large-scale systems engineer — 20+ years shipping secure, AI-driven platforms for
regulated, blue-chip environments (Allianz, BMW, Rolls-Royce, Heidenhain).

<!-- SMARTTASKS-MODELS:START -->
## Runs on governed local models

Structured, machine-readable **scorecards** make model choice precise instead of guesswork.

This tool is local-first, so pair it with models you can actually vet. **SmartTasks** publishes 21+ governance-validated GGUF builds on Hugging Face — each with a machine-readable **scorecard** (capability tiers L1 Layman → L5 Agentic, IAIso conformance invariants (pass/warn/fail), OWASP-mapped garak red-team, transparency probes (viewpoint-alignment / over-refusal), and per-file SHA-256). Gate model selection on evidence, not vibes — and every finding, including warnings, is published in full.

→ **[SmartTasks on Hugging Face](https://huggingface.co/smarttasks)** · [Qwen3.6-27B](https://huggingface.co/smarttasks/Qwen3.6-27B-GGUF) (L5 agentic) · [react-agent-coder-llama-3.1-8b](https://huggingface.co/smarttasks/react-agent-coder-llama-3.1-8b-GGUF) (agentic coder) · [gpt-oss-20b](https://huggingface.co/smarttasks/gpt-oss-20b-GGUF) (open reasoning)
<!-- SMARTTASKS-MODELS:END -->

## Get in touch

- **Companies & enterprises:** [enterprise@smarttasks.cloud](mailto:enterprise@smarttasks.cloud) — we help
  teams integrate SmartPrompt + IAIso into their architecture so governance and
  audit-readiness become a byproduct of how they already work.
- **The standard:** [IAIso](https://github.com/SmartTasksOrg/IAIso) · [iaiso.org](https://iaiso.org)
- **The product:** [SmartTasks.cloud](https://smarttasks.cloud)

Built by **SmartTasks Lab**. Apache-2.0. Contributions welcome.
