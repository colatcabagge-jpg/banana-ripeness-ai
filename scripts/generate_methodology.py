from pathlib import Path
from datetime import datetime
import json

from src.journal_logger import log_event

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
REGISTRY_PATH = PROJECT_ROOT / "registry" / "model_registry.json"


def generate_methodology():
    DOCS_DIR.mkdir(exist_ok=True)

    registry = {}
    if REGISTRY_PATH.exists():
        registry = json.loads(REGISTRY_PATH.read_text())

    content = f"""
# Methodology

## Project Overview
CVLab is a collaborative, experiment-driven computer vision ecosystem designed
to support reproducible research and production-ready deployment.
This study focuses on banana ripeness detection and shelf-life estimation.

## Dataset
Images are organized into four classes:
- unripe
- ripe
- overripe
- rotten

Dataset bias and imbalance are analyzed using automated dataset intelligence tools.

## Model Architecture
A MobileNetV2 backbone with transfer learning is used.
The final classification head consists of:
- Global Average Pooling
- Dropout regularization
- Dense softmax output layer

## Training Strategy
Two training modes are supported:

**DEV Mode**
- Reduced epochs
- Dataset sampling
- Laptop-safe experimentation

**FULL Mode**
- Full dataset
- Extended epochs
- Used for production candidates

Each training run produces:
- Unique experiment ID
- Saved model artifact
- Accuracy & loss plots
- Structured experiment logs

## Experiment Tracking
All experiments are logged using:
- Machine-readable journal events
- Human-readable development journal
- Git version control

## Model Registry
Models are registered automatically after training.
The registry tracks:
- Experiment ID
- Validation accuracy
- Training mode
- Contributor

Only FULL-mode models are eligible for production deployment.

## Deployment & Demo Safety
Inference is restricted to a locked production model.
Demo/LAN mode disables training and mutation actions to preserve integrity.

## Reproducibility
All results are fully traceable through:
- Experiment IDs
- Git commit history
- Journal logs
- Auto-generated artifacts

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}
""".strip()

    path = DOCS_DIR / "methodology.md"
    path.write_text(content, encoding="utf-8")

    log_event(
        event_type="METHODOLOGY_GENERATED",
        title="Methodology document generated",
        description="Auto-generated methodology section for IEEE submission.",
        metadata={"path": str(path)}
    )


if __name__ == "__main__":
    generate_methodology()
    print("methodology.md generated")
