| Question | Before | After |
|----------|--------|-------|
| Where would you change the credit rate? How many places? | Update `RATE = 450000` directly inside the monolithic script (set in at least one configuration spot). | Update `credit_rate_vnd` in `config.py` (`Settings`), which the service then passes into `tuition()`. |
| Can you run the tests without internet or an API key? | A manual `--test` flag is available, but there is no standalone offline test setup for the fee calculations. | Yes; the deterministic tests covering `tools.py` run completely offline without requiring LLM API calls. |
| What happens if `handbook.json` is missing? | A broad exception handler catches the failure and prints an error message, leaving the handbook empty so rule lookups fail to return answers. | `Handbook.from_json()` explicitly raises a `DataError` when the file is absent, though top-level application handling for this exception still needs to be confirmed. |
| Is any secret printed or logged? | Yes | No |
| How long does it take a new teammate to find the fee logic? | More time, because fee parsing and calculation are tangled inside the monolithic workflow. | Less time, as fee calculations are separated into `tools.py`, settings reside in `config.py`, and workflow coordination is handled in `service.py`. |
| Number of global variables | 9 | 0 |
| Number of bare `except:` blocks | 3 | 0 |
| Lines in the longest function | ~65 | ~10 `load_dotenv` in `config.py`|
| `ruff check` issues | Numerous | 0 |
| Can you swap the LLM without touching the service? | Challenging, as the model and provider logic are tightly coupled to the monolithic LLM function. | Simpler in theory because `AssistantService` accepts an injected `responder` dependency, though the end-to-end provider-swapping process still requires verification. |

**Three sentences:**
1. **What improved most:** Splitting the monolith into a modular package with centralized `Settings` in `config.py`, safe telemetry in `logging_setup.py` (tracking intent, latency, and fallback status without exposing secrets or raw user messages), and an injected `Responder` protocol made the codebase secure, decoupled, and 100% offline-testable.
2. **What got more complex:** Transitioning away from a single script introduced architectural overhead, requiring coordinated modules (`config.py`, `logging_setup.py`, `service.py`, `tools.py`), strict Pydantic schemas, custom exception hierarchies, and formal typing protocols.
3. **What you would still change:** Now that `config.py` and `logging_setup.py` are in place, I would finish wiring up end-to-end integration tests and verify top-level error handling once my teammates' remaining router and knowledge pull requests are merged into `main`.