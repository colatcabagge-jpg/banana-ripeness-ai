import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Banana Results | CVLab", layout="wide")

REGISTRY_PATH = Path("registry/model_registry.json")

# -----------------------------
# Helpers (FAILSAFE)
# -----------------------------
def get_accuracy(m):
    return float(m.get("val_accuracy", 0.0))

# -----------------------------
# Load registry
# -----------------------------
if not REGISTRY_PATH.exists():
    st.error("❌ Model registry not found.")
    st.stop()

registry = json.loads(REGISTRY_PATH.read_text())
models = registry.get("models", [])

if not models:
    st.warning("⚠️ No experiment results available.")
    st.stop()

# -----------------------------
# Header
# -----------------------------
st.title("📈 Banana Model Results")
st.caption("Aggregated experiment performance")
st.divider()

# -----------------------------
# Metrics
# -----------------------------
best_acc = max(get_accuracy(m) for m in models)
avg_acc = sum(get_accuracy(m) for m in models) / len(models)

c1, c2 = st.columns(2)
c1.metric("Best Validation Accuracy", f"{best_acc * 100:.2f}%")
c2.metric("Average Validation Accuracy", f"{avg_acc * 100:.2f}%")

st.divider()

# -----------------------------
# Detailed Table
# -----------------------------
table_data = []
for m in models:
    table_data.append({
        "Experiment ID": m["exp_id"],
        "Accuracy (%)": round(get_accuracy(m) * 100, 2),
        "Mode": m["mode"],
        "Member": m["member"],
    })

st.dataframe(table_data, use_container_width=True)
