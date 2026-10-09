# SmartPolicyTranslator — PHP port

Thin client that calls a running SmartPolicyTranslator service and returns the
**IAIso policy** it generates from regulation text. (SmartPolicyTranslator
*produces* the policy; IAIso *enforces* it — see the repo `INTEGRATION.md`.)

## 1. Start the service

```bash
# from the repo root:
cd sf-smartpolicytranslator && bash scripts/run.sh     # → http://localhost:8000
```

## 2. Set up this port

Requires `ext-curl`.
```bash
cd ports/php
composer install     # sets up PSR-4 autoload for SmartTasks\Spt
```

## 3. Translate regulation → IAIso policy

```php
<?php
require "vendor/autoload.php";
use SmartTasks\Spt\SptClient;

$spt = new SptClient("http://localhost:8000");
$res = $spt->translate("Personal data must be redacted.");
echo $res["iaiso_policy"]["enforcement_mode"];
```

The result's `iaiso_policy` is a schema-conformant IAIso v1 document
(`version`, `enforcement_mode`, `pressure`, `consent.required_scopes`, `metadata`).

## 4. Enforce the policy with IAIso

Enforce with the IAIso PHP port (`iaiso-php`, core/iaiso-php): pass `iaiso_policy` to its execution guard.

## Notes

If you don't use Composer, just `require 'src/SptClient.php';` — it has no dependencies beyond ext-curl.

## One-command end-to-end demo

```bash
cd ports/php
./run_demo.sh                 # checks out IAIso, serves the app, translates the
                              # test dataset via this port, validates vs IAIso
SETUP_IAISO=0 ./run_demo.sh   # skip the IAIso checkout (native validation)
```

It writes one `out/<regulation>.policy.json` per file in `../../examples/dataset/`
and prints a PASS/FAIL per policy from IAIso's validator.
