# ======================================================
# CVLab One-Command Runner
# ======================================================

Write-Host ""
Write-Host "========================================"
Write-Host " CVLab Runner"
Write-Host "========================================"
Write-Host ""

# -------------------------------
# Resolve project root safely
# -------------------------------

$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $PROJECT_ROOT

Write-Host "Project root:"
Write-Host "  $PROJECT_ROOT"
Write-Host ""

# -------------------------------
# Verify virtual environment
# -------------------------------

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

# ======================================================
# SAFE AUTO-UPDATE FROM GITHUB
# ======================================================

Write-Host "----------------------------------------"
Write-Host "Checking for updates from GitHub"
Write-Host "----------------------------------------"

try {
    python scripts/git_autoupdate.py
} catch {
    Write-Host "⚠️ Auto-update skipped due to an error."
    Write-Host "Continuing with local version."
}

Write-Host ""

# ======================================================
# Launch CVLab
# ======================================================

Write-Host "Launching CVLab..."
Write-Host ""

streamlit run app.py
