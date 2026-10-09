# Integrations & ports

SmartPolicyTranslator produces **IAIso policy**; IAIso enforces it. These wire the
two into a company's architecture.

| Target | Path | Notes |
|---|---|---|
| LangChain (+ real IAIso SDK) | `langchain/spt_iaiso_langchain.py` | `make_spt_tool()` emits the policy; `bounded_execution_from_regulation()` loads it into IAIso's real `BoundedExecution` + `IAIsoCallbackHandler` so a LangChain LLM is governed by the translated policy. |
| n8n | `n8n/SmartPolicyTranslator.node.ts` | community node calling the REST service. |
| Flowise | `flowise/SmartPolicyTranslator_Flowise.ts` | tool node returning the IAIso policy. |
| Language ports | `../ports/{node,react,java,go,php,ruby,rust,csharp,swift,c,cpp}` | client per language; each pairs with the matching `iaiso-*` port. See `../ports/README.md`. |
| LM Studio / Ollama / llama.cpp | `../src/sf_smartpolicytranslator/llm.py` | one OpenAI-compatible client for optional semantic parsing. |

IAIso itself ships ports in Python, Node, Java, Go, PHP, Ruby, Rust, C#, and Swift
(github.com/SmartTasksOrg/IAISO, `IAIso-v5.0/core/`). Our ports mirror that set so a
translated policy can be consumed in the same language as your IAIso deployment.
