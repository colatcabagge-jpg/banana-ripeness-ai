import streamlit as st
from pathlib import Path
import json
import subprocess

# ============================================
# CVLAB MISSION CONTROL — FULL JARVIS OS
# ============================================

st.set_page_config(page_title="CVLab Mission Control", layout="wide")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MEMORY_FILE = PROJECT_ROOT / "cvlab_core" / "memory" / "current_state.md"
STATE_FILE = PROJECT_ROOT / "cvlab_core" / "system_state.json"

INTEL_SCRIPT = PROJECT_ROOT / "cvlab_core" / "git_check.py"
DECISION_SCRIPT = PROJECT_ROOT / "cvlab_core" / "autonomous_decision.py"
BRAIN_SCRIPT = PROJECT_ROOT / "cvlab_core" / "jarvis_brain.py"
AUTO_COMMIT_SCRIPT = PROJECT_ROOT / "cvlab_core" / "auto_commit_brain.py"

# ============================================
# ENGINE RUNNER
# ============================================

def run_engine(script_path):
    try:
        subprocess.run(
            ["python", str(script_path)],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
    except:
        pass

# Run all system brains silently
run_engine(INTEL_SCRIPT)
run_engine(DECISION_SCRIPT)
run_engine(BRAIN_SCRIPT)
run_engine(AUTO_COMMIT_SCRIPT)

# ============================================
# READ FILES
# ============================================

def read_memory():
    try:
        return MEMORY_FILE.read_text(encoding="utf-8", errors="ignore")
    except:
        return ""

def read_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

memory_text = read_memory()
state = read_state()

# ============================================
# AUTONOMOUS MESSAGE BAR
# ============================================

auto_msg = state.get("autonomous_message", "")
auto_decision = state.get("autonomous_decision", "none")

if auto_decision == "suggest_commit":
    st.warning(auto_msg)
elif auto_decision == "suggest_break":
    st.warning(auto_msg)
elif auto_decision == "review_direction":
    st.warning(auto_msg)
elif auto_decision == "continue":
    st.success(auto_msg)

# ============================================
# SECONDARY STATUS BAR
# ============================================

focus = state.get("focus_state", "stable")
fatigue = state.get("fatigue_flag", False)
commit = state.get("suggest_commit", False)
drift = state.get("drift_flag", "none")

if focus == "stable":
    st.success("System stable • running smoothly")
elif commit:
    st.warning("Safe commit recommended")
elif fatigue:
    st.warning("Long session detected • consider short reset")
elif drift != "none":
    st.warning("Focus drift detected")

# ============================================
# HEADER
# ============================================

st.title("CVLab Mission Control")
st.caption("Full Jarvis Engineering Workspace")

st.divider()

# ============================================
# MEMORY PARSER
# ============================================

def extract_section(memory, title):
    lines = memory.split("\n")
    capture = False
    result = []

    for line in lines:
        if title in line:
            capture = True
            continue
        if capture and line.startswith("#"):
            break
        if capture:
            result.append(line)

    return "\n".join(result).strip()

active_project = extract_section(memory_text, "ACTIVE PRIMARY PROJECT")
current_phase = extract_section(memory_text, "CURRENT PHASE")
next_step = extract_section(memory_text, "CURRENT ACTIVE STEP")

# ============================================
# CURRENT FOCUS
# ============================================

c1, c2 = st.columns(2)

with c1:
    st.subheader("Active Project")
    st.info(active_project)

    st.subheader("Current Phase")
    st.write(current_phase)

with c2:
    st.subheader("Next Action")
    st.success(next_step)

st.divider()

# ============================================
# SESSION STATE
# ============================================

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric("Last Session", state.get("last_session_time", "N/A"))

with s2:
    st.metric("Momentum", state.get("momentum_state", "unknown"))

with s3:
    st.metric("Session Runtime (min)", state.get("session_runtime_min", 0))

with s4:
    st.metric("Sessions", state.get("session_count", 0))

st.divider()

# ============================================
# SYSTEM INTELLIGENCE
# ============================================

i1, i2, i3, i4 = st.columns(4)

with i1:
    st.info(f"Git: {state.get('git_status','unknown')}")

with i2:
    st.info(f"Focus: {state.get('focus_state','stable')}")

with i3:
    st.info(f"Drift: {state.get('drift_flag','none')}")

with i4:
    st.info(f"Health: {state.get('system_health','stable')}")

st.divider()

# ============================================
# JARVIS ACTION PANEL
# ============================================

ACTION_FILE = PROJECT_ROOT / "cvlab_core" / "pending_action.json"

st.subheader("Jarvis Actions")

if ACTION_FILE.exists():
    try:
        with open(ACTION_FILE, "r") as f:
            action = json.load(f)

        st.warning(f"Pending Action: {action.get('title','')}")
        st.write(action.get("reason",""))

        st.code("\n".join(action.get("commands", [])))

        c1, c2 = st.columns(2)

        with c1:
            if st.button("Approve Action"):
                subprocess.run(
                    ["python", "-c",
                     "from cvlab_core.jarvis_executor import approve_action; approve_action()"]
                )
                st.rerun()

        with c2:
            if st.button("Execute Approved"):
                subprocess.run(
                    ["python", "-c",
                     "from cvlab_core.jarvis_executor import execute_action; execute_action()"]
                )
                st.rerun()

    except:
        st.info("No active actions.")
else:
    st.success("No pending actions. System calm.")

st.divider()

# ============================================
# CONTROL PANEL
# ============================================

st.subheader("Control")

b1, b2, b3, b4 = st.columns(4)

with b1:
    if st.button("Start Session"):
        st.info("Run in terminal: cvlab_start")

with b2:
    if st.button("System Status"):
        st.info("Run in terminal: cvlab_status")

with b3:
    if st.button("Close Session"):
        st.info("Run in terminal: cvlab_close")

with b4:
    if st.button("Refresh"):
        st.rerun()

st.divider()

with st.expander("System Memory"):
    st.text_area("", memory_text, height=300)

st.caption("CVLab OS — Full Jarvis Mode Active")