// C# client for SmartPolicyTranslator: regulation -> IAIso policy.
// Pair with the iaiso-csharp port (github.com/SmartTasksOrg/IAISO core/iaiso-csharp).
using System.Text;
using System.Text.Json;

namespace SmartTasks.Spt;

public sealed class SptClient
{
    private readonly HttpClient _http = new() { Timeout = TimeSpan.FromSeconds(120) };
    private readonly string _baseUrl;

    public SptClient(string baseUrl = "http://localhost:8000") =>
        _baseUrl = baseUrl.TrimEnd('/');

    /// <summary>Translate regulation into a validated IAIso policy document.</summary>
    public async Task<JsonElement> TranslateAsync(
        string uri, bool useLlm = false, string provider = "lmstudio")
    {
        var payload = JsonSerializer.Serialize(new { uri, use_llm = useLlm, provider });
        using var content = new StringContent(payload, Encoding.UTF8, "application/json");
        using var res = await _http.PostAsync($"{_baseUrl}/translate", content);
        var body = await res.Content.ReadAsStringAsync();
        if (!res.IsSuccessStatusCode)
            throw new HttpRequestException($"SPT {(int)res.StatusCode}: {body}");
        return JsonSerializer.Deserialize<JsonElement>(body);
    }
}
