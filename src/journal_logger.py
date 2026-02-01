import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


# -------------------------------------------------
# INTERNAL HELPERS
# -------------------------------------------------

def _get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _journal_paths():
    root = _get_project_root()
    return {
        "md": root / "docs" / "dev_journal.md",
        "json": root / "docs" / "journal_events.json",
    }


def _ensure_files():
    paths = _journal_paths()
    paths["md"].parent.mkdir(parents=True, exist_ok=True)

    if not paths["md"].exists():
        paths["md"].write_text("# CVLab Development Journal\n\n")

    if not paths["json"].exists():
        paths["json"].write_text("[]")


# -------------------------------------------------
# PUBLIC API (PURE LOGGER)
# -------------------------------------------------

def log_event(
    event_type: str,
    title: str,
    description: str,
    metadata: Dict[str, Any] = None,
):
    """
    Central journal logger for CVLab.
    PURE FUNCTION: no git, no side effects beyond logging.
    """

    _ensure_files()
    paths = _journal_paths()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    event = {
        "timestamp": timestamp,
        "event_type": event_type,
        "title": title,
        "description": description,
        "metadata": metadata or {},
    }

    # JSON (for website)
    events = json.loads(paths["json"].read_text())
    events.append(event)
    paths["json"].write_text(json.dumps(events, indent=2))

    # Markdown (for IEEE / GitHub)
    with open(paths["md"], "a", encoding="utf-8") as f:
        f.write(f"## [{timestamp}] {title}\n\n")
        f.write(f"{description}\n\n")

        if metadata:
            f.write("**Details:**\n")
            for k, v in metadata.items():
                f.write(f"- {k}: {v}\n")
            f.write("\n")

        f.write("---\n\n")
