# Lab 7 — Bao04 usability QA

**Result: integration not accepted yet.** D.4 and Part E were exercised against
main `24333b963b1601b02e06acabb5261a5161e6fd3f` on 2026-11-21. Successful
chat display is blocked by L1/L2, and F1 is not implemented. This report records
actual observations without treating unimplemented or untested states as passes.

## Scope and assignment

Sources supplied in `/Users/trangiabao/Downloads/`:
`CSC10014_2026_Lab07_UI_Fullstack_Tutorial.docx.pdf`, pp.12–16, and
`Phan_cong_Lab07.docx`, section I. The assignment's work paths are relative to
the repository's `lab07/` directory.

- Bao04: D.4, Part E, phone-width checks, checklist and reproducible failures; review Bao06's F1. Bao06 reviews this QA contribution.
- Nhật: L1/L2; Bao06: F1; Linh: U1–U4; Hân: H2; Tân: H1; Đăng: integration, final verification, README and `v0.7-mvp`.
- This assignment distributes team tasks. It does not ask Bao04 to repeat every member's implementation or produce seven duplicate UI implementations.

No F1 PR by Bao06 was available at the time of this audit. The feedback findings
below concern the supplied baseline, **not a review or approval of a Bao06 PR**.
Formal review remains pending when that PR exists.

## Environment and commands

Python 3.12, pinned `starter/requirements.txt`, Streamlit 1.39.0, pytest 8.3.3,
offline `LLM_PROVIDER=stub`, an isolated SQLite database, and headless Chrome via
Playwright CLI. Desktop: 1280 × 900. Resized browser viewports: 390 × 844 and
320 × 768. No physical phone, mobile browser engine, or touch gestures were tested.

Run from `lab07/starter`, with dependencies installed in an activated environment:

```sh
# Terminal 1; use a disposable database path.
PYTHONPATH=src LLM_PROVIDER=stub DATABASE_URL=sqlite:////tmp/lab07-bao04-qa.db \
  python -m uvicorn assistant_api.main:create_app --factory --host 127.0.0.1 --port 18007

# Terminal 2.
ASSISTANT_API_URL=http://127.0.0.1:18007 python -m streamlit run ui/app.py \
  --server.address 127.0.0.1 --server.port 18507 --browser.gatherUsageStats false
```

Open `http://127.0.0.1:18507`. Stop only the API process started for this check
when reproducing backend-down behavior. Actual test metadata is in
[environment.json](evidence/environment.json).

## D.4 browser results

| Case | Action and expected result | Actual result | Status / owner |
|---|---|---|---|
| D4-01 | Click a sidebar example; see the question and answer. | Thesis example reaches the API, then `format_sources()` raises `NotImplementedError: L1`. The answer is never appended. | FAIL — Nhật L1 |
| D4-02 | Ask about thesis registration with 118 credits; show answer and `Sources: H26#5.3 …`. | Same thesis run fails in L1. Independent API probe returns 200, the 120-credit requirement and `H26#5.3`. API evidence is not a UI pass. | FAIL — Nhật L1 |
| D4-03 | Ask the capital of France; show Training Office escalation. | Typed question also reaches L1 and fails. Independent API probe returns 200, `escalate=true`, `path=abstain` and room I.101; L2 also fails its unit test. | FAIL/BLOCKED — Nhật L1/L2 |
| D4-04 | Press Enter with empty input; send nothing. | No new chat message, exception or API interaction; database interaction count stays 0 → 0. | PASS |
| D4-05 | Click 👍; thank the user and remove rating controls. | Real chat path cannot reach the controls because of L1. In an explicitly seeded-history browser harness, 👍 saves rating 1 and thanks the user, but its button stays visible until a later rerun. 👎 does not exist. | BLOCKED end to end; diagnostic FAIL — Bao06 F1 |
| D4-06 | Stop API and ask a question; show a friendly error without crashing. | Backend warning appears; asking “Where is the library?” shows “Cannot reach the assistant. Is the backend running?” without an uncaught exception. | PASS |

Screenshots: [initial page](evidence/01-desktop-initial.png),
[thesis failure](evidence/03-thesis-crash.png),
[backend down](evidence/09-backend-down.png).
[API boundary evidence](evidence/api_boundary.json) demonstrates that the API can
answer the two questions; it does not demonstrate that the UI renders them.

## Part E observations

