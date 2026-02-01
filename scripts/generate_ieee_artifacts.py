import json
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

from src.journal_logger import log_event

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "registry" / "model_registry.json"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

FIG_DIR = PROJECT_ROOT / "docs" / "figures"
TABLE_DIR = PROJECT_ROOT / "docs" / "tables"
CAPTION_DIR = PROJECT_ROOT / "docs" / "captions"

for d in [FIG_DIR, TABLE_DIR, CAPTION_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# -------------------------------
# LOAD DATA
# -------------------------------

with open(REGISTRY_PATH) as f:
    registry = json.load(f)

models = registry.get("models", [])
if not models:
    raise RuntimeError("No experiments found in registry")


# -------------------------------
# TABLE 1: EXPERIMENT COMPARISON
# -------------------------------

df = pd.DataFrame(models)
df_sorted = df.sort_values(by="val_accuracy", ascending=False)

table_path = TABLE_DIR / "table_experiment_comparison.csv"
df_sorted.to_csv(table_path, index=False)

caption_1 = (
    "Table 1: Comparison of all experiments conducted in CVLab, "
    "sorted by validation accuracy."
)

(CAPTION_DIR / "table1.txt").write_text(caption_1)


# -------------------------------
# FIGURE 1: VALIDATION ACCURACY BAR
# -------------------------------

plt.figure(figsize=(10, 5))
plt.bar(df_sorted["exp_id"], df_sorted["val_accuracy"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Validation Accuracy")
plt.title("Validation Accuracy Across Experiments")
plt.tight_layout()

fig1_path = FIG_DIR / "fig_validation_accuracy.png"
plt.savefig(fig1_path)
plt.close()

caption_2 = (
    "Figure 1: Validation accuracy of different experiments conducted "
    "under DEV and FULL modes."
)

(CAPTION_DIR / "fig1.txt").write_text(caption_2)


# -------------------------------
# FIGURE 2: BEST MODEL HIGHLIGHT
# -------------------------------

best_id = registry.get("best_model")
best_row = df_sorted[df_sorted["exp_id"] == best_id]

plt.figure(figsize=(5, 5))
plt.bar(["Best Model"], best_row["val_accuracy"])
plt.ylim(0, 1)
plt.ylabel("Validation Accuracy")
plt.title("Best Performing Model")

fig2_path = FIG_DIR / "fig_best_model.png"
plt.savefig(fig2_path)
plt.close()

caption_3 = (
    f"Figure 2: Best performing model identified by CVLab registry "
    f"(Experiment ID: {best_id})."
)

(CAPTION_DIR / "fig2.txt").write_text(caption_3)


# -------------------------------
# JOURNAL ENTRY
# -------------------------------

log_event(
    event_type="DOCS_GENERATED",
    title="IEEE figures and tables generated",
    description="All IEEE-ready figures and tables were automatically generated.",
    metadata={
        "figures": [str(fig1_path), str(fig2_path)],
        "tables": [str(table_path)],
        "timestamp": datetime.now().isoformat()
    }
)

print("IEEE figures and tables generated successfully.")
