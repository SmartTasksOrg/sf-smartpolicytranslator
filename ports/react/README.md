# SmartPolicyTranslator — React port

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
cd ports/react
npm install react
```
The client (`@smarttasks/smartpolicytranslator-client`) is not published on npm yet:
build it from `ports/node` in a clone (`npm install && npm run build`) and install it
by path (`npm install ../node`).

## 3. Translate regulation → IAIso policy

```tsx
import { SptPolicyViewer } from "./src/SptPolicyViewer";

export default function App() {
  return <SptPolicyViewer baseUrl="http://localhost:8000" />;
}
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

Enforcement is server-side; the component only displays the generated IAIso policy. Wire enforcement in your backend via the IAIso Node SDK (IAISO repository, `IAIso-v5.0/core/iaiso-node`, from source; not on npm yet).

## Notes

CORS: the SPT service must allow your web origin. For production, proxy `/translate` through your own backend rather than calling it from the browser.

## One-command end-to-end demo

```bash
cd ports/react
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
