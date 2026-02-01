import json
from pathlib import Path
from src.journal_logger import log_event


REGISTRY_PATH = Path("registry/model_registry.json")


def load_registry():
    if not REGISTRY_PATH.exists():
        return {
            "best_model": None,
            "production_model": None,
            "production_locked": False,
            "models": []
        }
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def save_registry(registry):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)


def update_registry(exp_id, model_path, metrics, member, mode):
    registry = load_registry()

    val_acc = metrics.get("val_accuracy")
    if val_acc is None:
        raise ValueError("metrics must contain 'val_accuracy'")

    entry = {
        "exp_id": exp_id,
        "path": str(model_path),
        "val_accuracy": float(val_acc),
        "mode": mode,
        "member": member
    }

    registry["models"].append(entry)

    # Best model = highest validation accuracy (any mode)
    best_entry = max(
        registry["models"],
        key=lambda m: m.get("val_accuracy", 0)
    )
    registry["best_model"] = best_entry["exp_id"]

    log_event(
        event_type="REGISTRY_UPDATED",
        title="Registry updated",
        description="Model registry updated after training.",
        metadata={
            "experiment_id": exp_id,
            "val_accuracy": val_acc,
            "mode": mode,
            "member": member,
        },
    )
    
    save_registry(registry)


# -------------------------------
# PRODUCTION MODEL CONTROL
# -------------------------------

def set_production_model(exp_id):
    registry = load_registry()

    if registry.get("production_locked"):
        raise RuntimeError("Production model is LOCKED. Unlock first.")

    # Find experiment
    exp = next(
        (m for m in registry["models"] if m["exp_id"] == exp_id),
        None
    )

    if exp is None:
        raise ValueError(f"Experiment {exp_id} not found in registry")

    if exp["mode"] != "full":
        raise ValueError("Only FULL mode experiments can be production")

    registry["production_model"] = exp_id

    log_event(
        event_type="PRODUCTION_SET",
        title="Production model set",
        description="A FULL experiment was set as the production model.",
        metadata={
            "experiment_id": exp_id
        },
    )
    save_registry(registry)


def lock_production():
    registry = load_registry()
    registry["production_locked"] = True

    log_event(
        event_type="PRODUCTION_LOCKED",
        title="Production model locked",
        description="Production model was locked to prevent accidental changes.",
    )

    save_registry(registry)


def unlock_production():
    registry = load_registry()
    registry["production_locked"] = False
    save_registry(registry)
