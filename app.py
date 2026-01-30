import numpy as np
import streamlit as st
from PIL import Image
import tensorflow as tf
from tensorflow import keras

CLASS_NAMES = ["unripe", "ripe", "overripe", "rotten"]
IMG_SIZE = (224, 224)
MODEL_PATH = "models/banana_ripeness_model.keras"

SUGGESTIONS = {
    "unripe": "⏳ Not ready yet. Keep at room temperature for 2–3 days.",
    "ripe": "✅ Perfect to eat now!",
    "overripe": "🥤 Best for milkshake/smoothie. Eat soon.",
    "rotten": "❌ Avoid eating. Discard if smell/mold is present."
}

@st.cache_resource
def load_model():
    return keras.models.load_model(MODEL_PATH)

def preprocess(img: Image.Image):
    img = img.convert("RGB").resize(IMG_SIZE)
    x = np.array(img, dtype=np.float32)
    x = np.expand_dims(x, axis=0)
    return x

st.set_page_config(page_title="Banana Ripeness AI", page_icon="🍌", layout="centered")

st.title("🍌 Banana Ripeness Detection AI")
st.write("Upload a banana image and get ripeness stage + suggestion.")

uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", use_container_width=True)

    if not tf.io.gfile.exists(MODEL_PATH):
        st.error("Model not found. Train first using: python -m src.train")
    else:
        model = load_model()
        x = preprocess(img)
        preds = model.predict(x, verbose=0)[0]
        idx = int(np.argmax(preds))
        label = CLASS_NAMES[idx]
        confidence = float(preds[idx])

        st.subheader(f"Prediction: **{label.upper()}**")
        st.progress(min(confidence, 1.0))
        st.write(f"Confidence: **{confidence*100:.2f}%**")
        st.info(SUGGESTIONS[label])
