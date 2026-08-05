# Test dataset

Six regulations spanning the policy space, used by every port/integration `run_demo.sh`
and by `scripts/translate_dataset.py`:

| File | Character | Expected IAIso policy |
|---|---|---|
| `01_eu_ai_act_excerpt.txt` | high-risk, oversight, disclosure | strict |
| `02_data_protection.txt` | PII redaction, secrets, consent | strict |
| `03_model_security.txt` | prompt-injection, gateway, rate-limit | strict |
| `04_output_assurance.txt` | output verification, audit receipts | strict |
| `05_permissive_analytics.txt` | logging/analytics (no MUST) | permissive |
| `06_workforce.txt` | workforce-impact monitoring (SHOULD/MAY) | permissive |

Add your own `.txt` regulations here; the harness picks them up automatically.
