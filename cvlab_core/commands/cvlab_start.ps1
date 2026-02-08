# ============================================
# CVLab Start Session (updates system state)
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "        CVLAB SESSION START" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --- Paths ---
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Resolve-Path (Join-Path $SCRIPT_DIR "..\..")
$MEMORY_FILE = Join-Path $PROJECT_ROOT "cvlab_core\memory\current_state.md"
$STATE_FILE = Join-Path $PROJECT_ROOT "cvlab_core\system_state.json"

Write-Host "Project Root:" $PROJECT_ROOT -ForegroundColor DarkGray
Write-Host ""

if (-not (Test-Path $MEMORY_FILE)) {
    Write-Host "ERROR: current_state.md not found." -ForegroundColor Red
    exit 1
}

# --- Update system_state.json ---
if (Test-Path $STATE_FILE) {
    $json = Get-Content $STATE_FILE | ConvertFrom-Json
    $json.last_session_time = (Get-Date).ToString("yyyy-MM-dd HH:mm")
    $json.last_action = "Session started"
    $json.session_count = [int]$json.session_count + 1
    $json | ConvertTo-Json -Depth 5 | Set-Content $STATE_FILE
}

$content = Get-Content $MEMORY_FILE

function ShowSection($title, $color) {
    $start = ($content | Select-String $title).LineNumber
    if ($start) {
        Write-Host ""
        for ($i = $start; $i -lt $content.Length; $i++) {
            if ($i -ne $start -and $content[$i] -match "^# ") { break }
            Write-Host $content[$i] -ForegroundColor $color
        }
    }
}

ShowSection "ACTIVE PRIMARY PROJECT" Yellow
ShowSection "CURRENT PHASE" Cyan

Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor DarkGray
Write-Host "TODAY'S PRIMARY ACTION" -ForegroundColor Green
Write-Host "----------------------------------------" -ForegroundColor DarkGray

ShowSection "CURRENT ACTIVE STEP" Green

Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor DarkGray
Write-Host "AFTER THAT" -ForegroundColor Magenta
Write-Host "----------------------------------------" -ForegroundColor DarkGray

ShowSection "NEXT STEP AFTER CURRENT" Magenta

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Session started. System tracking active." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""