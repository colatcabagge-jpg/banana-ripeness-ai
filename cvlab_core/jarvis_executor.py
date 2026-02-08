import subprocess
import json
from pathlib import Path
from datetime import datetime

# ============================================
# CVLAB JARVIS EXECUTION ENGINE
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = PROJECT_ROOT / "cvlab_core" / "system_state.json"
ACTION_FILE = PROJECT_ROOT / "cvlab_core" / "pending_action.json"
LOG_FILE = PROJECT_ROOT / "cvlab_core" / "execution_log.txt"


# ============================================
# UTILITIES
# ============================================

def load_state():
    if not STATE_FILE.exists():
        return {}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_log(text):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}]\n{text}\n")


# ============================================
# CREATE PENDING ACTION
# ============================================

def create_action(title, commands, reason=""):
    """
    Creates a pending action for user approval.
    """
    action = {
        "title": title,
        "commands": commands,
        "reason": reason,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    with open(ACTION_FILE, "w") as f:
        json.dump(action, f, indent=4)

    print("Pending action created.")


# ============================================
# EXECUTE APPROVED ACTION
# ============================================

def execute_action():
    if not ACTION_FILE.exists():
        print("No pending action.")
        return

    with open(ACTION_FILE, "r") as f:
        action = json.load(f)

    if action.get("status") != "approved":
        print("Action not approved yet.")
        return

    print(f"Executing: {action['title']}")
    save_log(f"EXECUTING: {action['title']}")

    for cmd in action["commands"]:
        print(f"> {cmd}")
        save_log(f"CMD: {cmd}")

        result = subprocess.run(
            cmd,
            shell=True,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )

        save_log(result.stdout)
        save_log(result.stderr)

    action["status"] = "executed"

    with open(ACTION_FILE, "w") as f:
        json.dump(action, f, indent=4)

    print("Action executed and logged.")


# ============================================
# APPROVE ACTION
# ============================================

def approve_action():
    if not ACTION_FILE.exists():
        print("No pending action.")
        return

    with open(ACTION_FILE, "r") as f:
        action = json.load(f)

    action["status"] = "approved"

    with open(ACTION_FILE, "w") as f:
        json.dump(action, f, indent=4)

    print("Action approved. Run executor to execute.")


# ============================================
# VIEW ACTION
# ============================================

def show_action():
    if not ACTION_FILE.exists():
        print("No pending action.")
        return

    with open(ACTION_FILE, "r") as f:
        action = json.load(f)

    print("\n=== PENDING ACTION ===")
    print("Title:", action["title"])
    print("Reason:", action["reason"])
    print("Status:", action["status"])
    print("Commands:")
    for c in action["commands"]:
        print(" ", c)
    print("======================\n")


if __name__ == "__main__":
    print("Jarvis executor ready.")