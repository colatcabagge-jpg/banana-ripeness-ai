import json
from pathlib import Path
from datetime import datetime

# ============================================
# CVLAB SESSION MEMORY BRAIN
# Tracks daily engineering progress
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = PROJECT_ROOT / "cvlab_core" / "system_state.json"
SESSION_LOG = PROJECT_ROOT / "cvlab_core" / "memory" / "session_log.json"


def read_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def write_session_log(entry):
    try:
        if SESSION_LOG.exists():
            with open(SESSION_LOG, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(entry)

        with open(SESSION_LOG, "w") as f:
            json.dump(data, f, indent=4)

    except:
        pass


def detect_session_update():
    state = read_state()

    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "active_project": state.get("active_project", ""),
        "phase": state.get("current_phase", ""),
        "momentum": state.get("momentum_state", ""),
        "git_status": state.get("git_status", ""),
        "focus": state.get("focus_state", ""),
        "notes": "Auto session capture"
    }

    write_session_log(entry)
    print("Session memory updated.")


if __name__ == "__main__":
    detect_session_update()