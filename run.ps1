# ======================================================
# CVLab One-Command Runner
# ======================================================

Write-Host ""
Write-Host "========================================"
Write-Host " CVLab Runner"
Write-Host "========================================"
Write-Host ""

$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $PROJECT_ROOT

$VENV_DIR = Join-Path $PROJECT_ROOT ".venv"

if (-not (Test-Path $VENV_DIR)) {
    Write-Host "ERROR: Virtual environment not found."
    Write-Host "Please run install.ps1 first."
    exit 1
}

Write-Host "Activating virtual environment..."
& "$VENV_DIR\Scripts\Activate.ps1"

# -------------------------------
# Mode selection
# -------------------------------

if ($env:CVLAB_MODE -eq "demo") {
    Write-Host "Running in DEMO MODE (read-only)"
} else {
    Write-Host "Running in DEV MODE"
}

Write-Host ""
Write-Host "Launching CVLab..."
Write-Host ""

streamlit run app.py
