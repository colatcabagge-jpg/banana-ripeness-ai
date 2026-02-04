import subprocess
from datetime import datetime
from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parent.parent
JOURNAL_JSON = PROJECT_ROOT / "docs" / "journal_events.json"

AUTO_GIT_EVENTS = {
    "TRAINING_COMPLETED",
    "REGISTRY_UPDATED",
    "DOCS_GENERATED",
    "PRODUCTION_SET",
    "PRODUCTION_LOCKED",
}


def run(cmd: str):
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def git_has_changes() -> bool:
    code, out, _ = run("git status --porcelain")
    return bool(out)


def auto_git_commit_for_latest_event():
    """
    Automatically commit important CVLab events.
    Git PUSH is best-effort and MUST NOT crash training.
    """

    if not JOURNAL_JSON.exists():
        return

    try:
        events = json.loads(JOURNAL_JSON.read_text())
    except Exception:
        # Corrupt journal should never block execution
        print("⚠️ Warning: Unable to read journal_events.json")
        return

    if not events:
        return

    last_event = events[-1]
    event_type = last_event.get("event_type")

    if event_type not in AUTO_GIT_EVENTS:
        return

    if not git_has_changes():
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"{event_type.lower().replace('_', ' ')} [{timestamp}]"

    # ---------- COMMIT (MANDATORY) ----------
    run("git add .")
    code, _, err = run(f'git commit -m "{message}"')
    if code != 0:
        raise RuntimeError(f"Git commit failed: {err}")

    # ---------- PUSH (NON-BLOCKING) ----------
    code, _, err = run("git push")
    if code != 0:
        print("⚠️ Git push skipped (offline/auth issue).")
        print(f"    Reason: {err}")
        print("    Commit is saved locally and can be pushed later.")
        return


def safe_checkpoint_push(reason: str):
    """
    Force-save all changes as a safe checkpoint.
    Push is best-effort and non-blocking.
    """

    code, out, _ = run("git status --porcelain")
    if not out:
        return "Repository already clean. Nothing to checkpoint."

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"checkpoint: {reason} [{timestamp}]"

    run("git add .")
    code, _, err = run(f'git commit -m "{message}"')
    if code != 0:
        raise RuntimeError(err)

    code, _, err = run("git push")
    if code != 0:
        print("⚠️ Checkpoint commit created, but push failed.")
        print(f"    Reason: {err}")
        print("    You can push manually when online.")
        return message + " (local only)"

    return message
