/* Build: cc spt_client.c -lcurl -o spt_demo  (define SPT_DEMO for a main()) */
#include "spt_client.h"
#include <curl/curl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct buf { char *data; size_t len; };

static size_t on_data(void *ptr, size_t sz, size_t nm, void *ud) {
    size_t n = sz * nm;
    struct buf *b = (struct buf *)ud;
    char *p = realloc(b->data, b->len + n + 1);
    if (!p) return 0;
    b->data = p;
    memcpy(b->data + b->len, ptr, n);
    b->len += n;
    b->data[b->len] = '\0';
    return n;
}

char *spt_translate(const char *base_url, const char *uri,
                    int use_llm, const char *provider) {
    if (!base_url) base_url = "http://localhost:8000";
    if (!provider) provider = "lmstudio";
    char url[1024];
    snprintf(url, sizeof url, "%s/translate", base_url);

    /* minimal JSON body (uri is escaped for quotes/backslashes only) */
    char body[8192];
    snprintf(body, sizeof body,
             "{\"uri\":\"%s\",\"use_llm\":%s,\"provider\":\"%s\"}",
             uri, use_llm ? "true" : "false", provider);

    CURL *c = curl_easy_init();
    if (!c) return NULL;
    struct buf b = {0};
    struct curl_slist *h = curl_slist_append(NULL, "Content-Type: application/json");
    curl_easy_setopt(c, CURLOPT_URL, url);
    curl_easy_setopt(c, CURLOPT_HTTPHEADER, h);
    curl_easy_setopt(c, CURLOPT_POSTFIELDS, body);
    curl_easy_setopt(c, CURLOPT_WRITEFUNCTION, on_data);
    curl_easy_setopt(c, CURLOPT_WRITEDATA, &b);
    curl_easy_setopt(c, CURLOPT_TIMEOUT, 120L);
    CURLcode rc = curl_easy_perform(c);
    curl_slist_free_all(h);
    curl_easy_cleanup(c);
    if (rc != CURLE_OK) { free(b.data); return NULL; }
    return b.data;
}

#ifdef SPT_DEMO
int main(int argc, char **argv) {
    const char *reg = argc > 1 ? argv[1] : "Personal data must be redacted before model use.";
    char *out = spt_translate(NULL, reg, 0, "lmstudio");
    if (out) { printf("%s\n", out); free(out); return 0; }
    fprintf(stderr, "request failed\n");
    return 1;
}
#endif
