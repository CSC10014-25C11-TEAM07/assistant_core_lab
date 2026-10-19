"""Provide deterministic tools for tuition calculation."""

import re

from assistant_core.errors import InvalidRequest


def parse_credits(text: str) -> tuple[int, int]:
    """Extract regular credits and retake credits from a tuition question."""
    if not text or not text.strip():
        raise InvalidRequest("Please specify the number of credits.")

    credits_match = re.search(
        r"\b(\d+)\s*credits?\b",
        text,
        re.IGNORECASE,
    )
    retake_match = re.search(
        r"\b(\d+)\s*retake\b",
        text,
        re.IGNORECASE,
    )

    if credits_match is None:
        raise InvalidRequest("How many credits?")

    credits = int(credits_match.group(1))
    retake = int(retake_match.group(1)) if retake_match else 0

    return credits, retake


def tuition(
    credits: int,
    retake: int,
    rate: int,
    retake_multiplier: float,
    max_credits: int,
) -> int:
    """Calculate tuition using the configured rate and retake multiplier."""
    if not isinstance(credits, int) or isinstance(credits, bool):
        raise InvalidRequest("Credits must be an integer.")

    if not isinstance(retake, int) or isinstance(retake, bool):
        raise InvalidRequest("Retake credits must be an integer.")

    if not isinstance(max_credits, int) or isinstance(max_credits, bool):
        raise InvalidRequest("Maximum credits must be an integer.")

    if not 1 <= credits <= max_credits:
        raise InvalidRequest(
            f"Credits must be between 1 and {max_credits}."
        )

    if retake < 0:
        raise InvalidRequest("Retake credits cannot be negative.")

    if rate < 0:
        raise InvalidRequest("Credit rate cannot be negative.")

    if retake_multiplier < 0:
        raise InvalidRequest("Retake multiplier cannot be negative.")

    return int(credits * rate + retake * rate * retake_multiplier)