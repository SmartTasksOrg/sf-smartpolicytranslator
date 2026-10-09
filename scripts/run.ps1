$ErrorActionPreference="Stop"; Set-Location "$PSScriptRoot\.."
if (-not (Test-Path .venv)) { python -m venv .venv }
. .\.venv\Scripts\Activate.ps1
pip install -q -r requirements.txt
$env:PYTHONPATH = "$(Get-Location)\src"
Write-Host "SmartPolicyTranslator -> http://localhost:8000/docs"
uvicorn sf_smartpolicytranslator.api:app --reload --port 8000
