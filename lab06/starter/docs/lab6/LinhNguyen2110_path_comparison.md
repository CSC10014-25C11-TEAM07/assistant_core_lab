# Lab06 — Individual A1–A2 Verification & Path Comparison

## 1. A1 — Abstain / Escalation

Verified the existing A1 implementation in `rag/answerer.py`.

The RAG pipeline abstains and escalates when no relevant retrieval result is available or the highest retrieval score is below the configured minimum threshold.

## 2. A2 — Grounding Check

Verified the existing A2 implementation in `llm.py`.

For non-abstaining answers, the grounding check requires at least one source ID and ensures all cited source IDs belong to the retrieved sources. Invalid citations raise `ProviderError`.

Additional A2 tests were submitted separately under team Issue #85.

## 3. Test Results

Command:

`python -m pytest -q`

Result: **42 passed, 1 warning**

The warning concerns a deprecated Starlette/AnyIO API and does not cause test failures.

## 4. Path Comparison

Command:

`python eval/compare_paths.py`

| Path | Correct | Abstain OK | P50 (ms) | Max (ms) |
|---|---:|---:|---:|---:|
| Deterministic | 9/25 | 7/7 | 0.0 | 0.6 |
| Retrieval | 20/25 | 6/7 | 0.0 | 0.1 |
| LLM (stub) | 20/25 | 6/7 | 0.4 | 1.1 |

### Failed Cases

- **Deterministic:** E01, E02, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E21, E22, E23
- **Retrieval:** E13, E14, E15, E19, E23
- **LLM (stub):** E13, E14, E15, E19, E23

## 5. Three Observations

1. Retrieval and LLM stub both answered 20 out of 25 evaluation cases correctly, outperforming the deterministic path, which answered 9 out of 25 correctly.
2. The deterministic path successfully handled all seven abstention cases, while retrieval and LLM stub each handled six out of seven.
3. Retrieval achieved the lowest maximum measured latency at 0.1 ms, while the LLM stub had a higher median latency of 0.4 ms and a maximum latency of 1.1 ms.