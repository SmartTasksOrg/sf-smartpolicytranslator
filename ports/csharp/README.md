# SmartPolicyTranslator — C# port

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
cd ports/csharp
dotnet build
```
(.NET 8+)

## 3. Translate regulation → IAIso policy

```csharp
using SmartTasks.Spt;

var spt = new SptClient("http://localhost:8000");
var policy = await spt.TranslateAsync("Personal data must be redacted.");
Console.WriteLine(policy.GetProperty("iaiso_policy").GetProperty("enforcement_mode"));
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

Enforce with the IAIso C# port (`iaiso-csharp`, core/iaiso-csharp): pass the `iaiso_policy` element to its guard.

## Notes

Uses `System.Net.Http` + `System.Text.Json` — no external packages.

## One-command end-to-end demo

```bash
cd ports/csharp
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
