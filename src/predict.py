import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from src.utils import CLASS_NAMES, IMG_SIZE

MODEL_PATH = "models/banana_ripeness_model.keras"

def predict_image(image_path: str):
    model = keras.models.load_model(MODEL_PATH)

    img = Image.open(image_path).convert("RGB")
    img = img.resize(IMG_SIZE)
    x = np.array(img, dtype=np.float32)
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x, verbose=0)[0]
    idx = int(np.argmax(preds))
    label = CLASS_NAMES[idx]
    confidence = float(preds[idx])

    return label, confidence

if __name__ == "__main__":
    path = input("Enter image path: ").strip()
    label, conf = predict_image(path)
    print(f"Prediction: {label} ({conf*100:.2f}%)")
