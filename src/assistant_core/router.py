
from assistant_core.models import Intent

GREETINGS = frozenset({"hi", "hello", "hey", "xin chao"})
FEE_KEYWORDS = ("fee", "tuition")


def _normalize_text(text: str) -> str:
    """Normalize a message before matching its intent."""
    return text.lower().strip().rstrip("? !.".replace(" ", ""))


def route(text: str, office_names: set[str]) -> Intent:
    """Determine the intent of a user message."""
    normalized_text = _normalize_text(text)

    if normalized_text in GREETINGS:
        return Intent.GREETING

    if any(keyword in normalized_text for keyword in FEE_KEYWORDS):
        return Intent.FEE

    if any(name in normalized_text for name in office_names):
        return Intent.OFFICE

    return Intent.RULE
