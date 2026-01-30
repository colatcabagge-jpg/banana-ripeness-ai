import os
import json
import datetime
from pathlib import Path

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from src.utils import TRAIN_DIR, VAL_DIR, CLASS_NAMES, IMG_SIZE, BATCH_SIZE, SEED


# Ensure core folders exist
os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


# ===============================
# 🔬 EXPERIMENT SYSTEM HELPERS
# ===============================

def load_member_config():
    config_path = Path("config/member_config.json")

    if not config_path.exists():
        raise FileNotFoundError(
            "member_config.json missing. Copy template and fill values."
        )

    with open(config_path, "r") as f:
        return json.load(f)


def generate_experiment_id(member_name):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H%M")
    return f"EXP-{timestamp}-{member_name}"


def prepare_experiment_environment(exp_id):
    output_dir = Path("outputs") / exp_id
    output_dir.mkdir(parents=True, exist_ok=True)

    model_path = Path("models") / f"model_{exp_id}.keras"

    return output_dir, model_path


# ===============================
# 🧠 MODEL
# ===============================

def build_model(num_classes: int):
    base = keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights="imagenet"
    )
    base.trainable = False  # MVP: freeze backbone

    inputs = keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = keras.Model(inputs, outputs)
    return model


# ===============================
# 🚀 MAIN TRAINING
# ===============================

def main():

    # ===== Load Config =====
    config = load_member_config()
    member_name = config["member_name"]
    laptop_name = config["laptop_name"]

    exp_id = generate_experiment_id(member_name)
    output_dir, model_path = prepare_experiment_environment(exp_id)

    print("\n=====================================")
    print(" EXPERIMENT STARTED")
    print("=====================================")
    print(f"Experiment ID: {exp_id}")
    print(f"Member: {member_name}")
    print(f"Laptop: {laptop_name}")
    print("=====================================\n")

    # ===== Dataset =====
    train_ds = keras.utils.image_dataset_from_directory(
        TRAIN_DIR,
        labels="inferred",
        label_mode="categorical",
        class_names=CLASS_NAMES,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,
        seed=SEED
    )

    val_ds = keras.utils.image_dataset_from_directory(
        VAL_DIR,
        labels="inferred",
        label_mode="categorical",
        class_names=CLASS_NAMES,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # ===== Model =====
    model = build_model(num_classes=len(CLASS_NAMES))

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    # ===== Callbacks =====
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            str(model_path),
            save_best_only=True,
            monitor="val_accuracy",
            mode="max"
        ),
        keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=5,
            restore_best_weights=True
        )
    ]

    # ===== Training =====
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=15,
        callbacks=callbacks
    )

    # ===== Save Metrics =====
    metrics_path = output_dir / "metrics.txt"

    with open(metrics_path, "w") as f:
        f.write(f"Experiment ID: {exp_id}\n")
        f.write(f"Member: {member_name}\n")
        f.write(f"Laptop: {laptop_name}\n")
        f.write(f"Final Train Accuracy: {history.history['accuracy'][-1]}\n")
        f.write(f"Final Val Accuracy: {history.history['val_accuracy'][-1]}\n")

    print("\n=====================================")
    print(" TRAINING COMPLETE")
    print("=====================================")
    print(f"Experiment: {exp_id}")
    print(f"Model Saved: {model_path}")
    print(f"Metrics Saved: {metrics_path}")
    print("=====================================\n")


if __name__ == "__main__":
    main()
