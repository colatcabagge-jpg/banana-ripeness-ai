# ======================================================
# CVLab One-Command Installer (Windows)
# Location-independent bootstrapper
# ======================================================

Write-Host ""
Write-Host "========================================"
Write-Host " CVLab Automated Installer (Windows)"
Write-Host " Location-independent bootstrapper"
Write-Host "========================================"
Write-Host ""

# -------------------------------
# PowerShell safety
# -------------------------------

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# -------------------------------
# Admin check (optional)
# -------------------------------

function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator
    )
}

if (-not (Test-Admin)) {
    Write-Host "WARNING: Not running as Administrator."
    Write-Host "Some installations may require admin rights."
    Write-Host ""
}

# -------------------------------
# Define fixed install workspace
# -------------------------------

$CVLAB_ROOT = "C:\CVLab"
$REPO_NAME  = "banana-ripeness-ai"
$REPO_DIR   = Join-Path $CVLAB_ROOT $REPO_NAME

Write-Host "CVLab will be installed at:"
Write-Host "  $REPO_DIR"
Write-Host ""

# -------------------------------
# Create workspace (safe)
# -------------------------------

if (-not (Test-Path $CVLAB_ROOT)) {
    Write-Host "Creating workspace directory: $CVLAB_ROOT"
    New-Item -ItemType Directory -Path $CVLAB_ROOT | Out-Null
} else {
    Write-Host "Workspace already exists."
}

Write-Host ""

Write-Host "Phase 1 complete: Installer can run from ANY location."
Write-Host ""

# ======================================================
# PHASE 2 — Python 3.10 + Git AUTO Bootstrap
# ======================================================

Write-Host "----------------------------------------"
Write-Host "Phase 2: Verifying system dependencies"
Write-Host "----------------------------------------"
Write-Host ""

# ======================================================
# 1. Python 3.10 (verify → auto-install)
# ======================================================

Write-Host "Checking for Python 3.10..."

function Test-Python310 {
    try {
        $out = & py -3.10 --version 2>&1
        return ($out -match "Python 3.10")
    } catch {
        return $false
    }
}

if (-not (Test-Python310)) {

    Write-Host "Python 3.10 not found. Installing automatically..."

    $pyUrl  = "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"
    $pyExe  = "$env:TEMP\python-3.10.11-installer.exe"

    Write-Host "Downloading Python 3.10..."
    Invoke-WebRequest -Uri $pyUrl -OutFile $pyExe

    Write-Host "Running Python 3.10 installer (silent)..."
    Start-Process -FilePath $pyExe `
        -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" `
        -Wait

    Write-Host "Python 3.10 installation completed."
} else {
    Write-Host "Python 3.10 already installed."
}

# Final Python verification
try {
    $pyCheck = & py -3.10 --version
    Write-Host "Using $pyCheck"
} catch {
    Write-Host "ERROR: Python 3.10 setup failed."
    exit 1
}

Write-Host ""

# ======================================================
# 2. Git (verify → auto-install)
# ======================================================

Write-Host "Checking for Git..."

function Test-Git {
    try {
        $null = & git --version
        return $true
    } catch {
        return $false
    }
}

if (-not (Test-Git)) {

    Write-Host "Git not found. Installing automatically..."

    # Prefer winget if available (Windows 10/11)
    function Test-Winget {
        try {
            $null = & winget --version
            return $true
        } catch {
            return $false
        }
    }

    if (Test-Winget) {
        Write-Host "Installing Git via winget..."
        winget install --id Git.Git -e --silent
    } else {
        Write-Host "ERROR: winget not available to install Git."
        Write-Host "Please install Git manually from https://git-scm.com"
        exit 1
    }

    Write-Host "Git installation completed."
} else {
    Write-Host "Git already installed."
}

# Final Git verification
try {
    $gitCheck = & git --version
    Write-Host "Using $gitCheck"
} catch {
    Write-Host "ERROR: Git setup failed."
    exit 1
}

Write-Host ""
Write-Host "Phase 2 complete: Python and Git are ready."
Write-Host ""


# ======================================================
# PHASE 3 — Repo clone, venv creation, pip hardening
# ======================================================

Write-Host "----------------------------------------"
Write-Host "Phase 3: Project setup"
Write-Host "----------------------------------------"
Write-Host ""

# -------------------------------
# 1. Clone or update repository
# -------------------------------

