import json
from pathlib import Path
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import os

# ----------------------------------
# Page config
# ----------------------------------
st.set_page_config(
    page_title="Banana Ripeness Inference | CVLab",
    layout="wide"
)

st.title("🍌 Banana Ripeness Detection")
st.caption("Production inference using the deployed CVLab model")
st.divider()

# ----------------------------------
# Working directory sanity check
# ----------------------------------
PROJECT_ROOT = Path.cwd()
EXPECTED = "banana-ripeness-ai"

if PROJECT_ROOT.name != EXPECTED:
    st.error("❌ CVLab is running from the wrong directory.")
    st.code(f"Current directory: {PROJECT_ROOT}")
    st.code("Expected directory name: banana-ripeness-ai")
    st.stop()

st.caption(f"📂 Running from: `{PROJECT_ROOT}`")

# ----------------------------------
# Paths
# ----------------------------------
REGISTRY_PATH = Path("registry/model_registry.json")
MODELS_DIR = Path("models")

# ----------------------------------
# Load registry
# ----------------------------------
if not REGISTRY_PATH.exists():
    st.error("❌ Model registry not found.")
    st.stop()

registry = json.loads(REGISTRY_PATH.read_text())
production_exp_id = registry.get("production_model")

if not production_exp_id:
    st.warning("⚠️ No production model is set yet.")
    st.info(
        "To enable inference:\n"
        "• Train a FULL model\n"
        "• Promote it to production\n"
        "• Or copy an existing production model here"
    )
    st.stop()

model_path = MODELS_DIR / f"model_{production_exp_id}.keras"

# ----------------------------------
# FAILSAFE: missing production model
# ----------------------------------
if not model_path.exists():
    st.error("❌ Production model file not found on this system.")
    st.code(str(model_path))
    st.info(
        "This happens when:\n"
        "• The model was trained on another laptop\n"
        "• The models/ folder was cleaned\n\n"
        "**How to fix:**\n"
        "1️⃣ Train a FULL model on this machine\n"
        "2️⃣ Or copy the production `.keras` file into `models/`\n"
        "3️⃣ Or reset production model selection"
    )
    st.stop()

# ----------------------------------
# Load model (SAFE)
# ----------------------------------
model = tf.keras.models.load_model(model_path)

CLASS_NAMES = ["overripe", "ripe", "rotten", "unripe"]
IMG_SIZE = (224, 224)

# ----------------------------------
# Helpers
# ----------------------------------
def preprocess_image(img):
    img = img.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img)
    arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)
    return np.expand_dims(arr, axis=0)

def predict(img):
    preds = model.predict(preprocess_image(img), verbose=0)[0]
    idx = int(np.argmax(preds))
    return CLASS_NAMES[idx], float(preds[idx])

def shelf_life_estimate(label, confidence):
    base = {"unripe": 5, "ripe": 2, "overripe": 1, "rotten": 0}
    return round(base[label] * confidence, 2)

def recommendation(label):
    return {
        "unripe": "Keep at room temperature. Not ready yet.",
        "ripe": "Best time to eat. Consume soon.",
        "overripe": "Use immediately for smoothies or baking.",
        "rotten": "Not safe for consumption.",
    }[label]

# ----------------------------------
# UI
# ----------------------------------
col1, col2 = st.columns(2)

with col1:
    uploaded = st.file_uploader(
        "Upload banana image",
        type=["jpg", "jpeg", "png"]
    )

with col2:
    captured = st.camera_input("Take a photo")

image = None
if uploaded:
    image = Image.open(uploaded)
elif captured:
    image = Image.open(captured)

# ----------------------------------
# Inference
# ----------------------------------
if image:
    st.divider()
    st.subheader("🧠 Prediction Result")

    st.image(image, caption="Input Image", width="stretch")

    label, confidence = predict(image)
    days_left = shelf_life_estimate(label, confidence)

    st.markdown(f"## **{label.upper()}**")
    st.progress(min(confidence, 1.0))
    st.write(f"**Confidence:** {confidence * 100:.2f}%")

    st.divider()
    st.subheader("⏳ Estimated Shelf Life")
    st.metric("Days Remaining", f"{days_left} days")

    st.info(recommendation(label))

# ----------------------------------
# Footer
# ----------------------------------
st.divider()
st.caption(f"🚀 Using production model: `{model_path.name}`")
