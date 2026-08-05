# SmartPolicyTranslator — C++ port (libcurl, header-only)

Thin client that calls a running SmartPolicyTranslator service and returns the
**IAIso policy** it generates from regulation text. (SmartPolicyTranslator
*produces* the policy; IAIso *enforces* it — see the repo `INTEGRATION.md`.)

## 1. Start the service

```bash
# from the repo root:
cd smartpolicytranslator && bash scripts/run.sh     # → http://localhost:8000
```

## 2. Set up this port

Requires libcurl.
```bash
c++ -std=c++17 your_app.cpp -lcurl -o app
```

## 3. Translate regulation → IAIso policy

```cpp
#include "SptClient.hpp"
smarttasks::SptClient spt("http://localhost:8000");
std::string json = spt.translate("Personal data must be redacted.");
// json contains "iaiso_policy"; parse with nlohmann/json.
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

IAIso has no C++ port; enforce via a sidecar or the C ABI of an IAIso port.

## Notes

Header-only. Pair with nlohmann/json for parsing; the client returns the raw body.

## One-command end-to-end demo

```bash
cd ports/cpp
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
