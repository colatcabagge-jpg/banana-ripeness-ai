import tensorflow as tf
import numpy as np
from PIL import Image
from src.utils import CLASS_NAMES

MODEL_PATH = "models/model_EXP-2026-02-05-2142-kishor-full.keras"
IMAGE_PATH = "rotten.png"   # put banana image here

print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)

print("Loading image...")
img = Image.open(IMAGE_PATH).convert("RGB").resize((224, 224))

x = np.array(img, dtype=np.float32)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
x = np.expand_dims(x, axis=0)

print("Running prediction...")
pred = model.predict(x)[0]

print("\nRaw prediction vector:")
for i, p in enumerate(pred):
    print(f"{CLASS_NAMES[i]:10s}: {p:.4f}")

pred_index = int(np.argmax(pred))
print("\nPredicted index:", pred_index)
print("Predicted label:", CLASS_NAMES[pred_index])