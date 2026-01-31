from pathlib import Path
from collections import Counter
import json

import matplotlib.pyplot as plt

DATASET_PATH = Path("dataset")
OUTPUT_DIR = Path("outputs/dataset_audit")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def find_dataset_root():
    """
    Detect the actual dataset root that contains train/valid/test
    """
    for p in DATASET_PATH.rglob("*"):
        if p.is_dir():
            subdirs = {d.name for d in p.iterdir() if d.is_dir()}
            if {"train", "valid", "test"}.issubset(subdirs):
                return p
    return None


def analyze_dataset():
    dataset_root = find_dataset_root()

    if dataset_root is None:
        return {
            "error": "Dataset root with train/valid/test not found.",
            "total_images": 0,
            "class_counts": {},
            "imbalance_ratio": None,
            "warnings": ["Dataset structure not detected."]
        }

    class_counts = Counter()

    for split in ["train", "valid", "test"]:
        split_path = dataset_root / split
        if not split_path.exists():
            continue

        for class_dir in split_path.iterdir():
            if class_dir.is_dir():
                count = len(
                    [f for f in class_dir.iterdir() if f.is_file()]
                )
                class_counts[class_dir.name] += count

    total_images = sum(class_counts.values())

    if total_images == 0:
        return {
            "error": "No images found in dataset.",
            "total_images": 0,
            "class_counts": {},
            "imbalance_ratio": None,
            "warnings": ["Dataset folders exist but contain no images."]
        }

    # ---------------- Plot ----------------
    plt.figure(figsize=(8, 5))
    plt.bar(class_counts.keys(), class_counts.values())
    plt.title("Dataset Class Distribution")
    plt.ylabel("Number of Images")
    plt.xlabel("Class")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "class_distribution.png")
    plt.close()

    # ---------------- Bias metrics ----------------
    max_class = max(class_counts.values())
    min_class = min(class_counts.values())
    imbalance_ratio = round(max_class / min_class, 2) if min_class > 0 else None

    report = {
        "dataset_root": str(dataset_root),
        "total_images": total_images,
        "class_counts": dict(class_counts),
        "imbalance_ratio": imbalance_ratio,
        "warnings": []
    }

    if imbalance_ratio and imbalance_ratio > 2:
        report["warnings"].append(
            f"Class imbalance detected (ratio {imbalance_ratio}:1)"
        )

    for cls, cnt in class_counts.items():
        if cnt < 500:
            report["warnings"].append(
                f"Low sample count for class '{cls}' ({cnt} images)"
            )

    with open(OUTPUT_DIR / "dataset_audit.json", "w") as f:
        json.dump(report, f, indent=4)

    return report
