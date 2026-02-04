import json
from pathlib import Path
import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Model Comparison | CVLab", layout="wide")

REGISTRY_PATH = Path("registry/model_registry.json")
OUTPUTS_DIR = Path("outputs")

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
best_exp_id = registry.get("best_model")
production_exp_id = registry.get("production_model")

if not models:
    st.warning("⚠️ No models registered yet.")
    st.stop()

# -----------------------------
# Header
# -----------------------------
st.title("🧪 Model Comparison Dashboard")
st.caption("Compare experiments and evaluate performance")
st.divider()

# -----------------------------
# Models Table
# -----------------------------
st.subheader("📋 Registered Models")

table_data = []
for m in models:
    table_data.append({
        "Experiment ID": m["exp_id"],
        "Accuracy (%)": round(get_accuracy(m) * 100, 2),
        "Mode": m["mode"],
        "Member": m["member"],
        "Best": "🏆" if m["exp_id"] == best_exp_id else "",
        "Production": "🚀" if m["exp_id"] == production_exp_id else "",
    })

df = pd.DataFrame(table_data)
st.dataframe(df, use_container_width=True)

# -----------------------------
# Accuracy Chart
# -----------------------------
st.subheader("📊 Accuracy Comparison")
chart_df = df.set_index("Experiment ID")[["Accuracy (%)"]]
st.bar_chart(chart_df)

st.divider()

# -----------------------------
# Experiment Deep Dive
# -----------------------------
st.subheader("🔍 Experiment Deep Dive")

selected_exp = st.selectbox(
    "Select Experiment",
    [m["exp_id"] for m in models]
)

selected_model = next(m for m in models if m["exp_id"] == selected_exp)
exp_output_dir = OUTPUTS_DIR / selected_exp

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Metrics")
    st.metric(
        "Validation Accuracy",
        f"{get_accuracy(selected_model) * 100:.2f}%"
    )
    st.write(f"**Mode:** {selected_model['mode']}")
    st.write(f"**Member:** {selected_model['member']}")

    if selected_exp == production_exp_id:
        st.success("🚀 Production model")
    elif selected_exp == best_exp_id:
        st.info("🏆 Best-performing model")

with col2:
    st.markdown("### 📉 Training Curves")

    acc_plot = exp_output_dir / "accuracy_plot.png"
    loss_plot = exp_output_dir / "loss_plot.png"

    if acc_plot.exists():
        st.image(acc_plot, caption="Accuracy Curve", use_container_width=True)
    else:
        st.warning("Accuracy plot not found")

    if loss_plot.exists():
        st.image(loss_plot, caption="Loss Curve", use_container_width=True)
    else:
        st.warning("Loss plot not found")

st.divider()

# -----------------------------
# Summary
# -----------------------------
summary_file = exp_output_dir / "summary.md"
metrics_file = exp_output_dir / "metrics.txt"

st.subheader("📝 Experiment Summary")

if summary_file.exists():
    st.markdown(summary_file.read_text())
else:
    st.info("No summary available.")

if metrics_file.exists():
    with st.expander("📄 Raw Metrics"):
        st.code(metrics_file.read_text())
