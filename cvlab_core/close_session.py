import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MEMORY =  ROOT / "cvlab_core" / "memory"
SESSION_LOG = MEMORY / "session_log.json"

now = datetime.now().strftime("%Y-%m-%d %H:%M")

entry = {
    "time": now,
    "event": "session_end",
    "status": "saved",
    "notes": "Session closed safely"
}

# Load existing log
if SESSION_LOG.exists():
    try:
        data = json.loads(SESSION_LOG.read_text())
    except:
        data = []
else:
    data = []

data.append(entry)

SESSION_LOG.write_text(json.dumps(data, indent=4))

print("🔵 CVLab session closed and saved")