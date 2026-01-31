import json
from pathlib import Path
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Model Comparison | CVLab", layout="wide")

# -----------------------------
# Paths
# -----------------------------
REGISTRY_PATH = Path("registry/model_registry.json")
OUTPUTS_DIR = Path("outputs")

# -----------------------------
# Load registry
# -----------------------------
if not REGISTRY_PATH.exists():
    st.error("❌ Model registry not found.")
    st.stop()

with open(REGISTRY_PATH, "r") as f:
    registry = json.load(f)

models = registry.get("models", [])
best_model = registry.get("best_model")
production_model = registry.get("production_model")

if not models:
    st.warning("⚠️ No models registered yet.")
    st.stop()

# -----------------------------
# Header
# -----------------------------
st.title("🧪 Model Comparison Dashboard")
st.caption("Compare experiments, evaluate performance, and support research decisions")

st.divider()

# -----------------------------
# SECTION 1 — Models Table
# -----------------------------
st.subheader("📋 Registered Models")

table_data = []
for m in models:
    table_data.append({
        "Experiment ID": m["exp_id"],
        "Accuracy": round(m["accuracy"] * 100, 2),
        "Mode": m["mode"],
        "Member": m["member"],
        "Best": "🏆" if m["path"] == best_model else "",
        "Production": "🚀" if m["path"] == production_model else ""
    })

df = pd.DataFrame(table_data)
st.dataframe(df, use_container_width=True)

# -----------------------------
# SECTION 2 — Accuracy Chart
# -----------------------------
st.subheader("📊 Accuracy Comparison")

chart_df = df[["Experiment ID", "Accuracy"]].set_index("Experiment ID")
st.bar_chart(chart_df)

st.divider()

# -----------------------------
# SECTION 3 — Experiment Deep Dive
# -----------------------------
st.subheader("🔍 Experiment Deep Dive")

exp_ids = [m["exp_id"] for m in models]
selected_exp = st.selectbox("Select Experiment", exp_ids)

selected_model = next(m for m in models if m["exp_id"] == selected_exp)
exp_output_dir = OUTPUTS_DIR / selected_exp

col1, col2 = st.columns(2)

# ---- Metrics ----
with col1:
    st.markdown("### 📈 Metrics")
    st.metric("Accuracy", f"{selected_model['accuracy']*100:.2f}%")
    st.write(f"**Mode:** {selected_model['mode']}")
    st.write(f"**Member:** {selected_model['member']}")

    if selected_model["path"] == production_model:
        st.success("🚀 This is the current production model")
    elif selected_model["path"] == best_model:
        st.info("🏆 This is the best-performing model")

# ---- Plots ----
with col2:
    st.markdown("### 📉 Training Curves")

    acc_plot = exp_output_dir / "accuracy_plot.png"
    loss_plot = exp_output_dir / "loss_plot.png"

    if acc_plot.exists():
        st.image(Image.open(acc_plot), caption="Accuracy Curve", use_container_width=True)
    else:
        st.warning("Accuracy plot not found")

    if loss_plot.exists():
        st.image(Image.open(loss_plot), caption="Loss Curve", use_container_width=True)
    else:
        st.warning("Loss plot not found")

# -----------------------------
# SECTION 4 — Summary & Notes
# -----------------------------
st.divider()
st.subheader("📝 Experiment Summary")

summary_file = exp_output_dir / "summary.md"
metrics_file = exp_output_dir / "metrics.txt"

if summary_file.exists():
    st.markdown(summary_file.read_text())
else:
    st.info("No summary file available.")

if metrics_file.exists():
    with st.expander("📄 Raw Metrics"):
        st.code(metrics_file.read_text())
