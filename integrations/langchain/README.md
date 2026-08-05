# LangChain integration

Two capabilities live in `spt_iaiso_langchain.py`:

## A. A LangChain Tool that emits IAIso policy

Lets an agent translate regulation mid-chain.

```python
from spt_iaiso_langchain import make_spt_tool

tool = make_spt_tool()                                  # in-process
# tool = make_spt_tool(base_url="http://localhost:8000")# against a running service

# with any LangChain agent:
from langchain.agents import initialize_agent
agent = initialize_agent([tool], llm, agent="zero-shot-react-description")
agent.run("Translate this regulation into an IAIso policy: <paste text>")
```

Requires nothing beyond this repo for the in-process form. `langchain` only if you
want the real `Tool` wrapper (otherwise a plain callable is returned).

## B. Enforce the translated policy in LangChain via the REAL IAIso SDK

This is the full loop — regulation → IAIso policy → governed LLM:

```python
from spt_iaiso_langchain import bounded_execution_from_regulation
from langchain_openai import ChatOpenAI

execution, handler, policy = bounded_execution_from_regulation("regulation.txt")
llm = ChatOpenAI(callbacks=[handler])      # now governed by the translated policy
# check execution.check() between steps for enforcement decisions
```

### Install

```bash
pip install iaiso[langchain]      # the real IAIso SDK + its LangChain middleware
```

`bounded_execution_from_regulation()` builds a real `iaiso.PressureConfig` from the
translated policy's `pressure` block, starts a real `iaiso.BoundedExecution`, and
attaches IAIso's `IAIsoCallbackHandler`. Per IAIso's design the handler is
**advisory** (it accounts for tokens/tool-calls and emits audit events); make
pause/reset/reject decisions by calling `execution.check()` between chain steps, or
wrap the model with `iaiso.middleware.openai` / `.anthropic` for hard enforcement.

## How it fits together

SmartPolicyTranslator turns your regulation into the IAIso policy; IAIso's SDK
enforces it. See the repo `INTEGRATION.md` for the produce↔validate↔enforce model.

## One-command end-to-end demo

```bash
cd integrations/langchain
./run_demo.sh                 # checkout IAIso → run over the test dataset → validate vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout
```
