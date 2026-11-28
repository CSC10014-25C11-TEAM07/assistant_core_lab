import pytest

from ui.credit_rules import requires_advisor_approval


@pytest.mark.parametrize(
    ("credits", "expected"),
    [(0, False), (30, False), (31, True), (10**9, True)],
)
def test_credit_approval_threshold(credits, expected):
    assert requires_advisor_approval(credits) is expected


@pytest.mark.parametrize("credits", ["", "ba mươi tín chỉ", None])
def test_credit_approval_rejects_non_integer_input(credits):
    with pytest.raises(TypeError, match="credits must be an integer"):
        requires_advisor_approval(credits)