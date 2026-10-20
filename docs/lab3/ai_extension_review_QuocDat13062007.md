# AI Extension Review - Đạt (QuocDat13062007)

## Feature requested
Answer exam-absence questions (e.g. "I was sick and missed the final exam, what do I do?")
using the deadline from handbook rule H26-7.2.

Before the feature, this question was routed to the wrong rule:
`H26-4.2 (Retaking a course)` instead of `H26-7.2 (Exam absence)`, because `Handbook.search()`
is a keyword-overlap baseline and the question does not contain the word "absent".

## Tool and prompt
- Tool: Claude (claude.ai), Sonnet 5.5
- Prompt: add a feature that answers exam-absence questions using the deadline from rule
  H26-7.2 in `data/handbook.json`; modify the code as needed and add tests. The prompt also
  described the current wrong result (`H26-4.2`).
- Work was done on a temporary local branch; the AI code is not part of this PR.

## What the AI changed
- `models.py`: added `Intent.EXAM_ABSENCE`.
- `router.py`: new rule for "exam" + absence words.
- `knowledge.py`: new `Handbook.get(rule_id)`.
- `service.py`: new `_exam_absence()` branch.
- `tests/test_exam_absence.py`: 4 test cases.

Result of the raw AI output: `pytest` 66 -> 70 passed, `ruff` clean on the changed files.
The wrong answer for the sample question was fixed (`H26-7.2`, "3 working days").

## Review checklist
- **Respects interfaces (route -> service -> responder)?** Mostly yes. Signatures of `route()`,
  `Handbook.search()` and `Responder.explain()` are unchanged, and the answer still goes through
  `responder.explain()` with the `ProviderError` fallback. But the AI changed the shared contract in
  `models.py` (new `Intent` value) and bypassed `search()` by looking the rule up by a hard-coded id.
- **Adds new dependencies?** No.
- **Logs user data / uses `print()`?** No. Log messages do not contain the user's text.
- **Has real tests?** Partly. The tests assert intent, source id, "3 working days" and the
  `degraded` fallback. But there were no negative cases and no test for a missing rule.

## Improvements I made

### 1. Remove duplicated try/except and log a missing rule (`service.py`)
- Problem in AI code: `_exam_absence()` and `_rule()` contained the same block (call responder,
  catch `ProviderError`, fall back to `TemplateResponder`, set `degraded=True`). Any future change
  to the fallback would need two edits. Also, if rule `H26-7.2` disappeared from the handbook the
  service silently answered "I don't know that yet".
- Before:
```python
  def _exam_absence(self, text: str) -> Response:
      rule = self.handbook.get(EXAM_ABSENCE_RULE_ID)
      if rule is None:
          return Response(answer="Sorry, I don't know that yet.", intent=Intent.UNKNOWN)

      sources = [Source(id=rule.id, title=rule.title)]
      try:
          answer = self.responder.explain(text, rule)
          return Response(answer=answer, intent=Intent.EXAM_ABSENCE, sources=sources)
      except ProviderError:
          log.warning("provider failed; using template fallback")
          answer = self.fallback.explain(text, rule)
          return Response(answer=answer, intent=Intent.EXAM_ABSENCE, sources=sources, degraded=True)
```
- After:
```python
  def _exam_absence(self, text: str) -> Response:
      rule = self.handbook.get(EXAM_ABSENCE_RULE_ID)
      if rule is None:
          log.warning("exam absence rule %s not found in handbook", EXAM_ABSENCE_RULE_ID)
          return Response(answer="Sorry, I don't know that yet.", intent=Intent.UNKNOWN)
      return self._explain(text, rule, Intent.EXAM_ABSENCE)

  def _explain(self, text: str, rule, intent: Intent) -> Response:
      sources = [Source(id=rule.id, title=rule.title)]
      try:
          answer = self.responder.explain(text, rule)
          return Response(answer=answer, intent=intent, sources=sources)
      except ProviderError:
          log.warning("provider failed; using template fallback")
          answer = self.fallback.explain(text, rule)
          return Response(answer=answer, intent=intent, sources=sources, degraded=True)
```
  `_rule()` now also calls `_explain(text, rule, Intent.RULE)`.
- Why: one fallback path to maintain and test; a missing rule now leaves a warning in the logs.

### 2. Match whole words instead of substrings (`router.py`)
- Problem in AI code: `"miss" in t` also matches "mission" and `"exam" in t` also matches
  "example", so unrelated questions could be routed to exam absence.
- Before:
```python
  ABSENCE_WORDS = ("absent", "absence", "missed", "miss", "sick", "medical")
  ...
  if "exam" in t and any(word in t for word in ABSENCE_WORDS):
      return Intent.EXAM_ABSENCE
```
- After:
```python
  import re
  ABSENCE_WORDS = frozenset({"absent", "absence", "missed", "miss", "sick", "medical"})
  ...
  words = set(re.findall(r"[a-z]+", t))
  if "exam" in words and words & ABSENCE_WORDS:
      return Intent.EXAM_ABSENCE
```
- Why: fewer false positives; the keyword set is also an immutable `frozenset`.

### 3. Add a negative test and a missing-rule test (`tests/test_exam_absence.py`)
- Problem in AI code: tests only covered happy paths, so improvements 1 and 2 would not have
  been protected.
- Before: 4 test cases, none for false positives or for a handbook without `H26-7.2`.
- After:
```python
  def test_route_no_false_positive_on_substrings():
      assert route("give me an example of the mission statement", {"library"}) is not Intent.EXAM_ABSENCE

  def test_exam_absence_rule_missing_returns_unknown():
      service = make_service(TemplateResponder())
      service.handbook = Handbook([])
      r = service.handle(Message(text="I was sick and missed the final exam"))
      assert r.intent is Intent.UNKNOWN
      assert not r.sources
```
- Why: locks in the whole-word behaviour and the `UNKNOWN` fallback path.

Result after my changes: `pytest` 72 passed. `ruff check src tests` reports only two
pre-existing issues in `__main__.py` (not related to this feature).

## Problems I noticed but did not fix
- `EXAM_ABSENCE_RULE_ID = "H26-7.2"` is still hard-coded in `service.py`.
- `Intent.EXAM_ABSENCE` changes the public contract in `models.py`, which belongs to another
  teammate. Using `Intent.RULE` and selecting the rule differently would avoid that.
  Both are the reason this code is not merged into the shared branch.

## Conclusion
The AI produced a working feature quickly and its tests passed, but passing tests did not mean the
design was good: it duplicated code, matched substrings, touched a shared module and left error
paths untested. Manual review was needed on interfaces, error handling and test coverage.