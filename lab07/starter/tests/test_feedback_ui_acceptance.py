"""Bao04 acceptance checks for F1, independent of the pending L1/L2 helpers.

History is seeded and the HTTP client is faked: these are UI state tests,
not evidence that a real chat roundtrip or feedback persistence succeeded.
"""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from ui import api_client


class FeedbackClient:
    def __init__(self):
        self.accept_feedback = True
        self.calls = []

    def healthy(self):
        return True

    def ask(self, *_args):
        raise AssertionError("Seeded-history tests must not send a chat request")

    def send_feedback(self, request_id, rating, comment=None):
        self.calls.append((request_id, rating, comment))
        return self.accept_feedback


@pytest.fixture
def feedback_app(monkeypatch):
    client = FeedbackClient()
    monkeypatch.setattr(api_client, "AssistantClient", lambda *_args, **_kwargs: client)
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "ui/app.py"))
    app.session_state["messages"] = [
        {"role": "assistant", "content": "Welcome"},
        {"role": "assistant", "content": "First answer", "request_id": "answer-one"},
        {"role": "assistant", "content": "Second answer", "request_id": "answer-two"},
    ]
    app.run()
    assert not app.exception
    return app, client


def feedback_buttons(app, label):
    return [button for button in app.button if button.label == label]


def test_both_answers_have_independent_positive_and_negative_controls(feedback_app):
    app, _client = feedback_app
    assert len(feedback_buttons(app, "👍")) == 2
    assert len(feedback_buttons(app, "👎")) == 2
    keys = [button.key for button in app.button if button.label in {"👍", "👎"}]
    assert all(keys)
    assert len(keys) == len(set(keys))


@pytest.mark.parametrize(("label", "rating"), [("👍", 1), ("👎", -1)])
def test_successful_vote_targets_correct_answer_and_hides_on_next_render(feedback_app, label, rating):
    app, client = feedback_app
    controls = feedback_buttons(app, label)
    assert controls, f"Missing {label} control"
    target_index = 0 if rating == 1 else 1
    request_id = "answer-one" if rating == 1 else "answer-two"
    controls[target_index].click().run()
    assert not app.exception
    assert client.calls == [(request_id, rating, None)]
    assert app.session_state["rated"] == {request_id}
    assert any("Thanks" in toast.value for toast in app.toast)
    # AppTest 1.39 can retain stale deltas across an internal st.rerun().
    # Inspect a clean render; immediate disappearance still requires a browser check.
    app.run()
    assert not app.exception
    assert len(feedback_buttons(app, label)) == 1, "The other answer must remain independently rateable"
    assert client.calls == [(request_id, rating, None)], "Rendering must not resubmit a vote"


def test_failed_feedback_preserves_retry_and_does_not_claim_success(feedback_app):
    app, client = feedback_app
    client.accept_feedback = False
    feedback_buttons(app, "👍")[0].click().run()
    assert not app.exception
    assert client.calls == [("answer-one", 1, None)]
    actual = {
        "marked_rated": "answer-one" in app.session_state["rated"],
        "thanks_shown": any("Thanks" in toast.value for toast in app.toast),
        "positive_controls": len(feedback_buttons(app, "👍")),
    }
    assert actual == {"marked_rated": False, "thanks_shown": False, "positive_controls": 2}
