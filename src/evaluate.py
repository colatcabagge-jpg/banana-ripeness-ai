import tensorflow as tf
from tensorflow import keras
from src.utils import TEST_DIR, CLASS_NAMES, IMG_SIZE, BATCH_SIZE

def main():
    test_ds = keras.utils.image_dataset_from_directory(
        TEST_DIR,
        labels="inferred",
        label_mode="categorical",
        class_names=CLASS_NAMES,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    model = keras.models.load_model("models/banana_ripeness_model.keras")
    loss, acc = model.evaluate(test_ds)

    print(f"✅ Test Accuracy: {acc*100:.2f}%")
    print(f"✅ Test Loss: {loss:.4f}")

if __name__ == "__main__":
    main()
