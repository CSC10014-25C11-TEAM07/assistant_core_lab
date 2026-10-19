import pytest
from pydantic import ValidationError

from assistant_core.errors import AssistantError, InvalidRequest
from assistant_core.models import Intent, Message, Response, Source


def test_message_valid():
    """Checking valid Message creation."""
    msg = Message(text="What is the tuition fee?")
    assert msg.text == "What is the tuition fee?"
    assert msg.session_id == "local" # Kiểm tra giá trị mặc định

def test_message_empty_text():
    """Checking Message raises error with empty text."""
    with pytest.raises(ValidationError) as exc_info:
        Message(text="")
    assert "String should have at least 1 character" in str(exc_info.value)

def test_message_too_long():
    """Checking Message raises for string length exception (>2000 characters)."""
    long_text = "a" * 2001
    with pytest.raises(ValidationError):
        Message(text=long_text)

def test_response_creation():
    """Check if Response is created correctly with complex data."""
    src = Source(id="H26-5.3", title="Thesis rules")
    resp = Response(
        answer="You need 120 credits.",
        intent=Intent.RULE,
        sources=[src],
        degraded=True
    )
    assert resp.answer == "You need 120 credits."
    assert resp.intent == Intent.RULE
    assert len(resp.sources) == 1
    assert resp.degraded is True

def test_custom_exceptions():
    """Check if self defined exceptions work correctly with inheritance standards."""
    with pytest.raises(AssistantError):
        raise InvalidRequest("Invalid input provided")