/**
 * SmartPolicyTranslator — Node/TypeScript client.
 * Translates regulation into a REAL IAIso policy document. Pair with the
 * `iaiso-node` port (github.com/SmartTasksOrg/IAISO core/iaiso-node) to enforce
 * the returned policy in a Node/JS architecture.
 */
export interface IAIsoPolicy {
  version: "1";
  enforcement_mode: "permissive" | "strict";
  pressure: Record<string, number | boolean>;
  consent: { issuer: string | null; default_ttl_seconds: number;
             required_scopes: string[]; allowed_algorithms: string[] };
  metadata: Record<string, unknown>;
}
export interface TranslateResult {
  policy_id: string; framework: "IAIso"; iaiso_policy: IAIsoPolicy;
  valid: boolean; validation_errors: string[];
}

export class SmartPolicyTranslator {
  constructor(private baseUrl = "http://localhost:8000") {}

  async health(): Promise<any> { return (await fetch(`${this.baseUrl}/health`)).json(); }
  async iaisoSchema(): Promise<any> { return (await fetch(`${this.baseUrl}/iaiso/schema`)).json(); }

  /** Regulation text / path / URL -> a validated IAIso policy document. */
  async translate(uri: string, opts: { useLlm?: boolean;
      provider?: "lmstudio" | "ollama" | "llamacpp" } = {}): Promise<TranslateResult> {
    const res = await fetch(`${this.baseUrl}/translate`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ uri, use_llm: opts.useLlm ?? false,
                             provider: opts.provider ?? "lmstudio" }),
    });
    if (!res.ok) throw new Error(`SPT ${res.status}: ${await res.text()}`);
    return res.json() as Promise<TranslateResult>;
  }
}
export default SmartPolicyTranslator;
