# Flowise integration

A custom Tool node that returns the IAIso policy to a Flowise agent.

## Install

```bash
# in your Flowise custom-tools/components directory:
npm install flowise-components typescript --save-dev
# copy SmartPolicyTranslator_Flowise.ts into your components folder and build:
npx -p typescript tsc SmartPolicyTranslator_Flowise.ts
# restart Flowise so it picks up the new tool
```

The tool appears as **SmartPolicyTranslator** under *Tools*.

## Configure

| Field | Value |
|---|---|
| Base URL | `http://localhost:8000` (your SPT service) |

Attach it to an Agent/Tool-Agent node. The agent can then call
`smart_policy_translator` with regulation text and receive the IAIso policy JSON as
the tool result to reason over.

## Enforce

The tool output is the IAIso policy document; enforce it in your app via the IAIso
SDK (`iaiso`) or the matching `iaiso-<lang>` port. See the repo `INTEGRATION.md`.

## One-command end-to-end demo

```bash
cd integrations/flowise
./run_demo.sh                 # checkout IAIso → run over the test dataset → validate vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout
```
