import json
from pathlib import Path
import streamlit as st
from datetime import datetime


# -------------------------------
# CONFIG
# -------------------------------

st.set_page_config(
    page_title="CVLab Journal",
    layout="wide"
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
JOURNAL_JSON = PROJECT_ROOT / "docs" / "journal_events.json"


# -------------------------------
# HELPERS
# -------------------------------

def load_events():
    if not JOURNAL_JSON.exists():
        return []
    with open(JOURNAL_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def format_time(ts: str):
    try:
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return ts


# -------------------------------
# UI
# -------------------------------

st.title("📘 CVLab Development Journal")
st.caption(
    "A complete, automatically generated timeline of all important actions "
    "performed in this project."
)

events = load_events()

if not events:
    st.warning("No journal events found yet.")
    st.stop()

# Sort newest first
events = sorted(
    events,
    key=lambda e: e.get("timestamp", ""),
    reverse=True
)

# -------------------------------
# FILTERS
# -------------------------------

event_types = sorted(
    {e["event_type"] for e in events}
)

selected_types = st.multiselect(
    "Filter by event type",
    options=event_types,
    default=event_types
)

filtered_events = [
    e for e in events if e["event_type"] in selected_types
]

st.markdown("---")

# -------------------------------
# TIMELINE
# -------------------------------

for event in filtered_events:
    with st.expander(
        f"[{event['timestamp']}] {event['title']}",
        expanded=False
    ):
        st.markdown(f"**Event Type:** `{event['event_type']}`")
        st.markdown(event["description"])

        metadata = event.get("metadata", {})
        if metadata:
            st.markdown("#### Details")
            for k, v in metadata.items():
                st.markdown(f"- **{k}**: `{v}`")
