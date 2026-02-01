import json
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCS_DIR = PROJECT_ROOT / "docs"
REGISTRY_PATH = PROJECT_ROOT / "registry" / "model_registry.json"


def run(cmd):
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check_system_health():
    """
    Runs a full local system health audit.

    Returns:
        {
          "status": "HEALTHY" | "ISSUES_FOUND",
          "issues": [list of strings],
          "checks_passed": int,
          "checks_failed": int
        }
    """
    issues = []
    passed = 0
    failed = 0

    # -------------------------------------------------
    # 1. Git integrity checks (CORRECTED)
    # -------------------------------------------------

    # Basic git availability / status
    code, out, err = run("git status --porcelain")
    if code == 0:
        passed += 1
    else:
        failed += 1
        issues.append("Git repository status check failed")

    # Detect REAL merge conflicts (unmerged paths only)
    # UU, AA, DD indicate unresolved conflicts
    if any(
        marker in out
        for marker in ["UU ", "AA ", "DD "]
    ):
        failed += 1
        issues.append("Unresolved merge conflict detected")
    else:
        passed += 1

    # -------------------------------------------------
    # 2. Registry integrity
    # -------------------------------------------------

    if not REGISTRY_PATH.exists():
        failed += 1
        issues.append("model_registry.json is missing")
    else:
        try:
            registry = json.loads(REGISTRY_PATH.read_text())
            passed += 1

            prod = registry.get("production_model")
            if prod:
                prod_path = PROJECT_ROOT / prod
                if not prod_path.exists():
                    failed += 1
                    issues.append(
                        f"Production model file not found: {prod}"
                    )
                else:
                    passed += 1
        except Exception:
            failed += 1
            issues.append("model_registry.json is invalid JSON")

    # -------------------------------------------------
    # 3. Documentation sanity
    # -------------------------------------------------

    figures_dir = DOCS_DIR / "figures"
    tables_dir = DOCS_DIR / "tables"

    if figures_dir.exists():
        passed += 1
    else:
        failed += 1
        issues.append("docs/figures directory missing")

    if tables_dir.exists():
        passed += 1
    else:
        failed += 1
        issues.append("docs/tables directory missing")

    # -------------------------------------------------
    # 4. Journal sanity
    # -------------------------------------------------

    journal_json = DOCS_DIR / "journal_events.json"
    if journal_json.exists():
        try:
            json.loads(journal_json.read_text())
            passed += 1
        except Exception:
            failed += 1
            issues.append("journal_events.json is corrupted")
    else:
        failed += 1
        issues.append("journal_events.json missing")

    # -------------------------------------------------
    # FINAL STATUS
    # -------------------------------------------------

    status = "HEALTHY" if failed == 0 else "ISSUES_FOUND"

    return {
        "status": status,
        "issues": issues,
        "checks_passed": passed,
        "checks_failed": failed,
    }
