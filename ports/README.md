# Language ports

Each port is a thin client that calls a running SmartPolicyTranslator service
(`uvicorn sf_smartpolicytranslator.api:app`) and returns the **IAIso policy** it
generates. SmartPolicyTranslator *produces* the policy; the matching **IAIso port**
*enforces* it — so you can generate and enforce in the same language as your stack.

| Port | Path | Enforce with (IAIso SDK folder in `IAIso-v5.0/core/`, from source; not published on a registry yet) |
|---|---|---|
| Python | `python/spt_client.py` (remote) · `../src/` (in-process) | `iaiso-python` |
| Node / TypeScript | `node/` | `iaiso-node` |
| React | `react/` (uses the Node client) | `iaiso-node` |
| Java | `java/` | `iaiso-java` |
| Go | `go/` | `iaiso-go` |
| PHP | `php/` | `iaiso-php` |
| Ruby | `ruby/` | `iaiso-ruby` |
| Rust | `rust/` | `iaiso-rust` |
| C# | `csharp/` | `iaiso-csharp` |
| Swift | `swift/` | `iaiso-swift` |
| C | `c/` (libcurl) | — (embed via C ABI) |
| C++ | `cpp/` (libcurl, header-only) | — (embed via C ABI) |

IAIso's own ports live at `github.com/SmartTasksOrg/IAISO` → `IAIso-v5.0/core/iaiso-*`.
This set covers every language IAIso ships, plus React and C/C++.

## Quick starts
- **Go:** `import spt "github.com/SmartTasksOrg/sf-smartpolicytranslator/ports/go"` → `spt.New("").Translate(text, false, "lmstudio")`
- **PHP:** `new SmartTasks\Spt\SptClient()->translate($text)` (needs ext-curl)
- **Ruby:** `SmartTasks::SptClient.new.translate(text)`
- **Rust:** `SptClient::new("").translate(text, false, "lmstudio")`
- **C#:** `await new SmartTasks.Spt.SptClient().TranslateAsync(text)`
- **Swift:** `try await SPTClient().translate(uri: text)`
- **C:** `cc c/spt_client.c -lcurl -DSPT_DEMO -o spt && ./spt "…"`
- **C++:** `#include "cpp/SptClient.hpp"` → `smarttasks::SptClient{}.translate(text)` (`-lcurl`)
