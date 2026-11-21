# Lab 7 — Usability checklist

Tested by Bao04 (`giabao1001`) on 2026-11-21 against main `24333b9`.
Only verified items are checked. An unchecked item is a failure, partial result,
or pending check as explained below; this is not MVP acceptance.

- [x] The first screen says what the assistant can do, with example questions — welcome text and four sidebar examples observed.
- [x] Empty or too-long input shows a friendly message (not a crash) — empty Enter sends nothing, as D.4 requires; 2,001 characters shows the length warning. Neither created an interaction.
- [x] While waiting, the user sees "Thinking…" — observed with a three-second forwarding delay and the unmodified UI.
- [ ] Every answer from documents shows its sources — **FAIL, L1:** successful API responses trigger `NotImplementedError: L1` before the UI appends the answer.
- [ ] "I don't know" answers tell the user who can help (escalation) — **BLOCKED, L1/L2:** the France question fails in L1; the separate L2 unit test also fails. The API itself returns `escalate=true` and Training Office guidance.
- [x] If the backend is down, the page says so clearly — startup banner and friendly chat error observed without an uncaught exception.
- [ ] Each answer has 👍 / 👎, and clicking gives a "thanks" message — **FAIL, F1:** 👎 is absent. Seeded-history diagnostics also expose feedback retry and immediate-hiding problems; normal chat feedback remains blocked by L1.
- [x] The page says it is an AI assistant — sidebar disclosure observed; the sidebar starts collapsed at phone width.
- [ ] Text is readable (size, contrast); buttons have clear labels — **PARTIAL:** main text/input are 16 px and examples have text labels, but the 14 px AI disclosure is pale (measured contrast 2.12:1).
- [ ] Works on a phone-width window — **PARTIAL:** initial layout, sidebar and backend-down error inspected at 390 × 844; initial layout also inspected at 320 × 768. No document overflow at either width. Successful chat/feedback cannot be accepted until L1/L2/F1 are integrated.

Follow-up: Nhật's proposed L1/L2 PR #108 (`26ece65`) passes 49 official starter
tests and successfully renders the thesis/source and France escalation in a
normal browser flow, including the thesis answer at 390 px. It is not merged;
the checkboxes above still describe tested main `24333b9`. F1 remains incomplete.

Full results, reproduction steps, owners and screenshots:
[Bao04 QA report](../starter/docs/lab7/usability_qa_giabao1001.md).

Part E.3's two-minute hallway test is **pending**: no outside tester or authentic
observation is available, as confirmed by Bao04. Browser automation is not a
substitute for that observation. H1's ten-minute test belongs to Tân in the team
assignment and is tracked separately in `user_test_observations.md`.
The [E.3 worksheet](e3_hallway_test_giabao1001.md) provides the procedure, a blank
session record and a clearly labeled hypothetical rehearsal scenario.
