# SmartPolicyTranslator — Go port

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
cd ports/go
go mod tidy
```

## 3. Translate regulation → IAIso policy

```go
import spt "github.com/SmartTasksOrg/smartpolicytranslator-go"

c := spt.New("http://localhost:8000")
res, err := c.Translate("Personal data must be redacted.", false, "lmstudio")
// res["iaiso_policy"] is the IAIso policy document.
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

// enforce with the IAIso Go port (iaiso-go):
//   go get github.com/SmartTasksOrg/... (core/iaiso-go)
// pass the iaiso_policy map to iaiso-go's execution guard.

## Notes

Standard library only (`net/http`, `encoding/json`) — no third-party deps for the client.

## One-command end-to-end demo

```bash
cd ports/go
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
