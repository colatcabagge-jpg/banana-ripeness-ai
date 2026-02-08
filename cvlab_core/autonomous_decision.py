import json
from pathlib import Path
from datetime import datetime

# ============================================
# CVLAB AUTONOMOUS CORE BRAIN (FINAL STABLE)
# Single unified decision engine
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = PROJECT_ROOT / "cvlab_core" / "system_state.json"


# ============================================
# BASIC IO
# ============================================

def load_state():
    if not STATE_FILE.exists():
        return None
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ============================================
# FAILURE DETECTION
# ============================================

def detect_failures():
    failures = []

    dataset_path = PROJECT_ROOT / "data"
    model_path = PROJECT_ROOT / "models"
    docs_path = PROJECT_ROOT / "docs"
    git_path = PROJECT_ROOT / ".git"

    if not dataset_path.exists():
        failures.append("Dataset folder missing")

    elif len(list(dataset_path.glob("*"))) == 0:
        failures.append("Dataset folder exists but empty")

    if not model_path.exists():
        failures.append("Models folder missing")

    if not git_path.exists():
        failures.append("Git repository missing")

    if docs_path.exists():
        for f in docs_path.glob("*.log"):
            failures.append(f"Crash log detected: {f.name}")

    return failures


def log_failures(failures):
    fail_log = PROJECT_ROOT / "cvlab_core" / "memory" / "failures_log.md"

    try:
        with open(fail_log, "a", encoding="utf-8") as f:
            f.write("\n\n---\n")
            f.write(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("Failure Title: Automatic system detection\n")
            f.write("What Happened:\n")
            for fl in failures:
                f.write(f"- {fl}\n")
            f.write("\nRoot Cause:\nStructural issue detected\n")
            f.write("\nFix Applied:\nPending\n")
            f.write("\nLesson Learned:\nSystem must remain complete\n")
            f.write("\nPrevention Rule:\nNever ignore system warnings\n")
    except:
        pass


# ============================================
# PROJECT INTELLIGENCE
# ============================================

def project_intelligence(data):
    stage = data.get("project_stage", "")
    dataset_path = PROJECT_ROOT / "data" / "real_world"

    # DATA COLLECTION PHASE
    if stage == "data_collection":

        if not dataset_path.exists():
            data["autonomous_decision"] = "create_dataset"
            data["autonomous_message"] = "Create real-world dataset folders."
            return True

        img_count = len(list(dataset_path.glob("**/*.jpg"))) + len(list(dataset_path.glob("**/*.png")))

        if img_count < 120:
            data["autonomous_decision"] = "collect_dataset"
            data["autonomous_message"] = f"Dataset small ({img_count} images). Capture more real images."
            return True

        else:
            data["project_stage"] = "training_ready"
            data["next_engineering_step"] = "Retrain model with real dataset"
            data["last_progress_update"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            data["autonomous_decision"] = "ready_for_training"
            data["autonomous_message"] = "Dataset sufficient. Ready for retraining."
            return True

    return False


# ============================================
# MAIN CORE BRAIN
# ============================================

def evaluate():
    data = load_state()
    if not data:
        return

    # ============================================
    # PRIORITY 1 — FAILURE DETECTION (HIGHEST)
    # ============================================
    failures = detect_failures()

    if failures:
        data["system_health"] = "attention"
        data["autonomous_decision"] = "system_attention"
        data["autonomous_message"] = "System issue detected. Check failures log."
        data["last_decision_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")

        log_failures(failures)
        save_state(data)

        print("System issues detected:")
        for f in failures:
            print(" -", f)
        return
    else:
        data["system_health"] = "stable"

    # ============================================
    # PRIORITY 2 — PROJECT INTELLIGENCE
    # ============================================
    handled = project_intelligence(data)
    if handled:
        data["last_decision_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        save_state(data)
        print("Project intelligence updated.")
        return

    # ============================================
    # PRIORITY 3 — ENGINEERING HEALTH
    # ============================================
    runtime = data.get("session_runtime_min", 0)
    dirty = data.get("git_dirty_minutes", 0)
    stale_days = data.get("step_stale_days", 0)

    decision = "continue"
    message = "System stable. Continue."

    if runtime > 140:
        decision = "suggest_break"
        message = "Long session detected. Take 5 min reset."

    elif dirty > 60:
        decision = "suggest_commit"
        message = "Safe checkpoint recommended."

    elif stale_days >= 4:
        decision = "review_direction"
        message = "Same step too long. Review direction."

    data["autonomous_decision"] = decision
    data["autonomous_message"] = message
    data["last_decision_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    save_state(data)


if __name__ == "__main__":
    evaluate()
    print("Autonomous decision updated.")