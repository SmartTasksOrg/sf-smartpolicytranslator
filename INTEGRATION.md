# How SmartPolicyTranslator integrates with IAIso

A precise answer to "did you integrate the IAIso language/logic/policy — and how do
the two repos work together?"

## Short answer

Yes. The **IAIso policy language, its rules, and its validation logic are
integrated** — the policy spec is vendored into this repo and the translator emits
documents that conform to it (proven against IAIso's own official test vectors).
The IAIso **runtime SDK** (the pressure/consent/audit engine and middleware) is
**not copied in**; it is referenced as an optional dependency, because that code's
job is to *enforce* policy, which is IAIso's responsibility, not this repo's.

The relationship is: **SmartPolicyTranslator produces IAIso policy → IAIso validates
and enforces it.**

```
  regulation text
        │
        ▼
  SmartPolicyTranslator            (this repo — PRODUCE)
  ingest → parse → translate ──►  IAIso policy document (spec-conformant)
        │                                   │
        │  validate                         │  enforce
        ▼                                   ▼
  IAIso policy spec + validator      IAIso runtime SDK
  (VENDORED here)                    (iaiso package — REFERENCED)
  native + iaiso.policy._validate    BoundedExecution / consent / middleware
```

## What is VENDORED from IAIso (integrated into this repo)

Copied verbatim from `github.com/SmartTasksOrg/IAISO`, `IAIso-v5.0/core/spec/policy/`
(spec version **1.1**, repo `7272c11`), under `spec/iaiso/`:

| File | Source in IAIso repo | Purpose here |
|---|---|---|
| `policy.schema.json` | `core/spec/policy/policy.schema.json` | the real IAIso policy language (the schema we emit and validate against) |
| `vectors.json` | `core/spec/policy/vectors.json` | IAIso's official valid/invalid policy vectors |
| `POLICY_SPEC.md` | `core/spec/policy/README.md` | the normative policy specification |
| `IAISO_VERSION` | `core/spec/VERSION` | pinned spec version |

`src/smartpolicytranslator/iaiso_policy.py` implements the spec's **defaults and
validation logic** (version const, enforcement_mode enum, pressure ranges, the
`release_threshold > escalation_threshold` cross-field rule, the consent scope
grammar `^[a-z0-9_-]+(\.[a-z0-9_-]+)*$`) and **passes all of IAIso's vectors**
(`run_vectors()` → 22/22). That is the integrated policy logic — dependency-free.

`src/smartpolicytranslator/translator.py` is the **language conversion**: it maps
regulatory obligations onto IAIso policy fields (`enforcement_mode`, `consent`,
`pressure`, `metadata` provenance). `private/notes/MAPPING.md` documents each rule.

## What is REFERENCED (not copied) — the IAIso runtime SDK

`src/smartpolicytranslator/iaiso_sdk.py` is a **bridge** to the real `iaiso`
package (IAIso's `core/iaiso-python`). We deliberately do **not** vendor the SDK
source, so this repo stays small and always tracks IAIso's real code rather than a
stale copy. When `iaiso` is installed, the bridge does two things:

1. **Cross-validation** — `validate()` additionally runs the emitted policy through
   IAIso's **own** `iaiso.policy._validate`, so the document is blessed by IAIso's
   actual validator, not only our reimplementation. (Errors from that path are
   prefixed `iaiso-sdk:`.)
2. **Enforcement** — `integrations/langchain/spt_iaiso_langchain.py`'s
   `bounded_execution_from_regulation()` loads the emitted policy into IAIso's real
   `BoundedExecution` + `PressureConfig` and attaches `IAIsoCallbackHandler`, so a
   LangChain LLM/agent is governed by the translated policy.

Install the bridge:

```bash
pip install iaiso            # cross-validation through IAIso's own loader
pip install iaiso[langchain] # + enforcement via the LangChain middleware
```

With `iaiso` absent, both paths are skipped and the core still runs on the standard
library.

## Do the two repos need to be in the same tree?

No. They are separate repos that meet at the **policy document**:

- **Dev / CI of this repo** — nothing extra needed; the vendored spec + native
  validator are self-contained.
- **Cross-validation** — `pip install iaiso` in the same environment.
- **Runtime enforcement** — your application depends on `iaiso` (Python) or the
  matching `iaiso-<lang>` port (see `ports/README.md`); SmartPolicyTranslator can
  run as a service and your app calls it, or you generate policy at build time and
  ship the JSON into your IAIso deployment.

## Keeping the vendored spec in sync

The vendored files are pinned to IAIso spec **1.1**. To update: re-copy the four
files from the IAIso repo, run `python -m pytest tests/ -q` (the vector test will
fail loudly if our validator drifts from the new vectors), and bump `IAISO_VERSION`.
File hashes at vendor time are recorded in `spec/iaiso/PROVENANCE.txt`.
