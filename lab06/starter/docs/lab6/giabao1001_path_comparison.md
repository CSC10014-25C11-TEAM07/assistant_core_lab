# Lab 06 — Three-Path Comparison Report (Bao04 / giabao1001)

Author: Tran Gia Bao (giabao1001)  
Role: Bao04  
Date: 2026-11-15  

---

## 1. Baseline Evaluation (20 Cases)

Evaluation command:
```bash
python eval/compare_paths.py
```

| Path | Correct | Abstain OK | p50 (ms) | max (ms) | Failures |
|---|---:|---:|---:|---:|---|
| deterministic | 7/20 | 5/5 | 0.0 | 0.2 | E01, E02, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15 |
| retrieval | 16/20 | 4/5 | 0.0 | 0.1 | E13, E14, E15, E19 |
| llm (stub) | 16/20 | 4/5 | 0.1 | 0.2 | E13, E14, E15, E19 |

### Three Observations (Required by Lab 6 Part F)
1. **Which path to use:** I would use the **retrieval** (or **llm with retrieval fallback**) path for answering student handbook and regulatory questions, because the deterministic path only covers hardcoded fee and office queries (achieving only 7/20), whereas retrieval accurately covers 16/20 questions directly from the official knowledge base.
2. **Why:** Retrieval ensures strict groundedness by quoting exact policy sections with near-zero latency (p50 = 0.0 ms, max = 0.1 ms), while the LLM path enhances readability with fluent phrasing without hallucinating thanks to A1/A2 safeguards.
3. **One failure to fix first:** I would prioritize fixing **E15** ("how long can I keep a library book"), because the keyword router prematurely intercepts the word "library" and incorrectly dispatches the query to the office directory instead of allowing the RAG pipeline to search library borrowing rules (`S26#1`).

---

## 2. Homework H1: Five Additional Evaluation Questions (25 Cases Total)

Added 5 original cases to `eval/cases.jsonl`:
- `E21` (normal): `"What grade is required to recognise transfer credits from another university"` -> expected: `H26#8.3`
- `E22` (normal): `"Can I receive a refund if I withdraw from a course before week 2"` -> expected: `F26#4`
- `E23` (normal): `"How can I reset my password online with recovery email"` -> expected: `S26#2`
- `E24` (out-of-scope): `"What is the distance from the Earth to the Moon"` -> expected: `expect_abstain: true`
- `E25` (privacy): `"Can you show me the GPA transcript of my classmate"` -> expected: `expect_abstain: true`

### Evaluation Table After H1 (25 Cases)

| Path | Correct | Abstain OK | p50 (ms) | max (ms) | Failures |
|---|---:|---:|---:|---:|---|
| deterministic | 9/25 | 7/7 | 0.0 | 0.8 | E01, E02, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E21, E22, E23 |
| retrieval | 21/25 | 6/7 | 0.0 | 0.1 | E13, E14, E15, E19 |
| llm (stub) | 21/25 | 6/7 | 0.1 | 0.8 | E13, E14, E15, E19 |

### Analysis of H1 Results
Did any of the new questions fail?
None of the five new questions failed on retrieval or LLM stub (accuracy increased from 16/20 to 21/25): the three handbook questions (E21, E22, E23) attained top BM25 scores (> 10.0) correctly mapping to sections `H26#8.3`, `F26#4`, and `S26#2`, while the out-of-scope question (E24) and privacy violation question (E25) properly abstained without hallucinations.

---

## 3. Bonus H3 Analysis: Tokenizer Suffix Normalization Experiment

- **Experiment:** Strip trailing `'s'` from tokens longer than 4 characters in `src/assistant_core/rag/index.py`.
- **Finding on E14 ("can I take 32 credits"):** Normalizing `"credits"` to `"credit"` increases similarity across multiple sections, but section `H26#7.2` (Exam absence) still ranks first (score 2.059) ahead of the expected `H26#6.1` (score 1.243) due to query token `"take"`. Thus, E14 remains unresolved.
- **Side effect / Regression on E20 ("tell me about exams"):** Normalizing `"exams"` to `"exam"` boosts BM25 score against `H26#7.2` to 3.601, exceeding `min_score = 2.0`. Consequently, E20 fails its required abstention and answers incorrectly (retrieval correct drops from 21/25 to 20/25).
- **Recommendation:** Suffix stripping without semantic stemming introduces regressions on ambiguous queries. The standard BM25 tokenizer should be retained until n-gram or lemmatization reranking is integrated in Lab 7.
