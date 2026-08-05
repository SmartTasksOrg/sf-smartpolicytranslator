"""python -m smartpolicytranslator.cli examples/sample_regulation.txt [--llm --provider ollama]"""
from __future__ import annotations
import argparse, json, sys
from .pipeline import translate_document
from .llm import LLM


def main(argv=None):
    ap = argparse.ArgumentParser(description="SmartPolicyTranslator — regulation -> IAIso policy")
    ap.add_argument("source"); ap.add_argument("--llm", action="store_true")
    ap.add_argument("--provider", default="lmstudio", choices=["lmstudio", "ollama", "llamacpp"])
    ap.add_argument("--model", default=None); ap.add_argument("--issuer", default="smartpolicytranslator")
    ap.add_argument("--no-persist", action="store_true")
    a = ap.parse_args(argv)
    llm = LLM(provider=a.provider, model=a.model) if a.llm else None
    out = translate_document(a.source, use_llm=a.llm, llm=llm, issuer=a.issuer, persist=not a.no_persist)
    json.dump(out["iaiso_policy"], sys.stdout, indent=2); print()
    print(f"\nIAIso policy · valid={out['valid']} · mode={out['iaiso_policy']['enforcement_mode']} "
          f"· scopes={out['iaiso_policy']['consent']['required_scopes']}", file=sys.stderr)
    if out["validation_errors"]:
        print("errors:", out["validation_errors"], file=sys.stderr)


if __name__ == "__main__":
    main()
