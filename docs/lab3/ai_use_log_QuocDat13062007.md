# AI Use Log - Đạt (QuocDat13062007)

| Date | Tool/model | Purpose | Prompt summary | Result | What I changed |
|---|---|---|---|---|---|
| 2026-10-20 | Claude (claude.ai), Sonnet 5.5 | H1: generate an exam-absence feature to review | Add exam-absence answers using rule H26-7.2, including tests | 5 files changed (`models.py`, `router.py`, `knowledge.py`, `service.py`, `tests/test_exam_absence.py`); `pytest` 70 passed | Applied 3 improvements: shared `_explain()` helper plus missing-rule warning, whole-word keyword matching, 2 extra tests (`pytest` 72 passed) |
| 2026-10-20 | Claude (claude.ai), Sonnet 5.5 | H1: suggest review points on its own code | Asked which parts of the generated code could be improved | Suggested duplication, substring matching, missing tests, hard-coded rule id, shared enum change | I chose, applied and ran 3 of them; the other two are listed as unfixed in the review |

Notes:
- All AI-generated feature code lives only on a temporary local branch and is not in the PR.
- The only AI-assisted content in the PR is the two report files in `docs/lab3/`.
- Other work in this PR (`knowledge.py`, `tests/test_knowledge.py`, worksheet) was written for
  Lab 3 with Claude guidance on structure; I reviewed and ran it myself.