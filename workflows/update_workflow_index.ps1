# PowerShell helper: regenerate WORKFLOW_INDEX.md
# Usage: run this from repository root or from inside the workspace
# Requires Python environment with dependencies installed (requirements.txt)

Write-Host "Generating workflow index..." -ForegroundColor Cyan

$script = Join-Path $PSScriptRoot "..\scripts\generate_workflow_index.py"
if (-not (Test-Path $script)) {
    Write-Error "Cannot find generate_workflow_index.py at $script"
    exit 1
}

$indexFile = Join-Path $PSScriptRoot "WORKFLOW_INDEX.md"
# call Python and capture output
& python $script | Set-Content -Path $indexFile -Encoding utf8

if ($LASTEXITCODE -eq 0) {
    Write-Host "Workflow index updated at $indexFile" -ForegroundColor Green
    Write-Host "Don't forget to review and commit the changes."
} else {
    Write-Host "Python script returned exit code $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}
