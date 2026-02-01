from pathlib import Path
from datetime import datetime
import json

from src.journal_logger import log_event

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
REGISTRY_PATH = PROJECT_ROOT / "registry" / "model_registry.json"


def generate_motivation():
    content = f"""
# Project Motivation

Food spoilage due to improper ripeness assessment causes significant
economic loss and nutritional waste, particularly in perishable fruits.
Bananas are among the most consumed fruits worldwide and exhibit rapid
ripeness transitions, making timely decision-making critical.

This project explores **computer vision–based banana ripeness detection**
as a low-cost, scalable, and explainable alternative to manual inspection.
By enabling automated ripeness classification and shelf-life estimation,
the system supports better consumption planning, storage decisions,
and waste reduction.

The broader motivation extends beyond bananas. This work establishes
a reusable computer vision research framework that can be applied to
agriculture, health, fitness, and activity understanding tasks.

Generated automatically on {datetime.now().strftime('%Y-%m-%d %H:%M')}
""".strip()

    path = DOCS_DIR / "motivation.md"
    path.write_text(content, encoding="utf-8")

    return path


def generate_overview():
    registry_info = "No models trained yet."
    if REGISTRY_PATH.exists():
        registry = json.loads(REGISTRY_PATH.read_text())
        registry_info = (
            f"{len(registry.get('models', []))} experiments logged, "
            f"best model: {registry.get('best_model')}"
        )

    content = f"""
# System Overview – CVLab Framework

CVLab is a **collaborative, experiment-driven computer vision ecosystem**
designed to support reproducible research and safe deployment workflows.

The framework enforces a strict separation between:
- **Training** (experiment creation)
- **Coding** (version-controlled system changes)
- **Inference** (production-only usage)

### Core Capabilities
- Experiment automation with unique IDs
- Model registry with production locking
- Journal-based event tracking
- IEEE-ready artifact generation
- Safe demo / LAN mode with read-only guarantees
- Automated Git versioning with health gating

### Active Project
**Project 1:** Banana Ripeness Detection & Shelf-Life Estimation  
Classes: unripe, ripe, overripe, rotten

### System State Snapshot
{registry_info}

### Reproducibility Guarantees
Every result produced by CVLab is traceable through:
- Experiment identifiers
- Journal events
- Git commit history
- Auto-generated documentation

Generated automatically on {datetime.now().strftime('%Y-%m-%d %H:%M')}
""".strip()

    path = DOCS_DIR / "overview.md"
    path.write_text(content, encoding="utf-8")

    return path


def generate_core_docs():
    DOCS_DIR.mkdir(exist_ok=True)

    motivation_path = generate_motivation()
    overview_path = generate_overview()

    log_event(
        event_type="CORE_DOCS_GENERATED",
        title="Core documentation generated",
        description="Motivation and system overview documents were auto-generated.",
        metadata={
            "motivation": str(motivation_path),
            "overview": str(overview_path),
        }
    )


if __name__ == "__main__":
    generate_core_docs()
    print("motivation.md and overview.md generated")
