import json
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="CVLab Home",
    layout="wide"
)

# ----------------------------------
# Paths
# ----------------------------------
REGISTRY_PATH = Path("registry/model_registry.json")
OUTPUTS_DIR = Path("outputs")

# ----------------------------------
# Header
# ----------------------------------
st.title("🧪 CVLab — Computer Vision Research Platform")
st.caption(
    "An end-to-end, collaborative, experiment-driven platform for computer vision projects"
)

st.divider()

# ----------------------------------
# CVLab Overview
# ----------------------------------
st.subheader("🔬 What is CVLab?")

st.markdown(
    """
CVLab is a **research-grade computer vision platform** designed to support:

- Multiple CV projects under a unified system  
- Reproducible experiments  
- Team collaboration  
- Model comparison & tracking  
- Journal-ready documentation  

Each project (e.g., Banana Ripeness Detection) is built **on top of the same lab infrastructure**.
"""
)

st.divider()

# ----------------------------------
# Platform Status
# ----------------------------------
st.subheader("📊 Platform Status")

total_experiments = len([p for p in OUTPUTS_DIR.iterdir() if p.is_dir()]) if OUTPUTS_DIR.exists() else 0
total_models = 0
best_model = None
production_model = None

if REGISTRY_PATH.exists():
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)
        total_models = len(registry.get("models", []))
        best_model = registry.get("best_model")
        production_model = registry.get("production_model")

c1, c2, c3 = st.columns(3)

c1.metric("Total Experiments", total_experiments)
c2.metric("Registered Models", total_models)

if production_model:
    c3.metric("Production Model", "SET")
else:
    c3.metric("Production Model", "NOT SET")

st.divider()

# ----------------------------------
# Projects
# ----------------------------------
st.subheader("📁 Active Projects")

st.markdown(
    """
### 🍌 Banana Ripeness Detection
- Image & webcam-based ripeness classification  
- Shelf-life estimation  
- Dataset bias analysis  
- Model comparison & tracking  

➡️ Navigate to **🍌 Banana Inference** to test the system.
"""
)

st.info(
    "Future projects (Weed Detection, Hardware Counting, Cooking Assistant, Gym Coach) "
    "will reuse this same CVLab infrastructure."
)

st.divider()

# ----------------------------------
# Navigation Guide
# ----------------------------------
st.subheader("🧭 Where to Go Next")

st.markdown(
    """
- 🧪 **Model Comparison** → Compare trained models  
- 📝 **Experiment Notes** → Add human reasoning & insights  
- 📊 **Dataset Intelligence** → Analyze bias & imbalance  
- 🍌 **Banana Inference** → Run production predictions  
- 📁 **Documentation** → Journal-ready methodology & results  
"""
)

st.divider()

st.caption("CVLab v1 — Built for reproducible computer vision research")
