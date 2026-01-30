Write-Host "====================================="
Write-Host " BANANA RIPENESS AI - TEAM SETUP "
Write-Host "====================================="

# Create venv
Write-Host "Creating Virtual Environment..."
python -m venv .venv

# Activate
Write-Host "Activating Virtual Environment..."
.\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing dependencies..."
pip install -r requirements.txt

Write-Host ""
Write-Host "====================================="
Write-Host " SETUP COMPLETE "
Write-Host "====================================="
Write-Host ""
Write-Host "Next Steps:"
Write-Host "1) Activate env: .\.venv\Scripts\Activate.ps1"
Write-Host "2) Train model: python -m src.train"
Write-Host ""
