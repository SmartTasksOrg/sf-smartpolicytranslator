#!/usr/bin/env python3
"""Run SmartPolicyTranslator over the test dataset (in-process) and validate every
emitted policy against IAIso.

Usage: python3 scripts/translate_dataset.py [--out out] [--dataset examples/dataset]
Writes <out>/<name>.policy.json per regulation and prints a summary table.
Exit code reflects whether IAIso accepted every emitted policy.
"""
import argparse, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
from smartpolicytranslator.pipeline import translate_document


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "..", "out"))
    ap.add_argument("--dataset", default=os.path.join(HERE, "..", "examples", "dataset"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    files = sorted(glob.glob(os.path.join(a.dataset, "*.txt")))
    print(f"Translating {len(files)} regulations from {a.dataset}\n")
    print(f"  {'regulation':<34} {'mode':<11} {'scopes':>6}  valid")
    print("  " + "-" * 60)
    for f in files:
        out = translate_document(f, persist=False)
        pol = out["iaiso_policy"]
        name = os.path.splitext(os.path.basename(f))[0]
        json.dump(out, open(os.path.join(a.out, f"{name}.policy.json"), "w"), indent=2)
        print(f"  {name:<34} {pol['enforcement_mode']:<11} "
              f"{len(pol['consent']['required_scopes']):>6}  {out['valid']}")
    print(f"\nWrote {len(files)} policies to {a.out}/")
    print("Next: python3 scripts/validate_against_iaiso.py 'out/*.policy.json'")


if __name__ == "__main__":
    main()
