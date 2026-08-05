import SmartPolicyTranslator from "./dist/index.js";
import { readFileSync, readdirSync, writeFileSync, mkdirSync } from "fs";
const [ds, out] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
const spt = new SmartPolicyTranslator(process.env.SPT_URL || "http://localhost:8000");
for (const f of readdirSync(ds).filter((x) => x.endsWith(".txt")).sort()) {
  const res = await spt.translate(readFileSync(`${ds}/${f}`, "utf8"));
  const name = f.replace(/\.txt$/, "");
  writeFileSync(`${out}/${name}.policy.json`, JSON.stringify(res, null, 2));
  console.log(`  ${name}: ${res.iaiso_policy.enforcement_mode}`);
}
