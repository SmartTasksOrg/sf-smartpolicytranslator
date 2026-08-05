#!/usr/bin/env python3
"""Validate emitted IAIso policy JSON files against IAIso's OWN validator.

Usage: python3 scripts/validate_against_iaiso.py out/*.policy.json
Exit code 0 = all accepted by IAIso; 1 = at least one rejected.

If the real `iaiso` package is installed, this routes through
`iaiso.policy._validate`. Otherwise it falls back to the vendored spec's native
validator (which passes all of IAIso's official vectors), and says so.
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))


def _iaiso_validate(doc):
    try:
        from iaiso.policy import _validate, PolicyError
    except Exception:
        return None
    try:
        _validate(doc)
        return []
    except PolicyError as e:
        return [str(e)]
    except Exception as e:
        return [f"{type(e).__name__}: {e}"]


def main(argv):
    paths = []
    for a in argv or ["out/*.policy.json"]:
        paths += glob.glob(a)
    if not paths:
        print("no policy files matched", file=sys.stderr); return 1

    from smartpolicytranslator import iaiso_policy as native
    engine = "IAIso SDK (iaiso.policy._validate)"
    if _iaiso_validate({"version": "1"}) is None:
        engine = "native validator (iaiso package not installed)"

    ok = True
    for p in sorted(paths):
        doc = json.load(open(p))
        pol = doc.get("iaiso_policy", doc)
        errs = _iaiso_validate(pol)
        if errs is None:
            errs = native.validate(pol)
        status = "PASS" if not errs else "FAIL"
        ok = ok and not errs
        print(f"  [{status}] {os.path.basename(p)}"
              + (f"  → {errs}" if errs else ""))
    print(f"\nValidated with: {engine}")
    print("ALL POLICIES ACCEPTED BY IAIso" if ok else "SOME POLICIES REJECTED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
