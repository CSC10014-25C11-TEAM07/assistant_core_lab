# Lab 3 — Before / after maintainability comparison (sumin05092020-lab)

| Question | Before | After |
| :--- | :--- | :--- |
| Where would you change the credit rate? | 1 constant in code | 1 variable in .env |
| Can you run the tests without internet? | no | yes |
| What happens if handbook.json is missing?| prints and continues silently | DataError at startup |
| Is any secret printed or logged? | yes | no |
| Number of global variables | 9 (3 mutable) | 0 |
| Number of bare except: blocks | 3 | 0 |
| Lines in the longest function | ~65 (handle) | ~15 |
| How long does it take a new teammate to find the fee logic? | Slow (mixed inside handle function) | Fast (isolated in tools.py) |
| Can you swap the LLM without touching the service? | no | yes |
| ruff check issues | Many (line length, bare excepts) | 0 |

**Three sentences:**
1. What improved most: The system became highly modular, testable, and secure by isolating logic into separate files, removing global states, and keeping secrets out of the code.
2. What got more complex: The architecture requires understanding more files, explicit routing logic, and Pydantic models to manage data flow.
3. What you would still change: I would like to integrate a real LLM provider instead of relying solely on the stub and template fallback.
