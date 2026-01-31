import streamlit as st

st.set_page_config(
    page_title="Documentation | CVLab",
    layout="wide"
)

st.title("📁 CVLab Documentation")
st.caption("Research methodology, system design, and reproducibility")

st.divider()

# --------------------------------------------------
# 1. Motivation
# --------------------------------------------------
with st.expander("1️⃣ Project Motivation", expanded=True):
    st.markdown(
        """
Food spoilage due to improper ripeness assessment leads to significant economic
and nutritional loss. Bananas, being highly perishable, require timely decisions
for consumption, storage, or processing.

This project explores **computer vision–based ripeness detection** as a low-cost,
scalable solution that can be deployed on consumer devices.
"""
    )

# --------------------------------------------------
# 2. System Overview
# --------------------------------------------------
with st.expander("2️⃣ System Overview (CVLab Framework)", expanded=True):
    st.markdown(
        """
CVLab is a **modular computer vision research and deployment framework** designed to:

- Train and compare models
- Track experiments reproducibly
- Register production models
- Support collaborative teams
- Deploy inference via web interfaces

This banana project serves as **Project 1**, establishing a reusable foundation
for future CV applications.
"""
    )

# --------------------------------------------------
# 3. Dataset Description
# --------------------------------------------------
with st.expander("3️⃣ Dataset Description"):
    st.markdown(
        """
- **Source:** Public Kaggle banana ripeness dataset  
- **Classes:** Unripe, Ripe, Overripe, Rotten  
- **Total Images:** ~13,000  

A dedicated Dataset Intelligence module audits:
- Class imbalance
- Distribution skew
- Data quality issues
"""
    )

# --------------------------------------------------
# 4. Model Architecture
# --------------------------------------------------
with st.expander("4️⃣ Model Architecture"):
    st.markdown(
        """
The system uses **MobileNetV2** with transfer learning:

- Pretrained on ImageNet
- Frozen backbone during initial training
- Custom classification head

This architecture balances:
- Accuracy
- Low computational cost
- Suitability for CPU-based systems
"""
    )

# --------------------------------------------------
# 5. Training Methodology
# --------------------------------------------------
with st.expander("5️⃣ Training Methodology"):
    st.markdown(
        """
Two training modes are supported:

**DEV Mode**
- Reduced dataset
- Few epochs
- Rapid iteration

**FULL Mode**
- Complete dataset
- Extended training
- Final model selection

Each run generates:
- Unique Experiment ID
- Saved metrics & plots
- Registry entry
"""
    )

# --------------------------------------------------
# 6. Evaluation Protocol
# --------------------------------------------------
with st.expander("6️⃣ Evaluation Protocol"):
    st.markdown(
        """
- Metric: Classification Accuracy
- Validation: Held-out split
- Monitoring: Accuracy & Loss curves
- Best model auto-selected via registry

All evaluation artifacts are stored for traceability.
"""
    )

# --------------------------------------------------
# 7. Reproducibility & Collaboration
# --------------------------------------------------
with st.expander("7️⃣ Reproducibility & Collaboration"):
    st.markdown(
        """
Reproducibility is ensured via:

- Git version control
- Experiment logging
- Model registry (JSON-based)
- Per-member configuration
- Team logs and progress tracking

Any team member can clone the repository and resume work immediately.
"""
    )

# --------------------------------------------------
# 8. Extension Roadmap
# --------------------------------------------------
with st.expander("8️⃣ Extension Roadmap"):
    st.markdown(
        """
The CVLab framework is designed to scale to:

- Weed detection & growth stage analysis
- Smart gym form coaching
- Cooking activity monitoring
- Multi-fruit ripeness estimation
- Real-time video inference

This project establishes the **template** for all future systems.
"""
    )

st.divider()
st.caption("CVLab — Designed for reproducible computer vision research")
