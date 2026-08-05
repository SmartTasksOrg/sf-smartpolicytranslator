import os, sys, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))
from spt_iaiso_langchain import make_spt_tool

ds, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
tool = make_spt_tool()                       # in-process LangChain tool
run = tool.func if hasattr(tool, "func") else tool
for f in sorted(glob.glob(os.path.join(ds, "*.txt"))):
    policy = json.loads(run(open(f, encoding="utf-8").read()))
    name = os.path.splitext(os.path.basename(f))[0]
    json.dump({"iaiso_policy": policy}, open(os.path.join(out, name + ".policy.json"), "w"), indent=2)
    print(f"  {name}: {policy['enforcement_mode']}")

# optional: prove the full enforcement loop when the real IAIso SDK is installed
try:
    from spt_iaiso_langchain import bounded_execution_from_regulation
    first = sorted(glob.glob(os.path.join(ds, "*.txt")))[0]
    ex, handler, pol = bounded_execution_from_regulation(first)
    print(f"  [enforce] BoundedExecution started; handler = {type(handler).__name__}")
    if hasattr(ex, "__exit__"): ex.__exit__(None, None, None)
except Exception as e:
    print(f"  [enforce] skipped — install iaiso[langchain] ({type(e).__name__})")
