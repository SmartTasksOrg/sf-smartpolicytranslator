# SmartPolicyTranslator — Ruby port

Thin client that calls a running SmartPolicyTranslator service and returns the
**IAIso policy** it generates from regulation text. (SmartPolicyTranslator
*produces* the policy; IAIso *enforces* it — see the repo `INTEGRATION.md`.)

## 1. Start the service

```bash
# from the repo root:
cd sf-smartpolicytranslator && bash scripts/run.sh     # → http://localhost:8000
```

## 2. Set up this port

Ruby 3+ (stdlib `net/http`, `json`). No gems required.
```ruby
require_relative "spt_client"
```

## 3. Translate regulation → IAIso policy

```ruby
client = SmartTasks::SptClient.new("http://localhost:8000")
res = client.translate("Personal data must be redacted.")
puts res["iaiso_policy"]["enforcement_mode"]
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

Enforce with the IAIso Ruby port (`iaiso-ruby`, core/iaiso-ruby): pass `iaiso_policy` to its guard.

## Notes

Pure stdlib — no bundler needed for the client.

## One-command end-to-end demo

```bash
cd ports/ruby
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
