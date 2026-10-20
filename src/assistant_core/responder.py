from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from .errors import ProviderError

if TYPE_CHECKING:
    from .knowledge import Rule


class Responder(Protocol):
    """Interface for replaceable rule explanation providers."""

    def explain(self, question: str, rule: Rule) -> str: ...


class TemplateResponder:
    """Format rule content without an external provider."""

    def explain(self, question: str, rule: Rule) -> str:
        return f"{rule.title}: {rule.text}"


class StubLLMResponder:
    """Simulate a provider with an explicit, deterministic failure mode."""

    def __init__(self, fail: bool = False) -> None:
        self.fail = fail

    def explain(self, question: str, rule: Rule) -> str:
        if self.fail:
            raise ProviderError("stub provider unavailable")
        return f"Based on '{rule.title}': {rule.text}"
