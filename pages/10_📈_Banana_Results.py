import json
from pathlib import Path
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Banana Results | CVLab",
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
st.title("📈 Banana Ripeness Detection — Results & Analysis")
st.caption("Experimental results and performance evaluation")

st.divider()

# ----------------------------------
# 1. Evaluation Setup
# ----------------------------------
st.subheader("1️⃣ Evaluation Setup")

st.markdown(
    """
The banana ripeness classification system was evaluated using a held-out validation set.
Performance was measured using **classification accuracy**, monitored across epochs.

All experiments were conducted within the **CVLab framework**, ensuring reproducibility,
consistent preprocessing, and standardized logging.
"""
)

# ----------------------------------
# Load Registry
# ----------------------------------
if not REGISTRY_PATH.exists():
    st.error("❌ Model registry not found.")
    st.stop()

with open(REGISTRY_PATH, "r") as f:
    registry = json.load(f)

models = registry.get("models", [])
best_model_path = registry.get("best_model")
production_model_path = registry.get("production_model")

# ----------------------------------
# 2. Performance Summary
# ----------------------------------
st.subheader("2️⃣ Model Performance Summary")

if not models:
    st.warning("No trained models found.")
    st.stop()

best_acc = max(m["accuracy"] for m in models)
avg_acc = sum(m["accuracy"] for m in models) / len(models)

c1, c2, c3 = st.columns(3)

c1.metric("Best Accuracy", f"{best_acc*100:.2f}%")
c2.metric("Average Accuracy", f"{avg_acc*100:.2f}%")
c3.metric("Experiments Conducted", len(models))

# ----------------------------------
# 3. Best vs Production Model
# ----------------------------------
st.subheader("3️⃣ Best vs Production Model")

def model_name(path):
    return Path(path).name if path else "N/A"

st.markdown(
    f"""
- **Best Model:** `{model_name(best_model_path)}`
- **Production Model:** `{model_name(production_model_path)}`
"""
)

if best_model_path == production_model_path:
    st.success("The best-performing model is deployed as the production model.")
else:
    st.warning(
        "The production model differs from the best-performing model. "
        "This may be due to stability, resource, or deployment considerations."
    )

# ----------------------------------
# 4. Training Curves
# ----------------------------------
st.subheader("4️⃣ Training Curves")

# Use production model experiment
prod_exp_id = None
for m in models:
    if m["path"] == production_model_path:
        prod_exp_id = m["exp_id"]
        break

if prod_exp_id:
    exp_dir = OUTPUTS_DIR / prod_exp_id

    acc_plot = exp_dir / "accuracy_plot.png"
    loss_plot = exp_dir / "loss_plot.png"

    col1, col2 = st.columns(2)

    with col1:
        if acc_plot.exists():
            st.image(
                Image.open(acc_plot),
                caption="Accuracy vs Epochs",
                use_container_width=True
            )
        else:
            st.warning("Accuracy plot not found.")

    with col2:
        if loss_plot.exists():
            st.image(
                Image.open(loss_plot),
                caption="Loss vs Epochs",
                use_container_width=True
            )
        else:
            st.warning("Loss plot not found.")
else:
    st.warning("Production experiment data not available.")

# ----------------------------------
# 5. Interpretation
# ----------------------------------
st.subheader("5️⃣ Result Interpretation")

st.markdown(
    """
The model demonstrates **high classification accuracy**, indicating that visual features
captured by the MobileNetV2 backbone are sufficient to distinguish ripeness stages.

Rapid convergence during training suggests effective transfer learning from pretrained
ImageNet weights.

However, class imbalance in the dataset may influence confidence distribution, which is
further analyzed in the Dataset Intelligence module.
"""
 )

# ----------------------------------
# 6. Limitations & Future Work
# ----------------------------------
st.subheader("6️⃣ Limitations & Future Work")

st.markdown(
    """
**Limitations:**
- Dataset imbalance across ripeness stages
- Controlled image conditions in dataset
- Single-fruit focus (banana only)

**Future Work:**
- Class imbalance correction strategies
- Multi-fruit generalization
- Real-time video inference
- Edge-device deployment
"""
)

st.divider()
st.caption("Results generated via CVLab Experiment Framework")
