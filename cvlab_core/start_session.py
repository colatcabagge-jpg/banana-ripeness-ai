import json
from datetime import datetime
from pathlib import Path

# Root of CVLab project
ROOT = Path(__file__).resolve().parents[1]

# Memory paths
MEMORY =  ROOT / "cvlab_core" / "memory"
SESSION_LOG = MEMORY / "session_log.json"

# Ensure memory folder exists
MEMORY.mkdir(exist_ok=True)

# Current time
now = datetime.now().strftime("%Y-%m-%d %H:%M")

entry = {
    "time": now,
    "event": "session_start",
    "project": "Banana Ripeness Detection AI",
    "phase": "Real-world accuracy stabilization",
    "status": "active"
}

# Load existing log
if SESSION_LOG.exists():
    try:
        data = json.loads(SESSION_LOG.read_text())
    except:
        data = []
else:
    data = []

# Append entry
data.append(entry)

# Save
SESSION_LOG.write_text(json.dumps(data, indent=4))

print("🟢 CVLab session started and logged")