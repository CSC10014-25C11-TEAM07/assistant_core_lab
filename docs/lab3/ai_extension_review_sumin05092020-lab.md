# Lab 3 — AI extension review (sumin05092020-lab)

**1. Ask an AI coding assistant to extend your service with ONE feature:**
- Add an 'exam absence' intent. When the user asks about being absent from an exam, the bot should tell students the deadline to submit the absence form based on the handbook.

**2. Paste the prompt you used:**
- "I am working on a Python service called assistant_core. Please write the Python code to extend my service with ONE new feature: Add an 'exam absence' intent. When the user asks about being absent from an exam, the bot should tell students the deadline to submit the absence form based on the handbook. Show me the changes needed in router.py, models.py, and service.py."

**3. Review the generated code manually. Document at least three changes you made:**

| # | What the AI generated | Problem you found | What you changed | Why |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `if "absence" in text:` in `router.py` | The routing condition is too narrow. It misses common student phrases like "missed exam" or "absent". | Added a broader set of keywords: `ABSENCE_KEYWORDS = frozenset({"absence", "absent", "missed exam"})`. | To improve the bot's accuracy in understanding different user phrasing. |
| 2 | The AI returned a hardcoded string: "must submit evidence within 3 working days" in `service.py`. | If the handbook updates the rule (e.g., to 5 days), the code will become outdated and give wrong information. | Modified the service to dynamically fetch the exact wording from the `handbook.json` chunk instead of hardcoding. | To maintain a Single Source of Truth (SSOT) and ensure the bot's answers are always up-to-date with the official handbook. |
| 3 | Added tests in `test_router.py` and `test_service.py`, bringing the suite to 23 passing tests. | The tests only checked lowercase "absence". | Added assertions for uppercase and mixed-case inputs like "ABSENCE" and "I was Absent". | To ensure case-insensitivity logic is explicitly covered by unit tests. |

**Checklist:** 
- Interfaces respected? Yes.
- New dependencies? None.
- Secrets? None. 
- Logging of user data? No.
- Tests added and meaningful? Yes, the test suite now has 23 passing tests.
