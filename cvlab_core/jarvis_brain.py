import json
from pathlib import Path
from datetime import datetime

# ============================================
# CVLAB JARVIS BRAIN — AUTO ACTION GENERATOR
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = PROJECT_ROOT / "cvlab_core" / "system_state.json"
ACTION_FILE = PROJECT_ROOT / "cvlab_core" / "pending_action.json"


def load_state():
    if not STATE_FILE.exists():
        return None
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_action(action):
    with open(ACTION_FILE, "w") as f:
        json.dump(action, f, indent=4)


def action_exists():
    if not ACTION_FILE.exists():
        return False
    try:
        with open(ACTION_FILE, "r") as f:
            data = json.load(f)
            return data.get("status") in ["pending", "approved"]
    except:
        return False


def create_action(title, reason, commands):
    action = {
        "title": title,
        "reason": reason,
        "commands": commands,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    save_action(action)
    print(f"Jarvis prepared action: {title}")


def evaluate():
    state = load_state()
    if not state:
        return

    # Don't create new action if one already pending
    if action_exists():
        return

    git_dirty = state.get("git_dirty_minutes", 0)
    runtime = state.get("session_runtime_min", 0)
    phase = state.get("current_phase", "")

    # ============================================
    # SAFE COMMIT ACTION
    # ============================================
    if git_dirty > 60:
        create_action(
            title="Safe checkpoint commit",
            reason="Repository has uncommitted changes for long duration",
            commands=[
                "git add .",
                "git commit -m 'CVLab auto safe checkpoint'",
                "git push"
            ]
        )
        return

    # ============================================
    # FATIGUE RESET ACTION
    # ============================================
    if runtime > 150:
        create_action(
            title="Short reset recommended",
            reason="Long continuous session detected",
            commands=[
                "echo Take a 5 minute break. Drink water. Come back fresh."
            ]
        )
        return

    # ============================================
    # DATASET COLLECTION PHASE ASSIST
    # ============================================
    if "dataset" in phase.lower():
        dataset_path = PROJECT_ROOT / "data" / "real_world"

        if not dataset_path.exists():
            create_action(
                title="Create real-world dataset folder",
                reason="Preparing structured dataset collection",
                commands=[
                    "mkdir data\\real_world",
                    "mkdir data\\real_world\\raw",
                    "mkdir data\\real_world\\sorted"
                ]
            )
            return

    # ============================================
    # DEFAULT: NO ACTION
    # ============================================
    # System continues silently


if __name__ == "__main__":
    evaluate()