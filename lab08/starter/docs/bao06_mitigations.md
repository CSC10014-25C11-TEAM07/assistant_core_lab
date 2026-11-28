# Lab 8 — Bao06 mitigation handoff

Implemented against main commit 6040ef9 on 28 November 2026.

## Three confirmed failures and fixes

Linh's PR #120 supplies the three Part E regression tests. All three failed on the original starter and passed after these changes. The greeting control also passed. Linh's test file was used unchanged in an isolated checkout; this PR leaves that file to PR #120.

| Failure | Severity | Mitigation | Linh's regression test |
|---|---|---|---|
| A downvote cannot carry an explanation | Medium | A per-answer comment field accepts up to 500 characters and submits trimmed text with a negative rating. Failed submissions preserve the comment and allow retry. | test_downvote_submits_optional_feedback_comment |
| The answer quotes the minimum without addressing 118 credits | Medium | Trusted rule text supplies the minimum. Deterministic code explains a shortfall before invoking a provider. Both legacy and deployed RAG routes use it. The other conditions remain visible in the cited rule text. | test_thesis_answer_explains_why_118_credits_is_not_enough |
| The handbook reference is plain text | Medium | Known source IDs become Markdown links to the checked-in Lab 8 document and heading. Legacy IDs work. Unknown IDs retain their readable label. | test_thesis_citation_links_to_handbook_section |

## Verification

- Linh's exact PR #120 file before fixes had three failures and one passing control.
- After fixes, the same file passed all four tests.
- All 11 additional cases in tests/test_bao06_mitigations.py passed.
- With Linh's tests temporarily included, the starter suite reported 75 passed and two pre-existing G1 failures.
- The committed suite reported 72 passed and two pre-existing G1 failures after restoring the base Part E placeholder.
- Ruff passed on all changed Python files.
- Headless Chrome, Streamlit 1.39.0, a real Uvicorn API and SQLite verified normal chat, the 118/120 shortfall, the exact citation URL, a Vietnamese downvote comment, positive feedback on a different answer, and a thank-you message visible 1.5 seconds after rerun.
- The supplied red-team runner reported 11/12, with R03 failing. R02 passed through its general refusal heuristic even though the corresponding G1 regex unit test still fails.

## Integration handoff

Hân can use the three rows and exact test names above in the catalogue after checking the integrated branch. The additional test file covers retry with Vietnamese text, the deployed RAG route with template/stub/unavailable-provider configurations, the minimum boundary, changed document thresholds, ambiguous numeric inputs, and legacy/unknown citations.

Đăng can review this PR together with Linh's PR #120. The adjusted test_format_sources expectation reflects the requested clickable citation. No partner exchange results were available in the checked main snapshot, so partner-specific failures need another check when Bảo04 supplies that report.

Nhật's G1 work is still needed for the two missing prompt-injection patterns and the 12/12 target. Links point to the group's existing Lab 8 sample documents.

## H2 — Two-sentence reflection

Một tài liệu trong kho RAG có thể chèn chỉ thị yêu cầu mô hình bỏ qua quy tắc và đưa nội dung cuộc trò chuyện vào liên kết ngoài, khiến câu trả lời bị thao túng dù người dùng chỉ hỏi về học vụ.
Em đề xuất đánh dấu và tách nội dung truy xuất thành dữ liệu không đáng tin, giới hạn quyền gọi công cụ bằng code và kiểm tra cấu trúc đầu ra, mã nguồn cùng miền liên kết được phép, sau đó dùng pytest để giữ lại ca tấn công và ca đối chứng thành regression test.

Reading references are [pytest Get Started](https://docs.pytest.org/en/stable/getting-started.html) and [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/). These H2 defenses are proposals; this PR does not claim to implement an indirect-injection defense.

## Reproduce

Run from lab08/starter with the required dependencies installed.

    python -m pytest -q tests/test_bao06_mitigations.py
    python -m pytest -q
    python redteam/run_redteam.py

After integrating PR #120, run tests/test_my_regressions.py against the fixes as well.
