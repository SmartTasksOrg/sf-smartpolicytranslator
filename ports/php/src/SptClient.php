<?php
// PHP client for SmartPolicyTranslator: regulation -> IAIso policy.
// Pair with the iaiso-php port (github.com/SmartTasksOrg/IAISO core/iaiso-php).
namespace SmartTasks\Spt;

class SptClient
{
    private string $baseUrl;

    public function __construct(string $baseUrl = 'http://localhost:8000')
    {
        $this->baseUrl = rtrim($baseUrl, '/');
    }

    /** @return array The decoded translate result (contains 'iaiso_policy'). */
    public function translate(string $uri, bool $useLlm = false, string $provider = 'lmstudio'): array
    {
        $payload = json_encode(['uri' => $uri, 'use_llm' => $useLlm, 'provider' => $provider]);
        $ch = curl_init($this->baseUrl . '/translate');
        curl_setopt_array($ch, [
            CURLOPT_POST => true,
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_POSTFIELDS => $payload,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 120,
        ]);
        $body = curl_exec($ch);
        $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        if ($body === false || $code >= 300) {
            throw new \RuntimeException("SPT $code: $body");
        }
        return json_decode($body, true);
    }
}
