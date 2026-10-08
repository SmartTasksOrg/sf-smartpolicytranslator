# SmartPolicyTranslator — Swift port

Thin client that calls a running SmartPolicyTranslator service and returns the
**IAIso policy** it generates from regulation text. (SmartPolicyTranslator
*produces* the policy; IAIso *enforces* it — see the repo `INTEGRATION.md`.)

## 1. Start the service

```bash
# from the repo root:
cd sf-smartpolicytranslator && bash scripts/run.sh     # → http://localhost:8000
```

## 2. Set up this port

```bash
cd ports/swift
swift build
```
(Swift 5.9+; add as a SwiftPM dependency.)

## 3. Translate regulation → IAIso policy

```swift
import SPTClient

let spt = SPTClient(baseURL: "http://localhost:8000")
let res = try await spt.translate(uri: "Personal data must be redacted.")
if let p = res["iaiso_policy"] as? [String: Any] { print(p["enforcement_mode"] ?? "") }
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

Enforce with the IAIso Swift port (`iaiso-swift`, core/iaiso-swift): pass `iaiso_policy` to its guard.

## Notes

Uses `URLSession` async/await. On Linux, ensure FoundationNetworking is available.

## One-command end-to-end demo

```bash
cd ports/swift
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
