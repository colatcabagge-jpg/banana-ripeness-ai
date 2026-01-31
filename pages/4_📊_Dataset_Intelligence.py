import streamlit as st
from src.dataset_analyzer import analyze_dataset
from pathlib import Path
import json

st.set_page_config(page_title="Dataset Intelligence", layout="wide")
st.title("📊 Dataset Intelligence")
st.caption("Automated dataset bias & quality analysis")

if st.button("Run Dataset Audit"):
    with st.spinner("Analyzing dataset..."):
        report = analyze_dataset()
    st.success("Dataset audit completed.")
    st.session_state["report"] = report

report = st.session_state.get("report")

if report:
    if "error" in report:
        st.error(report["error"])

    st.subheader("📌 Dataset Summary")
    st.write(f"Dataset Root: `{report.get('dataset_root', '—')}`")
    st.write(f"Total Images: **{report['total_images']}**")

    if report["class_counts"]:
        st.subheader("Class Counts")
        st.json(report["class_counts"])

    if report["imbalance_ratio"] is not None:
        st.subheader("⚖️ Imbalance Analysis")
        st.write(f"Imbalance Ratio (max/min): **{report['imbalance_ratio']}**")

    if report["warnings"]:
        st.subheader("⚠️ Warnings")
        for w in report["warnings"]:
            st.warning(w)

    plot_path = Path("outputs/dataset_audit/class_distribution.png")
    if plot_path.exists():
        st.subheader("📈 Distribution Plot")
        st.image(str(plot_path))
else:
    st.info("Run dataset audit to view analysis.")
