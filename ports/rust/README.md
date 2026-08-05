# SmartPolicyTranslator — Rust port

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
cd ports/rust
cargo build
```

## 3. Translate regulation → IAIso policy

```rust
use smartpolicytranslator_client::SptClient;

let c = SptClient::new("http://localhost:8000");
let v = c.translate("Personal data must be redacted.", false, "lmstudio")?;
println!("{}", v["iaiso_policy"]["enforcement_mode"]);
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

// enforce with the IAIso Rust port (iaiso-rust, core/iaiso-rust):
// add it to Cargo.toml and pass the iaiso_policy value to its execution guard.

## Notes

Uses `ureq` (blocking) + `serde_json`. For async, swap in `reqwest` — the shape is identical.

## One-command end-to-end demo

```bash
cd ports/rust
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
