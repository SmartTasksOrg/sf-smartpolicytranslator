# SmartPolicyTranslator — C port (libcurl)

Thin client that calls a running SmartPolicyTranslator service and returns the
**IAIso policy** it generates from regulation text. (SmartPolicyTranslator
*produces* the policy; IAIso *enforces* it — see the repo `INTEGRATION.md`.)

## 1. Start the service

```bash
# from the repo root:
cd smartpolicytranslator && bash scripts/run.sh     # → http://localhost:8000
```

## 2. Set up this port

Requires libcurl dev headers (`libcurl4-openssl-dev` / `libcurl-devel`).
```bash
cc ports/c/spt_client.c -lcurl -DSPT_DEMO -o spt_demo
./spt_demo "Personal data must be redacted."
```

## 3. Translate regulation → IAIso policy

```c
#include "spt_client.h"
char *json = spt_translate(NULL, "Personal data must be redacted.", 0, "lmstudio");
/* json contains "iaiso_policy"; parse with cJSON/jansson. free(json) when done. */
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

IAIso has no C port; enforce via a sidecar (call the Python/Node IAIso SDK) or through the C ABI of an IAIso port.

## Notes

Request-side JSON escaping is minimal (quotes/backslashes). Use a JSON library (cJSON, jansson) to parse the response.

## One-command end-to-end demo

```bash
cd ports/c
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
