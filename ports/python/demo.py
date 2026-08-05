import os, sys, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spt_client import SptClient
ds, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
c = SptClient(os.environ.get("SPT_URL", "http://localhost:8000"))
for f in sorted(glob.glob(os.path.join(ds, "*.txt"))):
    res = c.translate(open(f, encoding="utf-8").read())
    name = os.path.splitext(os.path.basename(f))[0]
    json.dump(res, open(os.path.join(out, name + ".policy.json"), "w"), indent=2)
    print(f"  {name}: {res['iaiso_policy']['enforcement_mode']}")