| Check | Observation | Result |
|---|---|---|
| Capabilities and examples | Welcome explains fees, offices and handbook; four examples appear in the sidebar. | PASS |
| Input validation | Empty Enter is silent as D.4 specifies. A 2,001-character message produces a friendly maximum-length warning; interaction count stays 0 → 0. | PASS |
| Waiting feedback | “Thinking…” observed with a temporary forwarding proxy adding three seconds only to `POST /v1/chat`. The original UI and real backend were used. | PASS, controlled-delay diagnostic |
| AI disclosure | Explicit AI notice appears in the sidebar. At phone width the user must open the collapsed sidebar to read it. | PASS for presence; discoverability note |
| Text and contrast | Main body/input 16 px; disclosure 14 px. Disclosure foreground `rgb(163,168,184)` on sidebar `rgb(240,242,246)` measures 2.117:1 and looks faint. | PARTIAL — Đăng integration follow-up |
| 390 × 844 | Welcome, input, open/close sidebar and backend-down error fit. Document scroll width 390; input x=17…373. | Layout PASS; chat/feedback acceptance blocked |
| 320 × 768 | Welcome and input fit. Document scroll width 320; input right edge 303. | Initial layout PASS; full flow pending |
| E.3 external hallway test | Bao04 confirmed no outside tester has tried the page. No human observation has been invented. | PENDING — Bao04 |

Evidence: [long input](evidence/02-long-input.png),
[waiting](evidence/04-thinking-delayed.png),
[390 px](evidence/05-mobile-390.png),
[mobile sidebar](evidence/06-mobile-sidebar.png),
[320 px](evidence/07-mobile-320.png),
[mobile connection error](evidence/10-mobile-backend-down.png), and
[measured observations](evidence/browser_observations.json).

The Impeccable Python source detector returned `[]` for `ui/app.py`; that narrow
scan does not assess Streamlit's generated DOM. Rendered observations above take
precedence. This is a scoped lab usability audit, not a full accessibility,
performance, dark-mode or mobile-device certification.

## Reproduction and owner handoff

**B07-01 — successful chat crashes (blocking; Nhật).** Start both servers, click
the thesis example (or type the France question). The HTTP call succeeds, then
`ui/app.py` calls `format_sources()` and fails in `ui/logic.py` at the L1 TODO.
`status_note()` separately raises `NotImplementedError: L2`. Complete the assigned
helpers, rerun `pytest -q tests/test_ui.py`, and repeat D4-01/02/03. Retest escalation
priority when both `escalate` and `degraded` are true.

**B07-02 — negative feedback absent (Bao06).** Run the seeded-history acceptance
tests below: two answers each expose 👍 and no 👎. Implement F1 with distinct keys,
the clicked answer's `request_id`, rating -1, a thank-you message and rated state.
Then verify 👍 on one real answer and 👎 on a different real answer after L1/L2 land.

**B07-03 — vote controls remain after success (Bao06 / Đăng).** In the diagnostic
browser harness, click the first answer's 👍. HTTP persistence succeeds and a toast
appears, but both 👍 buttons remain on screen. The current handler adds the ID to
`rated` after rendering the button and does not refresh that rendered state.
Ensure successful votes remove the clicked answer's controls immediately. Check
this in a browser: AppTest 1.39 can retain stale deltas across an internal rerun,
so the automated checks only assert the subsequent clean render.

**B07-04 — rejected feedback claims success (Bao06 / Đăng).** In seeded-history
testing, make feedback sending return `False`. The app still adds the answer to
`rated` and displays “Thanks for your feedback!”. The supplied handler ignores
the client's Boolean result. Preserve retry and display a useful failure message
when feedback is not accepted. This is a robustness finding beyond adding 👎.
The browser harness reproduces this too: after the first vote persisted, stop
the isolated API and click the second answer's 👍. A new thank-you toast appears
even though the database feedback count remains 1. See
[successful vote with controls still present](evidence/11-feedback-seeded-positive.png),
[failed send with success toast](evidence/12-feedback-seeded-rejected.png) and
[database counts](evidence/feedback_db_observations.json).

**B07-05 — faint disclosure (Đăng).** Open the sidebar and inspect the AI notice.
Keep the notice readable against the sidebar background; the computed colors and
contrast calculation are recorded in `browser_observations.json`. This is a
readability finding, not a claim of a completed standards audit.

## Automated verification

```sh
# From lab07/starter
python -m pytest -q
python -m pytest -q tests/test_ui.py
python -m pytest -q tests/test_feedback_ui_acceptance.py
python -m ruff check tests/test_feedback_ui_acceptance.py

# From lab07/practice
python -m pytest -q
```

