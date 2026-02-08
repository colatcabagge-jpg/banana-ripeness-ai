import subprocess
import json
from pathlib import Path
from datetime import datetime

# ============================================
# CVLAB AUTONOMOUS INTELLIGENCE ENGINE v3
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = PROJECT_ROOT / "cvlab_core" / "system_state.json"


def run_git(cmd):
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )
    return result.stdout.strip(), result.stderr.strip()


# --------------------------------------------
# Git status
# --------------------------------------------
def check_git_status():
    out, err = run_git("git status --porcelain")

    if err:
        return "unknown"

    if out.strip() == "":
        return "clean"
    else:
        return "changes"


# --------------------------------------------
# Last commit time
# --------------------------------------------
def get_last_commit_time():
    out, err = run_git("git log -1 --date=iso --pretty=format:%cd")

    if err or not out:
        return None

    try:
        return datetime.strptime(out.strip()[:19], "%Y-%m-%d %H:%M:%S")
    except:
        return None


# --------------------------------------------
# MAIN UPDATE
# --------------------------------------------
def update_state():

    if not STATE_FILE.exists():
        return

    with open(STATE_FILE, "r") as f:
        data = json.load(f)

    now = datetime.now()

    # =============================
    # GIT STATE
    # =============================
    git_state = check_git_status()
    data["git_status"] = git_state

    last_commit = get_last_commit_time()
    if last_commit:
        data["git_last_commit_time"] = last_commit.strftime("%Y-%m-%d %H:%M")

    # Track dirty time
    if git_state == "changes":
        data["git_dirty_minutes"] = data.get("git_dirty_minutes", 0) + 1
    else:
        data["git_dirty_minutes"] = 0

    # Suggest commit after 45 min dirty
    if data["git_dirty_minutes"] > 45:
        data["suggest_commit"] = True
    else:
        data["suggest_commit"] = False

    # =============================
    # MOMENTUM CHECK
    # =============================
    try:
        last = datetime.strptime(data["last_session_time"], "%Y-%m-%d %H:%M")
        diff = now - last

        if diff.days == 0:
            data["momentum_state"] = "active"
        elif diff.days <= 2:
            data["momentum_state"] = "steady"
        else:
            data["momentum_state"] = "paused"
    except:
        data["momentum_state"] = "unknown"

    # =============================
    # SESSION RUNTIME
    # =============================
    try:
        start = datetime.strptime(data["session_start_time"], "%Y-%m-%d %H:%M")
        runtime = now - start
        runtime_min = int(runtime.total_seconds() / 60)
        data["session_runtime_min"] = runtime_min
    except:
        runtime_min = 0
        data["session_runtime_min"] = 0

    # =============================
    # FATIGUE DETECTION
    # =============================
    if runtime_min > 120:
        data["fatigue_flag"] = True
    else:
        data["fatigue_flag"] = False

    # =============================
    # STEP STALE DETECTION
    # =============================
    try:
        step_date = datetime.strptime(data["next_step_last_changed"], "%Y-%m-%d")
        diff = now.date() - step_date.date()
        data["step_stale_days"] = diff.days

        if diff.days >= 5:
            data["drift_flag"] = "step_stale"
        else:
            data["drift_flag"] = "none"
    except:
        data["step_stale_days"] = 0

    # =============================
    # FOCUS STATE
    # =============================
    if data["fatigue_flag"]:
        data["focus_state"] = "fatigued"
    elif data.get("suggest_commit"):
        data["focus_state"] = "needs_commit"
    else:
        data["focus_state"] = "stable"

    # =============================
    # SAVE
    # =============================
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    update_state()
    print("CVLab autonomous engine updated.")