package cloud.smarttasks.spt;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * SmartPolicyTranslator — Java client. Translates regulation into a REAL IAIso
 * policy document (JSON). Pair with the iaiso-java port
 * (github.com/SmartTasksOrg/IAISO core/iaiso-java) to enforce the policy in a
 * JVM architecture.
 */
public class SptClient {
    private final String baseUrl;
    private final HttpClient http = HttpClient.newHttpClient();

    public SptClient(String baseUrl) { this.baseUrl = baseUrl; }
    public SptClient() { this("http://localhost:8000"); }

    /** @return the raw JSON translate result (contains iaiso_policy). */
    public String translate(String uri, boolean useLlm, String provider) throws Exception {
        String body = String.format(
            "{\"uri\":%s,\"use_llm\":%s,\"provider\":\"%s\"}",
            quote(uri), useLlm, provider);
        HttpRequest req = HttpRequest.newBuilder(URI.create(baseUrl + "/translate"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(body)).build();
        HttpResponse<String> res = http.send(req, HttpResponse.BodyHandlers.ofString());
        if (res.statusCode() >= 300) throw new RuntimeException("SPT " + res.statusCode() + ": " + res.body());
        return res.body();
    }

    public String health() throws Exception {
        HttpResponse<String> res = http.send(
            HttpRequest.newBuilder(URI.create(baseUrl + "/health")).GET().build(),
            HttpResponse.BodyHandlers.ofString());
        return res.body();
    }

    private static String quote(String s) {
        return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"")
                       .replace("\n", "\\n") + "\"";
    }
}
