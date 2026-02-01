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


def run(cmd):
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def git_has_changes():
    code, out, _ = run("git status --porcelain")
    return bool(out)


def auto_git_commit_for_latest_event():
    if not JOURNAL_JSON.exists():
        return

    events = json.loads(JOURNAL_JSON.read_text())
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

    run("git add .")
    code, _, err = run(f'git commit -m "{message}"')
    if code != 0:
        raise RuntimeError(f"Git commit failed: {err}")

    code, _, err = run("git push")
    if code != 0:
        raise RuntimeError(f"Git push failed: {err}")
