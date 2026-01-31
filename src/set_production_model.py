import json
import argparse
from pathlib import Path

REGISTRY_PATH = Path("registry/model_registry.json")

def set_production_model(model_path: str):
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError("Model registry not found.")

    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)

    if model_path not in [m["path"] for m in registry["models"]]:
        raise ValueError("Model path not found in registry. Train/register first.")

    registry["production_model"] = model_path

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=4)

    print(f"✅ Production model set to: {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", required=True)
    args = parser.parse_args()

    set_production_model(args.model_path)
