import os
from pathlib import Path
import streamlit as st
import subprocess

from scripts.generate_methodology import generate_methodology
from scripts.generate_results import generate_results


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Documentation | CVLab",
    layout="wide"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"

CVLAB_MODE = os.getenv("CVLAB_MODE", "dev").lower()
IS_DEMO_MODE = CVLAB_MODE == "demo"

st.title("📁 CVLab Documentation")
st.caption("Research methodology, system design, reproducibility, and results")

st.divider()


# --------------------------------------------------
# MANUAL REGENERATE CONTROLS
# --------------------------------------------------

if not IS_DEMO_MODE:
    with st.container():
        col1, col2 = st.columns([1, 4])

        with col1:
            if st.button("🔄 Regenerate Docs"):
                with st.spinner("Regenerating methodology and results..."):
                    generate_methodology()
                    generate_results()
                st.success("Documentation regenerated successfully.")

        with col2:
            st.caption(
                "Regenerates auto-generated Methodology and Results sections "
                "from the latest system state."
            )
else:
    st.info("🔒 Demo Mode: Documentation is read-only")

st.divider()


# --------------------------------------------------
# HELPER: LOAD MARKDOWN SAFELY
# --------------------------------------------------

def render_md(title, path: Path, expanded=False):
    with st.expander(title, expanded=expanded):
        if path.exists():
            st.markdown(path.read_text(encoding="utf-8"))
            st.caption(f"Last updated: {path.stat().st_mtime_ns}")
        else:
            st.warning("Section not available yet.")


# --------------------------------------------------
# STATIC SECTIONS (INTRODUCTORY)
# --------------------------------------------------

render_md(
    "1️⃣ Project Motivation",
    DOCS_DIR / "motivation.md",
    expanded=True
)

render_md(
    "2️⃣ System Overview (CVLab Framework)",
    DOCS_DIR / "overview.md",
    expanded=True
)


# --------------------------------------------------
# AUTO-GENERATED CORE SECTIONS
# --------------------------------------------------

render_md(
    "3️⃣ Methodology (Auto-generated)",
    DOCS_DIR / "methodology.md",
    expanded=True
)

render_md(
    "4️⃣ Results (Auto-generated)",
    DOCS_DIR / "results.md",
    expanded=True
)


# --------------------------------------------------
# SUPPORTING DOCUMENTATION
# --------------------------------------------------

render_md(
    "5️⃣ Dataset Notes",
    DOCS_DIR / "dataset_notes.md"
)

render_md(
    "6️⃣ Development Journal",
    DOCS_DIR / "dev_journal.md"
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()
st.caption(
    "CVLab — All documentation is auto-generated, version-controlled, "
    "and traceable for reproducible research."
)
