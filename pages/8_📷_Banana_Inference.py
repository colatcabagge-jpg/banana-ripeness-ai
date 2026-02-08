import json
from pathlib import Path
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Banana Ripeness AI | Production",
    layout="wide"
)

st.title("🍌 Banana Ripeness Detection")
st.caption("Production inference using trained CVLab model")
st.divider()

# ----------------------------------
# PATHS
# ----------------------------------
PROJECT_ROOT = Path.cwd()
REGISTRY_PATH = Path("registry/model_registry.json")
MODELS_DIR = Path("models")

# ----------------------------------
# VERIFY PROJECT ROOT
# ----------------------------------
if PROJECT_ROOT.name != "banana-ripeness-ai":
    st.error("❌ Wrong working directory")
    st.code(str(PROJECT_ROOT))
    st.stop()

st.caption(f"📂 Running from: `{PROJECT_ROOT}`")

# ----------------------------------
# LOAD REGISTRY
# ----------------------------------
if not REGISTRY_PATH.exists():
    st.error("❌ model_registry.json missing")
    st.stop()

registry = json.loads(REGISTRY_PATH.read_text())
production_exp = registry.get("production_model")

if not production_exp:
    st.warning("⚠️ No production model set yet")
    st.stop()

model_path = MODELS_DIR / f"model_{production_exp}.keras"

# ----------------------------------
# FAILSAFE MODEL CHECK
# ----------------------------------
if not model_path.exists():
    st.error("❌ Production model not found")
    st.code(str(model_path))
    st.stop()

# ----------------------------------
# LOAD MODEL
# ----------------------------------
@st.cache_resource
def load_model_safe(path):
    return tf.keras.models.load_model(path)

model = load_model_safe(model_path)

# IMPORTANT: correct class order (same as training)
from src.utils import CLASS_NAMES

IMG_SIZE = (224, 224)

# ----------------------------------
# PREPROCESS (MATCH TRAINING EXACTLY)
# ----------------------------------
def preprocess(img):
    img = img.convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32)
    arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)
    return np.expand_dims(arr, axis=0)

# ----------------------------------
# PREDICT
# ----------------------------------
def predict(img):
    preds = model.predict(preprocess(img), verbose=0)[0]
    idx = int(np.argmax(preds))
    label = CLASS_NAMES[idx]
    confidence = float(preds[idx])
    return label, confidence, preds

# ----------------------------------
# SHELF LIFE LOGIC
# ----------------------------------
def shelf_life(label):
    mapping = {
        "unripe": 5,
        "ripe": 2,
        "overripe": 1,
        "rotten": 0
    }
    return mapping.get(label, 0)

def recommendation(label):
    return {
        "unripe": "Keep at room temperature. Not ready yet.",
        "ripe": "Perfect to eat now. Consume soon.",
        "overripe": "Use immediately for smoothies or baking.",
        "rotten": "Not safe for consumption.",
    }[label]

# ----------------------------------
# UI INPUT
# ----------------------------------
col1, col2 = st.columns(2)

with col1:
    uploaded = st.file_uploader("Upload banana image", type=["jpg","jpeg","png"])

with col2:
    captured = st.camera_input("Take photo")

img = None
if uploaded:
    img = Image.open(uploaded)
elif captured:
    img = Image.open(captured)

# ----------------------------------
# INFERENCE DISPLAY
# ----------------------------------
if img:
    st.divider()
    st.subheader("🧠 Prediction Result")

    c1, c2 = st.columns([1,1])

    with c1:
        st.image(img, caption="Input Image", use_container_width=True)

    label, conf, raw = predict(img)

    with c2:
        st.markdown(f"## 🏷️ {label.upper()}")
        st.progress(min(conf,1.0))
        st.write(f"**Confidence:** {conf*100:.2f}%")

        st.divider()
        st.subheader("📊 Class Probabilities")

        for i, cname in enumerate(CLASS_NAMES):
            st.write(f"**{cname}**")
            st.progress(float(raw[i]))

        st.divider()
        days = shelf_life(label)
        st.metric("Estimated shelf life", f"{days} days")
        st.info(recommendation(label))

# ----------------------------------
# FOOTER
# ----------------------------------
st.divider()
st.caption(f"🚀 Using production model: `{model_path.name}`")