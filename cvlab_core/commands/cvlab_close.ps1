# ============================================
# CVLab Close Session
# Logs progress and updates memory safely
# ============================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "        CVLAB SESSION CLOSE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --- Resolve paths ---
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Resolve-Path (Join-Path $SCRIPT_DIR "..\..")
$STATE_FILE = Join-Path $PROJECT_ROOT "cvlab_core\memory\current_state.md"
$DECISION_FILE = Join-Path $PROJECT_ROOT "cvlab_core\memory\decisions_log.md"

# Ask what happened today
Write-Host ""
$update = Read-Host "What did you work on? (one line is enough)"

if ([string]::IsNullOrWhiteSpace($update)) {
    $update = "Session ended without notes."
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

# --- Update CURRENT STATE (append evolution note) ---
Add-Content $STATE_FILE ""
Add-Content $STATE_FILE "Update [$timestamp]: $update"

# --- Log into decisions as evolution entry ---
Add-Content $DECISION_FILE ""
Add-Content $DECISION_FILE "Date: $timestamp"
Add-Content $DECISION_FILE "Decision Title: Session Progress Update"
Add-Content $DECISION_FILE "Context: Normal working session"
Add-Content $DECISION_FILE "Final Choice: Continued system progress"
Add-Content $DECISION_FILE "Reason: $update"
Add-Content $DECISION_FILE "Impact: System evolution ongoing"
Add-Content $DECISION_FILE "Future Revisit Needed: No"
Add-Content $DECISION_FILE "------------------------------------"

Write-Host ""
Write-Host "Session logged successfully." -ForegroundColor Green
Write-Host "Memory updated. Safe to close work." -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CVLab ready for next session." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""