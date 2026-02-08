# ============================================
# CVLab Status Command (Stable Version)
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "        CVLAB SYSTEM STATUS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --- Project root (fixed: 3 levels up) ---
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Resolve-Path (Join-Path $SCRIPT_DIR "..\..")
$MEMORY_FILE = Join-Path $PROJECT_ROOT "cvlab_core\memory\current_state.md"

Write-Host "Project Root:" $PROJECT_ROOT -ForegroundColor DarkGray
Write-Host ""

if (-not (Test-Path $MEMORY_FILE)) {
    Write-Host "ERROR: current_state.md not found." -ForegroundColor Red
    Write-Host "Expected path:" $MEMORY_FILE -ForegroundColor Red
    exit 1
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
ShowSection "CURRENT ACTIVE STEP" Green
ShowSection "NEXT STEP AFTER CURRENT" Magenta
ShowSection "FLEXIBLE FUTURE ROADMAP" DarkCyan
ShowSection "CURRENT SYSTEM HEALTH" DarkYellow

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "System ready." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""