| Scope | Result | Evidence |
|---|---|---|
| Official starter baseline, before QA tests | 47 passed, 2 failed (L1/L2) | [baseline log](evidence/baseline_starter_pytest.txt) |
| Official practice baseline | 1 passed, 3 failed (U2/U3/U4) | [baseline log](evidence/baseline_practice_pytest.txt) |
| Official UI tests | 5 passed, 2 failed (L1/L2) | [UI log](evidence/official_ui_pytest.txt) |
| New feedback acceptance tests | 1 passed, 3 failed (missing 👎 and rejected-feedback state/toast) | [feedback log](evidence/feedback_ui_pytest.txt) |
| Full starter including QA tests | 48 passed, 5 failed (the two official failures plus three feedback checks) | [full log](evidence/full_starter_pytest.txt) |
| Ruff on the added test file | Passed | [lint log](evidence/qa_ruff.txt) |

The new tests seed two answer records and fake the client. They exercise positive
and negative votes on different answer IDs, independent keys, rated state, the
next clean render and retry on rejection. They bypass L1/L2 deliberately and do
not prove real HTTP persistence or a complete chat flow. Failures remain visible;
none are skipped or marked as expected failures.

The browser feedback harness separately seeds history using two real API results
and executes the unchanged `ui/app.py`, bypassing only the blocked answer-formatting
path. It is diagnostic evidence, not normal end-to-end acceptance.

The exact temporary harness sources are saved as
[feedback harness](evidence/feedback_browser_harness.py.txt) and
[delay proxy](evidence/delay_proxy.py.txt). To repeat the feedback diagnostic
with the isolated API running, use a separate terminal from `lab07/starter`:

```sh
cp docs/lab7/evidence/feedback_browser_harness.py.txt /tmp/lab07-feedback-diagnostic.py
QA_STARTER_DIR="$PWD" ASSISTANT_API_URL=http://127.0.0.1:18007 \
  python -m streamlit run /tmp/lab07-feedback-diagnostic.py --server.port 18509
```

For the waiting diagnostic, copy `delay_proxy.py.txt` to `/tmp/delay_proxy.py`,
run `python -m uvicorn delay_proxy:app --app-dir /tmp --port 18008`, then start a
second copy of the original UI on port 18508 with
`ASSISTANT_API_URL=http://127.0.0.1:18008`. The proxy forwards to the real API on
18007 and delays chat requests only.

## Remaining acceptance work

1. Nhật completes L1/L2; Bao06 provides F1; rerun this matrix on the integrated commit.
2. Review Bao06's actual F1 PR and verify both votes on different answers, successful persistence, immediate hiding and failure retry.
3. Improve disclosure readability; repeat the successful answer/feedback flow at both phone widths.
4. Conduct E.3 with a classmate outside the team for two minutes without coaching; record one authentic surprise. Tân's separate H1 ten-minute test remains his assigned work.
5. Bao06 reviews this QA PR; Đăng owns final test acceptance, integration and the MVP tag.

## Follow-up: Nhật's proposed L1/L2 fix

PR [#108](https://github.com/CSC10014-25C11-TEAM07/assistant_core_lab/pull/108)
appeared during this audit. Its exact head
`26ece656e25b34357c52c7908c92dc4444e1d576` was checked out separately, without
modifying this QA branch. Main was still `24333b9`. These are **proposed-fix
results**, not a statement that the implementation has merged or the checklist
on main is fully accepted.

- All **49 official starter tests passed**: [log](evidence/pr108_official_starter_pytest.txt).
- Six additional helper assertions passed, including multiple sources and escalation priority over degradation: [results](evidence/pr108_helper_boundaries.json).
- Normal UI → API browser flow now shows the sidebar thesis question, answer and `H26#5.3` source; the typed France question shows the Training Office escalation. D4-01/02/03 pass on this proposed head.
- The thesis answer and source also render at 390 px. This was an actual chat flow, without seeded history.
- 👍 saves rating 1 with the thesis answer's request ID and shows a toast, but its control remains visible immediately afterward. 👎 is still absent, so D4-05/F1 is not accepted.

Evidence: [thesis answer](evidence/13-pr108-thesis-answer.png),
[mobile answer](evidence/14-pr108-mobile-answer.png),
[escalation](evidence/15-pr108-escalation.png),
[feedback still visible](evidence/16-pr108-positive-feedback.png), and
[preview metadata and database rows](evidence/pr108_preview.json).

This is QA of the proposed integration, not a formal GitHub review of PR #108;
the team assignment gives that review to Đăng. Recheck the final integrated head
after #108 and F1 land. E.3 still needs the real outside tester.
