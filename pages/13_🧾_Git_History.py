import streamlit as st
import subprocess
from datetime import datetime

from src.system_health import check_system_health
from src.git_auto import safe_checkpoint_push
from src.journal_logger import log_event


# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="Git History",
    layout="wide"
)

st.title("🧾 Git Commit History")
st.caption(
    "This page shows the complete Git commit history of the CVLab project. "
    "All changes — code, experiments, documentation — are automatically "
    "committed and pushed to GitHub."
)

st.markdown("---")


# -------------------------------
# SYSTEM SAFETY CONTROLS
# -------------------------------

st.header("🔐 Repository Safety Controls")

if "health_result" not in st.session_state:
    st.session_state.health_result = None

# ---- Health Check Button ----
if st.button("🔍 Check System Health"):
    result = check_system_health()
    st.session_state.health_result = result

    log_event(
        event_type="SYSTEM_HEALTH_CHECK",
        title="System health check executed",
        description="Local CI-style system integrity audit performed.",
        metadata=result
    )

health = st.session_state.health_result

# ---- Health Status Display ----
if health:
    if health["status"] == "HEALTHY":
        st.success(
            f"🟢 System HEALTHY — {health['checks_passed']} checks passed"
        )

        # ---- Safe Checkpoint Push ----
        if st.button("🔘 Push Safe Checkpoint"):
            try:
                commit_msg = safe_checkpoint_push(
                    reason="stable verified project state"
                )

                st.success("✅ Repository safely committed and pushed to GitHub")

                log_event(
                    event_type="CHECKPOINT_PUSH_COMPLETED",
                    title="Safe checkpoint push completed",
                    description="All uncommitted changes were safely saved and pushed.",
                    metadata={"commit_message": commit_msg}
                )

            except Exception as e:
                st.error("❌ Git push failed")
                st.exception(e)

    else:
        st.error("🔴 SYSTEM STATUS: ISSUES FOUND")
        st.warning("Git push is blocked until issues are resolved.")

        st.markdown("### ❌ Detected Issues")
        for idx, issue in enumerate(health["issues"], 1):
            st.markdown(f"{idx}. {issue}")

st.markdown("---")


# -------------------------------
# HELPER FUNCTION
# -------------------------------

def get_git_log():
    """
    Returns git log as list of dicts:
    hash, author, date, message
    """
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--pretty=format:%h|%an|%ad|%s",
                "--date=iso"
            ],
            capture_output=True,
            text=True,
            check=True
        )
    except Exception as e:
        st.error("Unable to read git history.")
        st.exception(e)
        return []

    commits = []
    for line in result.stdout.splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({
                "hash": parts[0],
                "author": parts[1],
                "date": parts[2],
                "message": parts[3],
            })
    return commits


# -------------------------------
# LOAD GIT DATA
# -------------------------------

commits = get_git_log()

if not commits:
    st.warning("No git commits found.")
    st.stop()


# -------------------------------
# FILTERS
# -------------------------------

authors = sorted({c["author"] for c in commits})
selected_authors = st.multiselect(
    "Filter by author",
    options=authors,
    default=authors
)

filtered_commits = [
    c for c in commits if c["author"] in selected_authors
]

st.markdown("---")


# -------------------------------
# COMMIT TIMELINE
# -------------------------------

st.header("📜 Commit Timeline")

for c in filtered_commits:
    with st.expander(
        f"{c['date']} — {c['message']}",
        expanded=False
    ):
        st.markdown(f"**Commit Hash:** `{c['hash']}`")
        st.markdown(f"**Author:** {c['author']}")
        st.markdown(f"**Timestamp:** {c['date']}")
        st.markdown(f"**Message:** {c['message']}")
