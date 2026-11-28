"""Lab 8 Part E: turn YOUR Week-7 failures into regression tests.

Write at least three tests. Each one must:
  - have a name that says what went wrong, e.g. test_empty_sources_does_not_crash_ui
  - FAIL on the old code (check by temporarily undoing your fix), and PASS after the fix.
Use the fixtures `service`, `settings` from conftest.py, or build a TestClient like tests/test_security.py.
"""
from assistant_core.models import Message


def test_example_greeting_still_works(service):
    """Example: a control case that must never break."""
    assert "Hello" in service.handle(Message(text="hi")).answer


def test_downvote_submits_optional_feedback_comment(monkeypatch):
    from streamlit.testing.v1 import AppTest

    from ui.api_client import AssistantClient

    submitted = []

    def record_feedback(self, request_id, rating, comment=None):
        submitted.append((request_id, rating, comment))
        return True

    monkeypatch.setattr(AssistantClient, "healthy", lambda self: True)
    monkeypatch.setattr(AssistantClient, "send_feedback", record_feedback)

    app = AppTest.from_file("ui/app.py")
    app.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Visit room I.102 for a replacement student card.",
            "request_id": "card-answer-1",
        }
    ]
    app.run()

    assert not app.exception
    assert len(app.text_area) == 1, "Expected a comment field before voting"

    comment = "Please tell me which documents to bring."
    app.text_area[0].input(comment).run()
    next(button for button in app.button if button.label == "👎").click().run()

    assert not app.exception
    assert submitted == [("card-answer-1", -1, comment)]

def test_thesis_answer_explains_why_118_credits_is_not_enough(service):
    result = service.handle(
        Message(text="Can I register my thesis with 118 credits?")
    )

    answer = result.answer.lower()
    assert "118" in answer, "Expected the answer to address the student's 118 credits"
    assert "120" in answer, "Expected the answer to state the 120-credit minimum"
    assert any(
        phrase in answer
        for phrase in ("below", "short", "not enough", "do not meet")
    ), "Expected a direct explanation that 118 credits does not meet the minimum"

def test_thesis_citation_links_to_handbook_section():
    import re

    from ui.logic import format_sources

    citation = format_sources(
        [{"id": "H26#5.3", "title": "5.3 Thesis registration"}]
    )

    link = re.search(r"\[[^\]\n]*H26#5\.3[^\]\n]*\]\(([^)\s]+)\)", citation)
    assert link is not None, "Expected H26#5.3 to be a clickable Markdown link"