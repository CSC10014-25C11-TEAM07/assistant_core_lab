"""UI logic without Streamlit, so it can be unit-tested."""

from __future__ import annotations

import re

from ui.api_client import ChatResult

WELCOME = (
    "Hi! I can answer questions about fees, offices and the student handbook. "
    "Try: “Can I register my thesis with 118 credits?”"
)
EXAMPLES = [
    "Can I register my thesis with 118 credits?",
    "Tuition for 18 credits and 2 retake",
    "Where is the library?",
    "I lost my student card",
]


def validate_input(text: str) -> str | None:
    """Return an error message for bad input, or None if it is fine."""
    t = text.strip()
    if not t:
        return "Please type a question."
    if len(t) > 2000:
        return "Your question is too long (max 2000 characters)."
    return None


def format_sources(sources: list[dict]) -> str:
    """'Sources: H26#5.3 — 5.3 Thesis registration' or '' if none."""
    if not sources:
        return ""
    documents = {"H26": "handbook_2026.md", "F26": "fees_2026.md", "S26": "services_2026.md"}
    base_url = "https://github.com/CSC10014-25C11-TEAM07/assistant_core_lab/blob/main/lab08/starter/data/kb/"
    citations = []
    for source in sources:
        label = f"{source['id']} — {source['title']}"
        source_id = re.fullmatch(r"(H26|F26|S26)[#-](\d+(?:\.\d+)*)", source["id"])
        if source_id:
            # Legacy handbook sources omit the section number from their title.
            heading = source["title"]
            if not heading.startswith(source_id[2] + " "):
                heading = f"{source_id[2]} {heading}"
            anchor = re.sub(r"[^\w\s-]", "", heading.lower()).replace(" ", "-")
            url = f"{base_url}{documents[source_id[1]]}#{anchor}"
            citations.append(f"[{label}]({url})")
        else:
            citations.append(label)
    return "Sources: " + "; ".join(citations)


def status_note(result: ChatResult) -> str | None:
    """A short note shown under the answer, explaining special situations."""
    if result.escalate:
        return "I could not find this in the official documents. A staff member can help: Training Office, room I.101."
    if result.degraded:
        return "Shown directly from the source document (the AI helper was unavailable)."
    return None
