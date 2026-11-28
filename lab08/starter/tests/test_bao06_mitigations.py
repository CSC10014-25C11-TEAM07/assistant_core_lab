"""Bao06 mitigation checks, complementing Linh's Part E tests."""
from pathlib import Path

import httpx
import pytest
from streamlit.testing.v1 import AppTest

from assistant_core.knowledge import thesis_credit_shortfall
from assistant_core.llm import StubLLM
from assistant_core.rag.answerer import RagAnswerer
from assistant_core.rag.chunker import load_folder
from assistant_core.rag.index import make_index
from ui import api_client
from ui.logic import format_sources

ROOT = Path(__file__).resolve().parents[1]


def test_downvote_keeps_comment_after_failure_then_saves_it_once(monkeypatch):
    calls = []
    accepting = [False]

    def handler(request):
        import json
        if request.url.path == "/health":
            return httpx.Response(200)
        calls.append(json.loads(request.content))
        return httpx.Response(201 if accepting[0] else 503, json={})

    client = api_client.AssistantClient("http://test", transport=httpx.MockTransport(handler))
    monkeypatch.setattr(api_client, "AssistantClient", lambda *_args: client)
    app = AppTest.from_file(str(ROOT / "ui/app.py"))
    app.session_state["messages"] = [
        {"role": "assistant", "content": "Answer", "request_id": "answer-1"}
    ]
    app.run()
    app.text_area[0].input("Cần giấy tờ gì?").run()
    app.button(key="down0").click().run()
    assert not app.exception
    assert not app.session_state["rated"]
    assert app.text_area[0].value == "Cần giấy tờ gì?"
    assert app.error
    accepting[0] = True
    app.button(key="down0").click().run()
    assert not app.exception
    assert calls == [
        {"request_id": "answer-1", "rating": -1, "comment": "Cần giấy tờ gì?"}
    ] * 2
    assert any("Thanks" in toast.value for toast in app.toast)
    # Streamlit 1.39 AppTest retains removed text-area deltas after st.rerun.
    clean = AppTest.from_file(str(ROOT / "ui/app.py"))
    clean.session_state["messages"] = app.session_state["messages"]
    clean.session_state["rated"] = app.session_state["rated"]
    clean.run()
    assert not clean.exception
    assert not clean.text_area
    assert not [b for b in clean.button if b.label in ("👍", "👎")]
    assert len(calls) == 2


@pytest.mark.parametrize("llm", [None, StubLLM(), StubLLM(fail=True)])
def test_real_rag_entry_explains_thesis_shortfall(llm):
    index = make_index("bm25", load_folder(ROOT / "data/kb"))
    answer = RagAnswerer(index, llm).answer("Can I register my thesis with 118 credits?")
    assert "118" in answer.answer and "120" in answer.answer
    assert "2 credits short" in answer.answer
    assert answer.sources[0].id == "H26#5.3"


@pytest.mark.parametrize("credits", [120, 130])
def test_meeting_credit_minimum_does_not_claim_full_eligibility(credits):
    rule = "Students may register a thesis with at least 120 accumulated credits and a GPA of at least 2.0."
    assert thesis_credit_shortfall(f"thesis with {credits} credits", rule) is None


def test_shortfall_uses_the_document_threshold():
    rule = "Students may register a thesis with at least 125 accumulated credits."
    assert "7 credits short" in thesis_credit_shortfall("thesis with 118 credits", rule)


@pytest.mark.parametrize("question", ["thesis", "thesis with 118.5 credits", "thesis with -1 credits"])
def test_unclear_credit_values_do_not_create_a_shortfall_verdict(question):
    rule = "Students may register a thesis with at least 120 accumulated credits."
    assert thesis_credit_shortfall(question, rule) is None


def test_citations_support_legacy_sources_and_unknown_ids():
    citation = format_sources([{"id": "H26-5.3", "title": "Thesis registration"}])
    assert "handbook_2026.md#53-thesis-registration)" in citation
    assert format_sources([{"id": "CUSTOM#1", "title": "Custom rule"}]) == "Sources: CUSTOM#1 — Custom rule"