$REPO_URL = "https://github.com/colatcabagge-jpg/banana-ripeness-ai.git"

if (-not (Test-Path $REPO_DIR)) {

    Write-Host "Cloning CVLab repository..."
    git clone $REPO_URL $REPO_DIR

} else {

    Write-Host "Repository already exists. Updating..."
    Set-Location $REPO_DIR
    git pull
}

Write-Host ""

# Ensure we are inside repo
Set-Location $REPO_DIR

# -------------------------------
# 2. Create virtual environment
# -------------------------------

$VENV_DIR = Join-Path $REPO_DIR ".venv"

if (-not (Test-Path $VENV_DIR)) {

    Write-Host "Creating virtual environment with Python 3.10..."
    py -3.10 -m venv $VENV_DIR

} else {

    Write-Host "Virtual environment already exists."
}

Write-Host ""

# -------------------------------
# 3. Activate virtual environment
# -------------------------------

Write-Host "Activating virtual environment..."
& "$VENV_DIR\Scripts\Activate.ps1"

Write-Host ""

# -------------------------------
# 4. Upgrade pip toolchain
# -------------------------------

Write-Host "Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel

Write-Host ""

# -------------------------------
# 5. Install project dependencies
# -------------------------------

$REQ_FILE = Join-Path $REPO_DIR "requirements.txt"

if (-not (Test-Path $REQ_FILE)) {
    Write-Host "ERROR: requirements.txt not found." -ForegroundColor Red
    exit 1
}

Write-Host "Installing Python dependencies..."
pip install -r $REQ_FILE

Write-Host ""

# -------------------------------
# Phase 3 complete
# -------------------------------

Write-Host "Phase 3 complete: CVLab environment is ready."
Write-Host ""


# ======================================================
# PHASE 4 — Dataset bootstrap (verified, reproducible)
# ======================================================

Write-Host "----------------------------------------"
Write-Host "Phase 4: Dataset setup"
Write-Host "----------------------------------------"
Write-Host ""

# -------------------------------
# Dataset configuration
# -------------------------------

$DATA_DIR = Join-Path $REPO_DIR "data"
$DATASET_NAME = "banana_ripeness"
$DATASET_DIR = Join-Path $DATA_DIR $DATASET_NAME

# >>> REPLACE WITH YOUR ACTUAL VALUES <<<
$DATASET_URL = "https://github.com/colatcabagge-jpg/banana-ripeness-ai/releases/download/v1.0-dataset/banana_dataset.zip"
$DATASET_SHA256 = "672ec861ef54f34e7c87f5c501e4f74298234c09c5c40e47cb470b6aba2e71aa"

$DATASET_ZIP = Join-Path $DATA_DIR "banana_dataset.zip"

# -------------------------------
# Create data directory
# -------------------------------

if (-not (Test-Path $DATA_DIR)) {
    Write-Host "Creating data directory..."
    New-Item -ItemType Directory -Path $DATA_DIR | Out-Null
}

# -------------------------------
# Download + verify dataset
# -------------------------------

if (-not (Test-Path $DATASET_DIR)) {

    Write-Host "Dataset not found locally."
    Write-Host "Downloading dataset..."

    Invoke-WebRequest -Uri $DATASET_URL -OutFile $DATASET_ZIP

    Write-Host "Verifying dataset integrity (SHA-256)..."

    $downloadedHash = (Get-FileHash $DATASET_ZIP -Algorithm SHA256).Hash.ToLower()
    $expectedHash = $DATASET_SHA256.ToLower()

    if ($downloadedHash -ne $expectedHash) {
        Write-Host "ERROR: Dataset checksum mismatch!" -ForegroundColor Red
        Write-Host "Expected: $expectedHash"
        Write-Host "Got:      $downloadedHash"
        Remove-Item $DATASET_ZIP -Force
        exit 1
    }

    Write-Host "Checksum verified."

    Write-Host "Extracting dataset..."
    Expand-Archive -Path $DATASET_ZIP -DestinationPath $DATA_DIR -Force

    Write-Host "Cleaning up zip file..."
    Remove-Item $DATASET_ZIP -Force

    Write-Host "Dataset ready at:"
    Write-Host "  $DATASET_DIR"

} else {

    Write-Host "Dataset already exists. Skipping download."
}

Write-Host ""
Write-Host "Phase 4 complete: Dataset verified and available."
Write-Host ""
