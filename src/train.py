import os
import json
import datetime
import argparse
from pathlib import Path

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from src.utils import TRAIN_DIR, VAL_DIR, CLASS_NAMES, IMG_SIZE, BATCH_SIZE, SEED


os.makedirs("models", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


# ===============================
# CONFIG + EXPERIMENT HELPERS
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
# MODEL
# ===============================

def build_model(num_classes: int):
    base = keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights="imagenet"
    )
    base.trainable = False

    inputs = keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    return keras.Model(inputs, outputs)


# ===============================
# DATASET SAMPLING
# ===============================

def sample_dataset(dataset, fraction):
    total_batches = tf.data.experimental.cardinality(dataset).numpy()
    take_batches = max(1, int(total_batches * fraction))
    return dataset.take(take_batches)


# ===============================
# MAIN
# ===============================

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="dev", choices=["dev", "full"])
    args = parser.parse_args()

    mode = args.mode.lower()

    # ===== Mode Settings =====
    if mode == "dev":
        EPOCHS = 2
        SAMPLE_FRAC = 0.3
        USE_CACHE = False
    else:
        EPOCHS = 15
        SAMPLE_FRAC = 1.0
        USE_CACHE = True

    # ===== Config =====
    config = load_member_config()
    member_name = config["member_name"]
    laptop_name = config["laptop_name"]

    exp_id = generate_experiment_id(member_name + "-" + mode)
    output_dir, model_path = prepare_experiment_environment(exp_id)

    print("\n=====================================")
    print(f" MODE: {mode.upper()}")
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

    # ===== Sampling =====
    train_ds = sample_dataset(train_ds, SAMPLE_FRAC)
    val_ds = sample_dataset(val_ds, SAMPLE_FRAC)

    AUTOTUNE = tf.data.AUTOTUNE

    if USE_CACHE:
        train_ds = train_ds.cache()

    train_ds = train_ds.prefetch(AUTOTUNE)
    val_ds = val_ds.prefetch(AUTOTUNE)

    # ===== Model =====
    model = build_model(num_classes=len(CLASS_NAMES))

    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    callbacks = [
        keras.callbacks.ModelCheckpoint(
            str(model_path),
            save_best_only=True,
            monitor="val_accuracy",
            mode="max"
        ),
        keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=3,
            restore_best_weights=True
        )
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks
    )

    # ===== Save Metrics =====
    metrics_path = output_dir / "metrics.txt"

    with open(metrics_path, "w") as f:
        f.write(f"Experiment ID: {exp_id}\n")
        f.write(f"Mode: {mode}\n")
        f.write(f"Member: {member_name}\n")
        f.write(f"Laptop: {laptop_name}\n")
        f.write(f"Train Acc: {history.history['accuracy'][-1]}\n")
        f.write(f"Val Acc: {history.history['val_accuracy'][-1]}\n")

    print("\n=====================================")
    print(" TRAINING COMPLETE")
    print("=====================================")
    print(f"Experiment: {exp_id}")
    print(f"Model Saved: {model_path}")
    print(f"Metrics Saved: {metrics_path}")
    print("=====================================\n")


if __name__ == "__main__":
    main()
