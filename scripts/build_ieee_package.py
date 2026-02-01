import zipfile
from pathlib import Path
from datetime import datetime
import shutil
import json

from src.journal_logger import log_event


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
REGISTRY_PATH = PROJECT_ROOT / "registry" / "model_registry.json"
OUTPUT_ZIP = PROJECT_ROOT / "docs" / "CVLab_IEEE_Submission.zip"


def build_ieee_package():
    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:

        # --- Add figures, tables, captions ---
        for folder in ["figures", "tables", "captions"]:
            folder_path = DOCS_DIR / folder
            if folder_path.exists():
                for file in folder_path.rglob("*"):
                    zipf.write(
                        file,
                        arcname=f"{folder}/{file.name}"
                    )

        # --- Add journals ---
        for file_name in ["dev_journal.md", "journal_events.json"]:
            file_path = DOCS_DIR / file_name
            if file_path.exists():
                zipf.write(file_path, arcname=file_name)

        # --- Add registry snapshot ---
        if REGISTRY_PATH.exists():
            zipf.write(
                REGISTRY_PATH,
                arcname="model_registry.json"
            )

        # --- Add README ---
        readme_content = f"""
CVLab – IEEE Submission Package
================================

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Contents:
- figures/: All IEEE-ready figures (auto-generated)
- tables/: Experiment comparison tables
- captions/: Figure & table captions
- methodology.md: Auto-generated methodology
- results.md: Auto-generated results
- dev_journal.md: Human-readable experiment log
- journal_events.json: Machine-readable event log
- model_registry.json: Model registry snapshot

This package was generated automatically by CVLab.
No manual edits were performed.
"""
        zipf.writestr("README.txt", readme_content.strip())

    log_event(
        event_type="IEEE_PACKAGE_BUILT",
        title="IEEE submission package generated",
        description="A complete IEEE-ready submission ZIP was generated.",
        metadata={
            "zip_path": str(OUTPUT_ZIP),
        },
    )

    return OUTPUT_ZIP


if __name__ == "__main__":
    zip_path = build_ieee_package()
    print(f"IEEE package created at: {zip_path}")
