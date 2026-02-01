import streamlit as st
from pathlib import Path
import pandas as pd


# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="IEEE Results",
    layout="wide"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = PROJECT_ROOT / "docs" / "figures"
TABLE_DIR = PROJECT_ROOT / "docs" / "tables"
CAPTION_DIR = PROJECT_ROOT / "docs" / "captions"


# -------------------------------
# HEADER
# -------------------------------

st.title("📊 IEEE Results & Artifacts")
st.caption(
    "All figures and tables shown below are automatically generated from "
    "CVLab experiments. No manual editing or screenshots were used."
)

st.markdown("---")


# -------------------------------
# FIGURES SECTION
# -------------------------------

st.header("📈 Figures")

if not FIG_DIR.exists():
    st.warning("No figures directory found. Generate IEEE artifacts first.")
else:
    figure_files = sorted(FIG_DIR.glob("*.png"))

    if not figure_files:
        st.warning("No IEEE figures found.")
    else:
        for fig in figure_files:
            st.subheader(fig.name)
            st.image(str(fig), use_column_width=True)

            caption_file = CAPTION_DIR / fig.name.replace(".png", ".txt")
            if caption_file.exists():
                st.caption(caption_file.read_text())
            else:
                st.caption("No caption available.")

            st.markdown("---")


# -------------------------------
# TABLES SECTION
# -------------------------------

st.header("📋 Tables")

if not TABLE_DIR.exists():
    st.warning("No tables directory found.")
else:
    table_files = sorted(TABLE_DIR.glob("*.csv"))

    if not table_files:
        st.warning("No IEEE tables found.")
    else:
        for table in table_files:
            st.subheader(table.name)

            df = pd.read_csv(table)
            st.dataframe(df, use_container_width=True)

            caption_file = CAPTION_DIR / table.name.replace(".csv", ".txt")
            if caption_file.exists():
                st.caption(caption_file.read_text())
            else:
                st.caption("No caption available.")

            st.markdown("---")


# -------------------------------
# FOOTER
# -------------------------------

st.info(
    "These artifacts are journal-ready and traceable to specific experiments. "
    "They are regenerated automatically whenever experiments or models change."
)
