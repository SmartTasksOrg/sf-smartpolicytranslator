"""sf-smartpolicytranslator --demo
sf-smartpolicytranslator regulation.txt [--llm --provider ollama]
(also: python -m sf_smartpolicytranslator ...)"""
from __future__ import annotations
import argparse, json, sys
from importlib import resources
from . import __version__
from .pipeline import translate_document
from .llm import LLM

SAMPLE = "sample_regulation.txt"


def sample_regulation() -> str:
    """The bundled sample regulation (a short synthetic text, not a real law), used by --demo."""
    return resources.files(__package__).joinpath("data", SAMPLE).read_text(encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="sf-smartpolicytranslator",
                                 description="SmartPolicyTranslator — regulation -> IAIso policy")
    ap.add_argument("source", nargs="?", help="a regulation: a text/PDF/DOCX file, a URL, or the text itself")
    ap.add_argument("--demo", action="store_true",
                    help="translate the bundled sample regulation (no input file, nothing is saved)")
    ap.add_argument("--version", action="version", version=f"SmartPolicyTranslator {__version__}")
    ap.add_argument("--llm", action="store_true")
    ap.add_argument("--provider", default="lmstudio", choices=["lmstudio", "ollama", "llamacpp"])
    ap.add_argument("--model", default=None); ap.add_argument("--issuer", default="sf-smartpolicytranslator")
    ap.add_argument("--no-persist", action="store_true")
    a = ap.parse_args(argv)
    if a.demo and a.source:
        ap.error("give either --demo or a source, not both")
    if not a.demo and not a.source:
        ap.error("give a regulation to translate, or --demo to translate the bundled sample")
    source = sample_regulation() if a.demo else a.source
    llm = LLM(provider=a.provider, model=a.model) if a.llm else None
    out = translate_document(source, use_llm=a.llm, llm=llm, issuer=a.issuer,
                             persist=not (a.no_persist or a.demo))
    json.dump(out["iaiso_policy"], sys.stdout, indent=2); print()
    print(f"\nIAIso policy · valid={out['valid']} · mode={out['iaiso_policy']['enforcement_mode']} "
          f"· scopes={out['iaiso_policy']['consent']['required_scopes']}", file=sys.stderr)
    if out["validation_errors"]:
        print("errors:", out["validation_errors"], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
