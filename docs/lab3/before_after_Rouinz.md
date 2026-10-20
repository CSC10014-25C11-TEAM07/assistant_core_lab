| Question | Monolith | assistant_core |
|----------|----------|----------------|
| Places to change the credit rate | 1 constant in code (`RATE = 450000`). | 1 variable in `.env` (loaded via `config.py`). |
| Tests run offline and deterministically? | No (dependent on actual API calls and random numbers). | Yes (uses `StubLLMResponder` and deterministic pure functions). |
| Missing handbook.json | Prints an error and continues silently. | Raises `DataError` at startup. |
| Secret printed or logged? | Yes (API key printed in debug logs). | No (`repr=False` prevents the key from leaking). |
| Module-level globals | 9 (including 3 mutable states like history). | 0 (State is managed via classes and dependency injection). |
| Bare `except:` | 3 | 0 (Replaced with specific exceptions like `DataError`, `ProviderError`). |
| Longest function (lines) | ~65 lines (`handle()` function). | ~15 lines (Logic split into router, tools, and service). |
| Swap the LLM without touching the service? | No (LLM logic is hardcoded inside the file). | Yes (via the `Responder` Protocol interface). |

**Three sentences:**

1. **What improved most:** The separation of concerns, especially isolating the deterministic tuition calculation into `tools.py` and the routing logic into `router.py`, makes the codebase highly testable and readable.
2. **What got more complex:** The project structure has significantly more files, and understanding how data flows through dependency injection (from `__main__.py` to `service.py` to `tools/knowledge`) takes more effort.
3. **What you would still change:** I would implement a more robust dependency injection container to handle the initialization of all components, rather than wiring everything manually in the CLI `__main__.py`.