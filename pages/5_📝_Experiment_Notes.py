import json
from pathlib import Path
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Experiment Notes | CVLab", layout="wide")

OUTPUTS_DIR = Path("outputs")

st.title("📝 Experiment Tagging & Notes")
st.caption("Human insights, decisions, and reasoning for every experiment")

st.divider()

# -----------------------------
# Load experiments
# -----------------------------
if not OUTPUTS_DIR.exists():
    st.error("❌ No experiments found.")
    st.stop()

exp_ids = sorted([p.name for p in OUTPUTS_DIR.iterdir() if p.is_dir()])

if not exp_ids:
    st.warning("⚠️ No experiments available.")
    st.stop()

selected_exp = st.selectbox("Select Experiment", exp_ids)

exp_dir = OUTPUTS_DIR / selected_exp
notes_file = exp_dir / "notes.json"

# -----------------------------
# Load existing notes
# -----------------------------
notes = {
    "tags": [],
    "summary": "",
    "observations": "",
    "issues": "",
    "next_steps": "",
    "last_updated": ""
}

if notes_file.exists():
    with open(notes_file, "r") as f:
        notes.update(json.load(f))

# -----------------------------
# UI
# -----------------------------
st.subheader(f"🧪 Experiment: `{selected_exp}`")

tags = st.text_input(
    "🏷️ Tags (comma separated)",
    value=", ".join(notes["tags"]),
    help="e.g. baseline, dev, imbalance, cpu-only"
)

summary = st.text_area(
    "🧠 Experiment Summary",
    value=notes["summary"],
    height=120
)

observations = st.text_area(
    "🔍 Observations",
    value=notes["observations"],
    height=120
)

issues = st.text_area(
    "⚠️ Issues / Limitations",
    value=notes["issues"],
    height=100
)

next_steps = st.text_area(
    "➡️ Next Steps",
    value=notes["next_steps"],
    height=100
)

# -----------------------------
# Save button
# -----------------------------
if st.button("💾 Save Notes"):
    new_notes = {
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "summary": summary,
        "observations": observations,
        "issues": issues,
        "next_steps": next_steps,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(notes_file, "w") as f:
        json.dump(new_notes, f, indent=4)

    st.success("✅ Notes saved successfully")

st.divider()

# -----------------------------
# Preview
# -----------------------------
if notes_file.exists():
    st.subheader("📄 Notes Preview (Journal Style)")
    st.markdown(f"**Last Updated:** {notes.get('last_updated','')}")
    st.markdown(f"**Tags:** {', '.join(notes.get('tags', []))}")
    st.markdown("### Summary")
    st.markdown(notes.get("summary", ""))
    st.markdown("### Observations")
    st.markdown(notes.get("observations", ""))
    st.markdown("### Issues")
    st.markdown(notes.get("issues", ""))
    st.markdown("### Next Steps")
    st.markdown(notes.get("next_steps", ""))
