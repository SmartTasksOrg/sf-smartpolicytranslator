# SmartPolicyTranslator — Python port (remote client)

Thin client that calls a running SmartPolicyTranslator service and returns the
**IAIso policy** it generates from regulation text. (SmartPolicyTranslator
*produces* the policy; IAIso *enforces* it — see the repo `INTEGRATION.md`.)

## 1. Start the service

```bash
# from the repo root:
cd smartpolicytranslator && bash scripts/run.sh     # → http://localhost:8000
```

## 2. Set up this port

No install needed — stdlib only. For in-process use, import the engine from `../../src` instead.

## 3. Translate regulation → IAIso policy

```python
from spt_client import SptClient

spt = SptClient("http://localhost:8000")
res = spt.translate("Personal data must be redacted before model use.")
policy = res["iaiso_policy"]           # a REAL IAIso policy document
print(policy["enforcement_mode"], policy["consent"]["required_scopes"])
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

# enforce with the real IAIso SDK:
#   pip install iaiso
from smartpolicytranslator.iaiso_sdk import load_as_iaiso_policy
iaiso_policy = load_as_iaiso_policy(policy)   # IAIso's real Policy dataclass

## Notes

In-process (no service) is often simpler in Python: `from smartpolicytranslator.pipeline import translate_document`.

## One-command end-to-end demo

```bash
cd ports/python
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
