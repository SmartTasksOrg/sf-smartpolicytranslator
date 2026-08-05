// C++ client for SmartPolicyTranslator: regulation -> IAIso policy (JSON string).
// Header-only; requires libcurl. Build: c++ -std=c++17 your.cpp -lcurl
// Pair with an IAIso enforcement layer in your C++ stack.
#pragma once
#include <curl/curl.h>
#include <stdexcept>
#include <string>

namespace smarttasks {

class SptClient {
public:
    explicit SptClient(std::string base_url = "http://localhost:8000")
        : base_url_(std::move(base_url)) {
        if (!base_url_.empty() && base_url_.back() == '/') base_url_.pop_back();
    }

    // Returns the raw JSON translate result (contains "iaiso_policy").
    std::string translate(const std::string& uri, bool use_llm = false,
                          const std::string& provider = "lmstudio") {
        std::string body = "{\"uri\":\"" + escape(uri) + "\",\"use_llm\":" +
                           (use_llm ? "true" : "false") + ",\"provider\":\"" +
                           provider + "\"}";
        CURL* c = curl_easy_init();
        if (!c) throw std::runtime_error("curl init failed");
        std::string out;
        curl_slist* h = curl_slist_append(nullptr, "Content-Type: application/json");
        curl_easy_setopt(c, CURLOPT_URL, (base_url_ + "/translate").c_str());
        curl_easy_setopt(c, CURLOPT_HTTPHEADER, h);
        curl_easy_setopt(c, CURLOPT_POSTFIELDS, body.c_str());
        curl_easy_setopt(c, CURLOPT_WRITEFUNCTION, &SptClient::write);
        curl_easy_setopt(c, CURLOPT_WRITEDATA, &out);
        curl_easy_setopt(c, CURLOPT_TIMEOUT, 120L);
        CURLcode rc = curl_easy_perform(c);
        curl_slist_free_all(h);
        curl_easy_cleanup(c);
        if (rc != CURLE_OK) throw std::runtime_error(curl_easy_strerror(rc));
        return out;
    }

private:
    static size_t write(char* ptr, size_t sz, size_t nm, void* ud) {
        static_cast<std::string*>(ud)->append(ptr, sz * nm);
        return sz * nm;
    }
    static std::string escape(const std::string& s) {
        std::string o;
        for (char ch : s) {
            if (ch == '"' || ch == '\\') o += '\\';
            if (ch == '\n') { o += "\\n"; continue; }
            o += ch;
        }
        return o;
    }
    std::string base_url_;
};

}  // namespace smarttasks
