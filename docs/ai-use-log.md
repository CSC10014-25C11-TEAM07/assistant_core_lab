## Lab08 H1 — Verify the Lab07 credit approval rule

- Source: Lab07 U4 in PR #113. AI helped write the rule that credit loads above 30 require advisor approval.
- For Lab08, I extracted the rule into `requires_advisor_approval()` in `lab08/starter/ui/credit_rules.py` and added explicit validation for non-integer inputs.
- Tests cover 0, 30, 31, a very large integer, an empty string, Vietnamese text, and `None`.
- Result: `python -m pytest -q tests/test_credit_rules.py` — **7 passed in 0.08s**.