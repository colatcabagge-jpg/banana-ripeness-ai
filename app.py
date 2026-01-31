import json
from pathlib import Path

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

from src.shelf_life import estimate_shelf_life
from src.utils import IMG_SIZE, CLASS_NAMES

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="Banana Ripeness Detection",
    layout="centered"
)

st.title("🍌 Banana Ripeness Detection")
st.caption("Powered by CVLab • Production Model Inference")

# -------------------------------
# Load production model
# -------------------------------
REGISTRY_PATH = Path("registry/model_registry.json")

@st.cache_resource
def load_production_model():
    if not REGISTRY_PATH.exists():
        st.error("❌ Model registry not found.")
        return None

    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    model_path = registry.get("production_model")

    if not model_path:
        st.warning("⚠️ No production model selected yet.")
        return None

    model = tf.keras.models.load_model(model_path)
    return model

model = load_production_model()

if model is None:
    st.stop()

# -------------------------------
# Helper functions
# -------------------------------
def preprocess_image(image: Image.Image):
    image = image.convert("RGB")
    image = image.resize(IMG_SIZE)
    img_array = np.array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

SUGGESTIONS = {
    "unripe": "🟡 Not ready yet. Store at room temperature.",
    "ripe": "🟢 Perfect to eat now!",
    "overripe": "🟠 Use soon for smoothies or baking.",
    "rotten": "🔴 Discard for safety."
}

# -------------------------------
# UI
# -------------------------------
st.subheader("📷 Upload or Capture Image")

uploaded_file = st.file_uploader(
    "Upload a banana image",
    type=["jpg", "jpeg", "png"]
)

camera_image = st.camera_input("Or take a photo")

image = None
if uploaded_file:
    image = Image.open(uploaded_file)
elif camera_image:
    image = Image.open(camera_image)

if image:
    st.image(image, caption="Input Image", use_container_width=True)

    with st.spinner("🔍 Analyzing ripeness..."):
        img_tensor = preprocess_image(image)
        preds = model.predict(img_tensor)[0]

    class_idx = int(np.argmax(preds))
    label = CLASS_NAMES[class_idx]
    confidence = float(preds[class_idx])

    st.divider()
    st.subheader("🧠 Prediction Result")

    st.markdown(f"### **{label.upper()}**")
    st.progress(min(confidence, 1.0))
    st.write(f"**Confidence:** {confidence * 100:.2f}%")

    days_left, advice = estimate_shelf_life(label, confidence)

    st.subheader("🕒 Estimated Shelf Life")
    st.metric("Days Remaining", f"{days_left} days")

    st.info(advice)
    st.info(SUGGESTIONS.get(label, "No suggestion available."))

else:
    st.info("Upload or capture an image to begin.")

# -------------------------------
# Footer
# -------------------------------
st.divider()
st.caption("CVLab • Experiment-driven Computer Vision Platform")
