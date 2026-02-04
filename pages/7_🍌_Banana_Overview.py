import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Banana Overview | CVLab", layout="wide")

REGISTRY_PATH = Path("registry/model_registry.json")

# -----------------------------
# Helpers (FAILSAFE)
# -----------------------------
def get_accuracy(m):
    return float(m.get("val_accuracy", 0.0))

# -----------------------------
# Header
# -----------------------------
st.title("🍌 Banana Ripeness Project Overview")
st.caption("Project status and best-performing models")
st.divider()

# -----------------------------
# Load registry
# -----------------------------
if not REGISTRY_PATH.exists():
    st.error("❌ Model registry not found.")
    st.stop()

registry = json.loads(REGISTRY_PATH.read_text())
models = registry.get("models", [])

if not models:
    st.warning("⚠️ No models trained yet.")
    st.stop()

# -----------------------------
# Best Model Stats
# -----------------------------
best_acc = max(get_accuracy(m) for m in models)

st.subheader("🏆 Best Model Performance")
st.metric("Best Validation Accuracy", f"{best_acc * 100:.2f}%")

st.divider()

# -----------------------------
# Project Notes
# -----------------------------
st.markdown(
    """
This project uses **MobileNetV2** with transfer learning to classify banana ripeness
into four categories:

- Unripe
- Ripe
- Overripe
- Rotten

The system supports **experiment tracking**, **model comparison**, and
**production-grade inference** across multiple laptops.
"""
)
