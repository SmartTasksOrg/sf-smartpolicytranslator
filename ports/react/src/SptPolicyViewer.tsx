import React, { useState } from "react";
import SmartPolicyTranslator, { IAIsoPolicy } from "@smarttasks/smartpolicytranslator-client";

/**
 * React component: paste regulation, get a REAL IAIso policy back and render it.
 * Uses the Node/TS client port; pair with iaiso-node to enforce the policy.
 */
export function SptPolicyViewer({ baseUrl = "http://localhost:8000" }: { baseUrl?: string }) {
  const [text, setText] = useState("");
  const [policy, setPolicy] = useState<IAIsoPolicy | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  const run = async () => {
    setBusy(true); setErr("");
    try {
      const spt = new SmartPolicyTranslator(baseUrl);
      const res = await spt.translate(text);
      setPolicy(res.iaiso_policy);
      if (!res.valid) setErr(res.validation_errors.join("; "));
    } catch (e: any) { setErr(String(e)); } finally { setBusy(false); }
  };

  return (
    <div style={{ fontFamily: "system-ui", maxWidth: 720 }}>
      <h3>Regulation → IAIso policy</h3>
      <textarea rows={6} style={{ width: "100%" }} value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste regulatory text…" />
      <button onClick={run} disabled={busy || !text}>
        {busy ? "Translating…" : "Translate to IAIso policy"}
      </button>
      {err && <p style={{ color: "crimson" }}>{err}</p>}
      {policy && (
        <>
          <p><b>enforcement_mode:</b> {policy.enforcement_mode}</p>
          <p><b>required_scopes:</b> {policy.consent.required_scopes.join(", ")}</p>
          <pre style={{ background: "#0f1421", color: "#cdd8ee", padding: 12, overflow: "auto" }}>
            {JSON.stringify(policy, null, 2)}
          </pre>
        </>
      )}
    </div>
  );
}
export default SptPolicyViewer;
