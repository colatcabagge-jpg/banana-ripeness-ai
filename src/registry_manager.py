import json
from pathlib import Path

REGISTRY_PATH = Path("registry/model_registry.json")


def load_registry():
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)


def save_registry(data):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=4)


def register_model(exp_id, model_path, accuracy, mode, member):

    registry = load_registry()

    entry = {
        "exp_id": exp_id,
        "path": str(model_path),
        "accuracy": float(accuracy),
        "mode": mode,
        "member": member
    }

    registry["models"].append(entry)

    # Auto best model update
    if registry["best_model"] is None or accuracy > max(
        [m["accuracy"] for m in registry["models"][:-1]], default=0
    ):
        registry["best_model"] = str(model_path)

    save_registry(registry)


def set_production_model(model_path):

    registry = load_registry()
    registry["production_model"] = str(model_path)
    save_registry(registry)


def get_production_model():

    registry = load_registry()
    return registry["production_model"]
