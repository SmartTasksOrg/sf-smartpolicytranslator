# SmartPolicyTranslator — Java port

Thin client that calls a running SmartPolicyTranslator service and returns the
**IAIso policy** it generates from regulation text. (SmartPolicyTranslator
*produces* the policy; IAIso *enforces* it — see the repo `INTEGRATION.md`.)

## 1. Start the service

```bash
# from the repo root:
cd smartpolicytranslator && bash scripts/run.sh     # → http://localhost:8000
```

## 2. Set up this port

Java 11+ (uses `java.net.http`). No extra dependencies. Drop `SptClient.java` into your project under `cloud.smarttasks.spt`, or build a jar.

## 3. Translate regulation → IAIso policy

```java
import cloud.smarttasks.spt.SptClient;

SptClient spt = new SptClient("http://localhost:8000");
String json = spt.translate("Personal data must be redacted.", false, "lmstudio");
// json contains "iaiso_policy" — parse with your JSON library (Jackson/Gson).
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

// enforce with the IAIso Java port:
//   add the iaiso-java dependency (github.com/SmartTasksOrg/IAISO core/iaiso-java)
// parse iaiso_policy and hand it to iaiso-java's bounded execution.

## Notes

The client returns the raw response body; add Jackson/Gson to deserialize `iaiso_policy`.

## One-command end-to-end demo

```bash
cd ports/java
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
