"""Test tuition parsing and calculation."""

import pytest

from assistant_core.errors import InvalidRequest
from assistant_core.tools import parse_credits, tuition


def test_parse_credits_with_retake() -> None:
    assert parse_credits(
        "fee for 18 credits and 2 retake"
    ) == (18, 2)


def test_parse_credits_without_retake() -> None:
    assert parse_credits("fee for 18 credits") == (18, 0)


def test_parse_credits_case_insensitive() -> None:
    assert parse_credits("Fee for 18 CREDITS and 2 RETAKE") == (18, 2)


@pytest.mark.parametrize("text", ["", "How much is tuition?", "hello"])
def test_parse_credits_missing_credits(text: str) -> None:
    with pytest.raises(InvalidRequest):
        parse_credits(text)


def test_tuition_expected_value() -> None:
    assert tuition(18, 2, 450_000, 1.5, 30) == 9_450_000


def test_tuition_without_retake() -> None:
    assert tuition(18, 0, 450_000, 1.5, 30) == 8_100_000


@pytest.mark.parametrize("credits", [0, 31, -1])
def test_tuition_rejects_invalid_credits(credits: int) -> None:
    with pytest.raises(InvalidRequest):
        tuition(credits, 0, 450_000, 1.5, 30)


def test_tuition_rejects_negative_retake() -> None:
    with pytest.raises(InvalidRequest):
        tuition(18, -1, 450_000, 1.5, 30)
