// Swift client for SmartPolicyTranslator: regulation -> IAIso policy.
// Pair with the iaiso-swift port (github.com/SmartTasksOrg/IAISO core/iaiso-swift).
import Foundation

public struct SPTClient {
    let baseURL: String
    public init(baseURL: String = "http://localhost:8000") {
        self.baseURL = baseURL.hasSuffix("/") ? String(baseURL.dropLast()) : baseURL
    }

    /// Translate regulation into a validated IAIso policy document (JSON).
    public func translate(uri: String, useLLM: Bool = false, provider: String = "lmstudio") async throws -> [String: Any] {
        var req = URLRequest(url: URL(string: "\(baseURL)/translate")!)
        req.httpMethod = "POST"
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody = try JSONSerialization.data(withJSONObject: [
            "uri": uri, "use_llm": useLLM, "provider": provider])
        let (data, resp) = try await URLSession.shared.data(for: req)
        if let http = resp as? HTTPURLResponse, http.statusCode >= 300 {
            throw NSError(domain: "SPT", code: http.statusCode,
                          userInfo: [NSLocalizedDescriptionKey: String(data: data, encoding: .utf8) ?? ""])
        }
        return try JSONSerialization.jsonObject(with: data) as? [String: Any] ?? [:]
    }
}
