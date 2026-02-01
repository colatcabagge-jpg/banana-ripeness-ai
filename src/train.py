import argparse
import json
from pathlib import Path

from src.journal_logger import log_event
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from src.git_auto import auto_git_commit_for_latest_event


from src.utils import (
    TRAIN_DIR,
    VAL_DIR,
    CLASS_NAMES,
    IMG_SIZE,
    BATCH_SIZE,
    SEED
)

from src.experiment_manager import ExperimentManager


# ===============================
# CONFIG
# ===============================

def load_member_config():
    config_path = Path("config/member_config.json")
    if not config_path.exists():
        raise FileNotFoundError(
            "member_config.json missing. Copy template and fill values."
        )
    with open(config_path, "r") as f:
        return json.load(f)


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
# DATASET HELPERS
# ===============================

def sample_dataset(dataset, fraction):
    total_batches = tf.data.experimental.cardinality(dataset).numpy()
    take_batches = max(1, int(total_batches * fraction))
    return dataset.take(take_batches)


# ===============================
# PLOTS
# ===============================

def save_training_plots(history, output_dir):
    plt.figure()
    plt.plot(history.history["accuracy"], label="train_accuracy")
    plt.plot(history.history["val_accuracy"], label="val_accuracy")
    plt.legend()
    plt.title("Accuracy vs Epoch")
    plt.savefig(output_dir / "accuracy_plot.png")
    plt.close()

    plt.figure()
    plt.plot(history.history["loss"], label="train_loss")
    plt.plot(history.history["val_loss"], label="val_loss")
    plt.legend()
    plt.title("Loss vs Epoch")
    plt.savefig(output_dir / "loss_plot.png")
    plt.close()


# ===============================
# MAIN
# ===============================

def main():

    # -------- CLI --------
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="dev", choices=["dev", "full"])
    args = parser.parse_args()
    mode = args.mode.lower()

    # -------- MODE CONFIG --------
    if mode == "dev":
        EPOCHS = 2
        SAMPLE_FRAC = 0.3
        USE_CACHE = False
    else:
        EPOCHS = 15
        SAMPLE_FRAC = 1.0
        USE_CACHE = True

    # -------- MEMBER CONFIG --------
    config = load_member_config()

    member_name = (
        config.get("member_name")
        or config.get("member")
        or "unknown"
    )

    # -------- EXPERIMENT START --------
    exp = ExperimentManager(
        member=member_name,
        mode=mode
    )

    print("\n=====================================")
    print(f" MODE: {mode.upper()}")
    print(f" EXPERIMENT: {exp.exp_id}")
    print(f" MEMBER: {member_name}")
    print("=====================================\n")

    # -------- DATASETS --------
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

    train_ds = sample_dataset(train_ds, SAMPLE_FRAC)
    val_ds = sample_dataset(val_ds, SAMPLE_FRAC)

    AUTOTUNE = tf.data.AUTOTUNE
    if USE_CACHE:
        train_ds = train_ds.cache()

    train_ds = train_ds.prefetch(AUTOTUNE)
    val_ds = val_ds.prefetch(AUTOTUNE)

    # -------- MODEL --------
    model = build_model(num_classes=len(CLASS_NAMES))

    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS
    )

    # -------- METRICS --------
    final_train_acc = history.history["accuracy"][-1]
    final_val_acc = history.history["val_accuracy"][-1]

    metrics = {
        "train_accuracy": float(final_train_acc),
        "val_accuracy": float(final_val_acc),
        "epochs": EPOCHS,
        "mode": mode
    }

    # -------- SAVE VIA EXPERIMENT MANAGER --------
    exp.save_model(model)
    exp.save_metrics(metrics)
    save_training_plots(history, exp.exp_dir)
    exp.save_summary()
    exp.finalize()

    log_event(
    event_type="TRAINING_COMPLETED",
    title="Training completed",
    description="Model training completed successfully.",
    metadata={
        "experiment_id": exp.exp_id,
        "mode": mode,
        "member": member_name,
        "val_accuracy": metrics.get("val_accuracy"),
        "output_dir": str(exp.exp_dir),
    },
    )
    auto_git_commit_for_latest_event()

    print("\n=====================================")
    print(" TRAINING COMPLETE")
    print("=====================================")
    print(f" EXPERIMENT: {exp.exp_id}")
    print(f" OUTPUT DIR: {exp.exp_dir}")
    print("=====================================\n")


if __name__ == "__main__":
    main()
