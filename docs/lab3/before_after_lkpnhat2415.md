# Before and After Maintainability

| Question | Monolith | assistant_core |
| :--- | :--- | :--- |
| Places to change the credit rate | 1 constant in code | 1 variable in .env |
| Tests run offline and deterministically? | no | yes |
| Missing `handbook.json` | prints and continues silently | `DataError` at startup |
| Secret printed or logged? | yes | no |
| Module-level globals | 9 (3 mutable) | 0 |
| Bare `except:` | 3 | 0 |
| Longest function (lines) | ~65 (`handle`) | ~15 |
| Swap the LLM without touching the service?| no | yes |