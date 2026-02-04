import os

DATASET_DIR = os.path.join("data", "banana_ripeness")

TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR   = os.path.join(DATASET_DIR, "valid")
TEST_DIR  = os.path.join(DATASET_DIR, "test")

CLASS_NAMES = ["unripe", "ripe", "overripe", "rotten"]

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42
