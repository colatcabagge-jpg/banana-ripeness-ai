import json
from pathlib import Path
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# ----------------------------------
# Page config
# ----------------------------------
st.set_page_config(
    page_title="Banana Ripeness Inference | CVLab",
    layout="wide"
)

st.title("🍌 Banana Ripeness Detection")
st.caption("Production inference using the currently deployed CVLab model")

st.divider()

# ----------------------------------
# Paths
# ----------------------------------
REGISTRY_PATH = Path("registry/model_registry.json")

# ----------------------------------
# Load production model
# ----------------------------------
if not REGISTRY_PATH.exists():
    st.error("❌ Model registry not found.")
    st.stop()

with open(REGISTRY_PATH, "r") as f:
    registry = json.load(f)

production_model_path = registry.get("production_model")

if not production_model_path:
    st.warning("⚠️ No production model set yet.")
    st.stop()

model = tf.keras.models.load_model(production_model_path)

CLASS_NAMES = ["overripe", "ripe", "rotten", "unripe"]
IMG_SIZE = (224, 224)

# ----------------------------------
# Helper functions
# ----------------------------------
def preprocess_image(img: Image.Image):
    img = img.convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.array(img)
    arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)
    return np.expand_dims(arr, axis=0)

def predict(img: Image.Image):
    x = preprocess_image(img)
    preds = model.predict(x, verbose=0)[0]
    idx = int(np.argmax(preds))
    return CLASS_NAMES[idx], float(preds[idx])

def shelf_life_estimate(label: str, confidence: float):
    base_days = {
        "unripe": 5,
        "ripe": 2,
        "overripe": 1,
        "rotten": 0
    }
    days = base_days[label] * confidence
    return round(days, 2)

def recommendation(label: str):
    return {
        "unripe": "Keep at room temperature. Not ready to eat yet.",
        "ripe": "Best time to eat. Consume soon.",
        "overripe": "Use immediately for smoothies or baking.",
        "rotten": "Not safe for consumption."
    }[label]

# ----------------------------------
# UI Layout
# ----------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Banana Image")
    uploaded = st.file_uploader(
        "Upload a banana image",
        type=["jpg", "jpeg", "png"]
    )

with col2:
    st.subheader("📸 Live Camera Capture")
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

    st.image(image, caption="Input Image", use_container_width=True)

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
st.caption(
    f"🚀 Using production model: `{Path(production_model_path).name}`"
)
