from pathlib import Path
from datetime import datetime
import json

from src.journal_logger import log_event

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
REGISTRY_PATH = PROJECT_ROOT / "registry" / "model_registry.json"


def generate_results():
    DOCS_DIR.mkdir(exist_ok=True)

    if not REGISTRY_PATH.exists():
        raise FileNotFoundError("model_registry.json not found")

    registry = json.loads(REGISTRY_PATH.read_text())
    models = registry.get("models", [])
    best_id = registry.get("best_model")
    prod_model = registry.get("production_model")

    content = f"""
# Results

## Experiment Summary
A total of {len(models)} experiments were conducted and logged.
Each experiment was evaluated using validation accuracy.

## Best Performing Model
Best Experiment ID:
**{best_id}**

Production Model:
**{prod_model or "Not set"}**

## Quantitative Results
The following metrics were observed across experiments:
- Validation accuracy comparison
- Accuracy & loss trends across epochs

Refer to IEEE figures and tables for detailed analysis.

## Deployment Results
The production model was evaluated through the inference interface,
providing class prediction, confidence score, and shelf-life estimation.

## Limitations
- Dataset collected under controlled lighting conditions
- Performance may vary under extreme environmental variations
- Shelf-life estimation is an approximation

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}
""".strip()

    path = DOCS_DIR / "results.md"
    path.write_text(content, encoding="utf-8")

    log_event(
        event_type="RESULTS_GENERATED",
        title="Results document generated",
        description="Auto-generated results section for IEEE submission.",
        metadata={"path": str(path)}
    )


if __name__ == "__main__":
    generate_results()
    print("results.md generated")
