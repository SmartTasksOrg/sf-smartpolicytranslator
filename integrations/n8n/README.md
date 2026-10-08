# n8n integration

A community node that calls a running SmartPolicyTranslator service and returns the
IAIso policy, so you can translate regulation inside any n8n workflow.

## Install (self-hosted n8n)

```bash
# in your n8n custom-nodes directory (or a package you publish):
npm init -y
npm install n8n-workflow typescript --save-dev
# copy SmartPolicyTranslator.node.ts into ./nodes/ and build:
npx -p typescript tsc SmartPolicyTranslator.node.ts --outDir dist
# point n8n at it:
export N8N_CUSTOM_EXTENSIONS="$(pwd)/dist"
n8n start
```

The node then appears as **SmartPolicyTranslator** under *Transform*.

## Configure the node

| Field | Value |
|---|---|
| Base URL | `http://localhost:8000` (your SPT service) |
| Source | regulation text, a file path, or a URL |
| Use LLM | on to route parsing through a local model |
| Provider | LM Studio / Ollama / llama.cpp |

Output item: `{ policy_id, iaiso_policy, valid, validation_errors, ... }`.

## Enforce downstream

Add a following node that ships `iaiso_policy` into your IAIso deployment (e.g. an
HTTP Request node to your enforcement service, or a Function node using
the IAIso Node SDK from source, `IAIso-v5.0/core/iaiso-node` in the IAISO repository).
SmartPolicyTranslator produces; IAIso enforces.

## One-command end-to-end demo

```bash
cd integrations/n8n
./run_demo.sh                 # checkout IAIso → run over the test dataset → validate vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout
```
