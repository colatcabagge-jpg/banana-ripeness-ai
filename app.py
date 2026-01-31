import streamlit as st

st.set_page_config(
    page_title="CVLab",
    layout="wide"
)

st.title("🧪 CVLab Platform")
st.caption("Collaborative Computer Vision Research & Deployment Framework")

st.markdown(
    """
Welcome to **CVLab**.

👉 Use the **sidebar** to navigate:

- 📊 Home Dashboard
- 🍌 Banana Project (overview, inference, results)
- 🧪 Experiments & Model Comparison
- 📁 Documentation

This landing page is intentionally minimal.
"""
)

st.info("⬅️ Select a page from the sidebar to begin.")
