Before/After Refactoring – Router Module
1. Assigned Module
Module: src/assistant_core/router.py
Related tests: tests/test_router.py
Responsibility: Classify incoming user messages into an intent.
Refactoring goal: Improve readability and maintainability while preserving the existing routing behavior.
2. Before Refactoring

The original Router implements intent classification in a single function named route().

The function performs the following operations:

Converts the message to lowercase, trims surrounding whitespace, and removes trailing punctuation.
Checks whether the normalized message matches a supported greeting.
Checks whether the message contains fee or tuition.
Checks whether the message contains an office name.
Returns Intent.RULE when no earlier condition matches.

The original implementation performs text normalization directly inside route() and checks fee-related keywords with inline conditions.

Original Code
from assistant_core.models import Intent

GREETINGS = frozenset({"hi", "hello", "hey", "xin chao"})


def route(text: str, office_names: set[str]) -> Intent:
    """Determine the intent of a user message."""
    t = text.lower().strip().rstrip("?!.")

    if t in GREETINGS:
        return Intent.GREETING

    if "fee" in t or "tuition" in t:
        return Intent.FEE

    if any(name in t for name in office_names):
        return Intent.OFFICE

    return Intent.RULE

3. After Refactoring

The refactored implementation introduces two improvements:

_normalize_text() separates text normalization from intent classification.
FEE_KEYWORDS stores fee-related keywords in a named constant, making them easier to maintain.

The route() function preserves the original intent-checking order: greeting, fee, office, and default rule.

Refactored Code
from assistant_core.models import Intent

GREETINGS = frozenset({"hi", "hello", "hey", "xin chao"})
FEE_KEYWORDS = ("fee", "tuition")


def _normalize_text(text: str) -> str:
    """Normalize a message before matching its intent."""
    return text.lower().strip().rstrip("?!.")


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

4. Before/After Comparison
Aspect	Before	After
Text normalization	Performed directly inside route()	Extracted into _normalize_text()
Fee keywords	Checked with inline conditions	Stored in FEE_KEYWORDS
Routing order	Greeting, fee, office, default rule	Preserved
Office matching	Uses any() to match office names	Preserves the existing matching logic
Readability	Normalization and routing are combined	Normalization has a separate, descriptive function
Maintainability	Adding a fee keyword requires changing the condition	Fee keywords can be updated in the constant
Business logic	Classifies user intent	Continues to classify user intent
5. Verification
Syntax Check

Command:

python -m py_compile src/assistant_core/router.py


Expected result: No output when compilation succeeds.

Router Tests

Command:

python -m pytest tests/test_router.py -v


Previously observed result: 8 passed.

Full Test Suite

Command:

python -m pytest -v


Previously observed result: 25 passed.

Additional Check

Command:

git diff --check


Previously observed result: No whitespace errors reported.

These results document the test run performed after the refactoring. Run the commands again if the implementation changes.

6. Conclusion

The refactoring separates text normalization from intent classification and centralizes fee-related keywords. The intent-checking order and matching rules are preserved by design.

The existing test suite passed after the refactoring. These tests provide evidence that the implementation works for the covered cases, although they do not prove equivalence for every possible input.