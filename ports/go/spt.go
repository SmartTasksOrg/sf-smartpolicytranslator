// Package spt is a Go client for SmartPolicyTranslator: regulation -> IAIso policy.
// Pair with the iaiso-go port (github.com/SmartTasksOrg/IAISO core/iaiso-go) to
// enforce the returned policy in a Go architecture.
package spt

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

type Client struct {
	BaseURL string
	HTTP    *http.Client
}

func New(baseURL string) *Client {
	if baseURL == "" {
		baseURL = "http://localhost:8000"
	}
	return &Client{BaseURL: baseURL, HTTP: &http.Client{Timeout: 120 * time.Second}}
}

type request struct {
	URI      string `json:"uri"`
	UseLLM   bool   `json:"use_llm"`
	Provider string `json:"provider"`
}

// Translate turns regulation text/path/URL into a validated IAIso policy document.
// It returns the parsed JSON as a generic map (iaiso_policy is under "iaiso_policy").
func (c *Client) Translate(uri string, useLLM bool, provider string) (map[string]any, error) {
	if provider == "" {
		provider = "lmstudio"
	}
	body, _ := json.Marshal(request{URI: uri, UseLLM: useLLM, Provider: provider})
	resp, err := c.HTTP.Post(c.BaseURL+"/translate", "application/json", bytes.NewReader(body))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	data, _ := io.ReadAll(resp.Body)
	if resp.StatusCode >= 300 {
		return nil, fmt.Errorf("SPT %d: %s", resp.StatusCode, string(data))
	}
	var out map[string]any
	return out, json.Unmarshal(data, &out)
}
