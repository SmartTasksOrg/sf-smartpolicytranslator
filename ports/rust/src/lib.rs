//! Rust client for SmartPolicyTranslator: regulation -> IAIso policy.
//! Pair with the iaiso-rust port (github.com/SmartTasksOrg/IAISO core/iaiso-rust)
//! to enforce the returned policy.
use serde_json::{json, Value};

pub struct SptClient {
    base_url: String,
}

impl SptClient {
    pub fn new(base_url: &str) -> Self {
        let b = if base_url.is_empty() { "http://localhost:8000" } else { base_url };
        SptClient { base_url: b.trim_end_matches('/').to_string() }
    }

    /// Translate regulation text/path/URL into a validated IAIso policy document.
    pub fn translate(&self, uri: &str, use_llm: bool, provider: &str) -> Result<Value, String> {
        let provider = if provider.is_empty() { "lmstudio" } else { provider };
        let resp = ureq::post(&format!("{}/translate", self.base_url))
            .send_json(json!({ "uri": uri, "use_llm": use_llm, "provider": provider }))
            .map_err(|e| e.to_string())?;
        resp.into_json::<Value>().map_err(|e| e.to_string())
    }
}
