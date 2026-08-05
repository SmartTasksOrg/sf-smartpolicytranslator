# SmartPolicyTranslator — Node / TypeScript port

Thin client that calls a running SmartPolicyTranslator service and returns the
**IAIso policy** it generates from regulation text. (SmartPolicyTranslator
*produces* the policy; IAIso *enforces* it — see the repo `INTEGRATION.md`.)

## 1. Start the service

```bash
# from the repo root:
cd smartpolicytranslator && bash scripts/run.sh     # → http://localhost:8000
```

## 2. Set up this port

```bash
cd ports/node
npm install
npm run build      # tsc → dist/
```

## 3. Translate regulation → IAIso policy

```ts
import SmartPolicyTranslator from "@smarttasks/smartpolicytranslator-client";

const spt = new SmartPolicyTranslator("http://localhost:8000");
const res = await spt.translate("Personal data must be redacted before model use.");
console.log(res.iaiso_policy.enforcement_mode, res.iaiso_policy.consent.required_scopes);
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

// enforce with the IAIso Node port:
//   npm install iaiso-node
// feed res.iaiso_policy into iaiso-node's BoundedExecution / callback handler.

## Notes

Peer dependency `iaiso-node` is only needed for enforcement, not for translation.

## One-command end-to-end demo

```bash
cd ports/node
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
