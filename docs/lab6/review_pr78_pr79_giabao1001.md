# Peer Review Report: PR #78 and PR #79 (Bao06 / Rouinz)

- **Reviewer:** Tran Gia Bao (`giabao1001` / Bao04)
- **Reviewee:** Rouinz (Bao06)
- **Reviewed Pull Requests:**
  - **PR #78:** `Lab 6: Complete individual RAG exercises` (branch `feat/lab06-individual-Rouinz`, commit `353131f`)
  - **PR #79:** `Lab 6 H3: Evaluate trailing-s normalization` (branch `experiment/lab06-h3-Rouinz`, commit `c4e23db`)
- **Review Date:** 2026-11-15
- **Tracking Issue:** #89

---

## 1. Review of PR #78 (S1 & Individual RAG Submission)

### Implementation Verification
1. **S1 Inverted Index (`lab06/practice/mini_search.py`):**
   - Function `build_index(docs)` iterates over `docs.items()`, tokenizes each document using `tokenize()`, and accumulates document IDs using `index.setdefault(word, set()).add(doc_id)`.
   - Verified against test suite: `pytest -q lab06/practice/test_mini_search.py` passed 4/4.
   - Verified against S2–S3 isolated acceptance suite: integrated cleanly with `test_search_scoring_ranking.py` (14/14 passed).
2. **A2 Grounding Check (`lab06/starter/src/assistant_core/llm.py`):**
   - `parse_draft()` enforces that non-abstaining drafts must contain at least one source ID and all source IDs must satisfy `set(draft.source_ids) <= allowed_ids`.
   - Properly raises `ProviderError("answer cites sources that were not retrieved")`.
   - Verified with `pytest -q tests/test_rag.py -k citation` (1 passed).
3. **A1 Abstention (`lab06/starter/src/assistant_core/rag/answerer.py`):**
   - Correctly guards against empty hits or `hits[0].score < self.min_score`, returning `Response(answer=ESCALATE_MSG, intent=Intent.UNKNOWN, path="abstain", escalate=True, confidence=0.0)`.
   - Prevents ungrounded LLM inference when retrieval confidence is insufficient.
4. **H1 Cases (`eval/cases.jsonl`):**
   - E21 (`S26#3`), E22 (`H26#5.4`), E23 (`F26#3`), E24 (abstain, out-of-scope), E25 (abstain, out-of-scope).
   - Notably observed that E23 is captured by the fee router rather than RAG, providing valuable insight into router-retrieval boundary interactions.
5. **H2 Reflection (`docs/lab6/h2_reflection.md`):**
   - Exactly five lines, well-structured, clearly contrasts open-book exam mechanics with closed-book memorization and highlights citation validation as the critical code-level safeguard.

---

## 2. Review of PR #79 (H3 Bonus Experiment: Trailing-s Suffix Stripping)

### Code Change Inspected
In `lab06/starter/src/assistant_core/rag/index.py`:
```python
def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"\w+", text.lower())
    return [
        token[:-1] if len(token) > 4 and token.endswith("s") else token
        for token in tokens
        if token not in STOP
    ]
```

### Independent Reproduction & Findings
1. **Target Query E14 (`"can I take 32 credits"`):**
   - Expected section: `H26#6.1` (Credit load).
   - Before normalization: `H26#7.2` (Exam absence) scores 2.086; `H26#6.1` scores 1.475.
   - After normalization: `"credits"` -> `"credit"`. However, section `H26#7.2` contains the token `"take"` ("Approved students take the exam..."), which keeps `H26#7.2` at score 2.059, still above `H26#6.1` (1.243).
   - **Conclusion:** E14 still fails to retrieve the correct section.
2. **Regression on E20 (`"tell me about exams"`):**
   - Expected behavior: `expect_abstain: true` (ambiguous query).
   - Before normalization: BM25 score is below the threshold, safely abstaining.
   - After normalization: `"exams"` -> `"exam"`, matching section `H26#7.2` with a BM25 score of 3.601 (> `min_score = 2.0`). Both retrieval and LLM stub paths generate an answer instead of abstaining.
   - Retrieval correct drops from 20/25 to 19/25; abstentions drop from 6/7 to 5/7.
3. **Verdict:**
   - Rouinz's evaluation in the PR description is completely accurate.
   - The recommendation to not merge this experiment into `main` and keep the baseline tokenizer is sound engineering practice.

---

## 3. Formal Structured Feedback (Course Protocol)

- **Praise:** Exemplary honesty and scientific rigor in documenting the H3 failure and E20 regression rather than pushing a flawed heuristic into production. The S1 implementation in `mini_search.py` is concise, correct, and passed all 18 unit and acceptance tests.
- **Question:** In `search()`, `index.get(word, ())` uses an empty tuple fallback instead of `set()`. While functional, is there a specific design reason for using a tuple rather than a set or `frozenset` to align with `index: dict[str, set[str]]`?
- **Suggestion:** For future work on E14 in Lab 7, addressing token-level mismatch could involve lemmatization (e.g. NLTK/spaCy WordNet lemmatizer) combined with proximity or bigram re-ranking (`"credit load"`, `"regular load"`) rather than naive character slicing, preventing false matches on common terms like `"exam"`.
