import streamlit as st
from pathlib import Path
from scripts.build_ieee_package import build_ieee_package


st.set_page_config(
    page_title="IEEE Package",
    layout="centered"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ZIP_PATH = PROJECT_ROOT / "docs" / "CVLab_IEEE_Submission.zip"


st.title("📦 IEEE Submission Package")
st.caption(
    "Generate and download a complete IEEE-ready submission package. "
    "All contents are automatically generated and traceable."
)

st.markdown("---")

if st.button("📦 Build IEEE Package"):
    with st.spinner("Building IEEE submission package..."):
        zip_path = build_ieee_package()
    st.success("IEEE package generated successfully.")

st.markdown("---")

if ZIP_PATH.exists():
    with open(ZIP_PATH, "rb") as f:
        st.download_button(
            label="⬇️ Download IEEE Submission ZIP",
            data=f,
            file_name="CVLab_IEEE_Submission.zip",
            mime="application/zip"
        )
else:
    st.info("Package not generated yet.")
