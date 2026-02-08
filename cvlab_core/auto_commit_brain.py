import json
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================
# CVLAB AUTO COMMIT BRAIN v2
# prepares real Jarvis actions
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = PROJECT_ROOT / "cvlab_core" / "system_state.json"
ACTION_FILE = PROJECT_ROOT / "cvlab_core" / "pending_action.json"


def run(cmd):
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )
    return result.stdout.strip()


def read_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def write_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def repo_has_changes():
    out = run("git status --porcelain")
    return len(out.strip()) > 0


def last_commit_time():
    out = run("git log -1 --format=%cd --date=iso")
    return out.strip()


def minutes_since_commit():
    try:
        last = last_commit_time()
        if not last:
            return 0
        last_dt = datetime.fromisoformat(last)
        now = datetime.now(last_dt.tzinfo)
        return int((now - last_dt).total_seconds() / 60)
    except:
        return 0


def pending_action_exists():
    if not ACTION_FILE.exists():
        return False
    try:
        with open(ACTION_FILE, "r") as f:
            data = json.load(f)
            return data.get("status") in ["pending", "approved"]
    except:
        return False


def create_commit_action():
    action = {
        "title": "Safe checkpoint commit",
        "reason": "Uncommitted work detected for long duration",
        "commands": [
            "git add .",
            "git commit -m \"CVLab auto safe checkpoint\"",
            "git push"
        ],
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    with open(ACTION_FILE, "w") as f:
        json.dump(action, f, indent=4)

    print("Jarvis prepared safe commit action.")


def main():
    state = read_state()

    dirty = repo_has_changes()
    mins = minutes_since_commit()

    state["git_status"] = "changes" if dirty else "clean"
    state["git_dirty_minutes"] = mins

    if dirty and mins > 20:
        state["suggest_commit"] = True

        # prepare jarvis action if none exists
        if not pending_action_exists():
            create_commit_action()
    else:
        state["suggest_commit"] = False

    write_state(state)

    print("Auto commit brain checked.")


if __name__ == "__main__":
    main()