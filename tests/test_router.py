
import pytest

from assistant_core.models import Intent
from assistant_core.router import route


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("hi", Intent.GREETING),
        ("hello!", Intent.GREETING),
        ("tuition for 18 credits", Intent.FEE),
        ("How much is the fee?", Intent.FEE),
        ("Where is the library?", Intent.OFFICE),
        ("Tell me about course retake rules", Intent.RULE),
    ],
)
def test_route(text: str, expected: Intent) -> None:
    office_names = {"library", "it office", "student affairs"}
    assert route(text, office_names) is expected


def test_route_greeting_ignores_case_and_spaces() -> None:
    assert route("  HELLO!  ", set()) is Intent.GREETING


def test_route_unmatched_office_defaults_to_rule() -> None:
    assert route(
        "Where is the cafeteria?",
        {"library", "it office"},
    ) is Intent.RULE
