/* C client for SmartPolicyTranslator: regulation -> IAIso policy (JSON).
 * Requires libcurl. Pair with an IAIso enforcement layer in your C/C++ stack. */
#ifndef SPT_CLIENT_H
#define SPT_CLIENT_H
/* Returns a malloc'd JSON string (caller frees) or NULL on error.
 * base_url may be NULL -> defaults to http://localhost:8000 */
char *spt_translate(const char *base_url, const char *uri,
                    int use_llm, const char *provider);
#endif
