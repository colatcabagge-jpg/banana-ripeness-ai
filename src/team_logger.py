from datetime import datetime
from pathlib import Path


def append_team_log(exp_id, member):
    project_root = Path(__file__).resolve().parent.parent
    log_path = project_root / "team" / "team_log.md"

    log_path.parent.mkdir(parents=True, exist_ok=True)

    log_line = (
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] "
        f"{member} ran experiment {exp_id}\n"
    )

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_line)
