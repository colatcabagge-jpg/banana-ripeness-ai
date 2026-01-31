import json
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Banana Ripeness Overview | CVLab",
    layout="wide"
)

# ----------------------------------
# Paths
# ----------------------------------
REGISTRY_PATH = Path("registry/model_registry.json")
OUTPUTS_DIR = Path("outputs")
DATASET_PATH = Path("dataset/Banana Ripeness Classification Dataset")

# ----------------------------------
# Header
# ----------------------------------
st.title("🍌 Banana Ripeness Detection — Project Overview")
st.caption("Project 1 | Built on CVLab Research Platform")

st.divider()

# ----------------------------------
# 1. Problem Statement
# ----------------------------------
st.subheader("1️⃣ Problem Statement")

st.markdown(
    """
Banana ripeness assessment is a **critical problem** in agriculture, retail supply chains, 
and household food management. Incorrect ripeness estimation leads to:

- Premature consumption
- Food wastage
- Inefficient logistics
- Economic losses for farmers and vendors

Traditional ripeness assessment relies on **human visual inspection**, which is subjective, 
inconsistent, and not scalable.

This project proposes a **computer vision–based system** that automatically classifies 
banana ripeness from images and estimates remaining shelf life.
"""
)

# ----------------------------------
# 2. Motivation & Impact
# ----------------------------------
st.subheader("2️⃣ Motivation & Real-World Impact")

st.markdown(
    """
A reliable banana ripeness detection system can:

- Assist farmers in harvest timing
- Help retailers manage inventory
- Enable consumers to reduce food waste
- Support automation in agri-tech systems

This project is designed to be **low-cost, camera-based, and deployable** on common devices.
"""
)

# ----------------------------------
# 3. Dataset Description
# ----------------------------------
st.subheader("3️⃣ Dataset Description")

total_images = 0
if DATASET_PATH.exists():
    total_images = sum(1 for _ in DATASET_PATH.rglob("*.jpg"))

st.markdown(
    f"""
- **Dataset:** Banana Ripeness Classification Dataset  
- **Classes:** Unripe, Ripe, Overripe, Rotten  
- **Total Images:** ~{total_images}  
- **Source:** Publicly available dataset (Kaggle)

The dataset exhibits **class imbalance**, which is explicitly analyzed using CVLab’s 
Dataset Intelligence module.
"""
)

# ----------------------------------
# 4. System Architecture
# ----------------------------------
st.subheader("4️⃣ System Architecture")

st.markdown(
    """
**Pipeline Overview:**

1. Image capture (upload or webcam)
2. Preprocessing (resize, normalization)
3. Feature extraction using MobileNetV2 backbone
4. Softmax-based ripeness classification
5. Shelf-life estimation logic
6. Recommendation generation

**Platform Components:**
- Model Registry
- Experiment Tracking
- Dataset Bias Analyzer
- Production Inference UI
"""
)

# ----------------------------------
# 5. Current Results Snapshot
# ----------------------------------
st.subheader("5️⃣ attaching your best Results Snapshot")

best_acc = None
prod_model = None

if REGISTRY_PATH.exists():
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)
        prod_model = registry.get("production_model")
        if registry.get("models"):
            best_acc = max(m["accuracy"] for m in registry["models"])

col1, col2 = st.columns(2)

with col1:
    if best_acc:
        st.metric("Best Validation Accuracy", f"{best_acc*100:.2f}%")
    else:
        st.metric("Best Validation Accuracy", "N/A")

with col2:
    if prod_model:
        st.metric("Production Model", "Deployed")
    else:
        st.metric("Production Model", "Not Set")

# ----------------------------------
# 6. How to Use
# ----------------------------------
st.subheader("6️⃣ How to Use the System")

st.markdown(
    """
1. Navigate to **🍌 Banana Inference**
2. Upload an image or use webcam
3. View ripeness prediction and confidence
4. Check estimated shelf life and recommendations
5. Explore results and dataset analysis via CVLab tools
"""
)

st.divider()
st.caption("Banana Ripeness Detection — CVLab Project 1")
