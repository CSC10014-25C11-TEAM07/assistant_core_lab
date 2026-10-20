| Question | Before | After |
|----------|--------|-------|
| Where would you change the credit rate? How many places? | Change `RATE = 450000` in the monolithic file; at least one configuration definition. | Change `credit_rate_vnd` in `config.py` / `Settings`; the service passes the configured rate to `tuition()`. |
| Can you run the tests without internet or an API key? | The original program has a manual `--test` mechanism, but independent offline testing of the fee logic is not established. | Yes, the deterministic tests for `tools.py` can run without an LLM API call. |
| What happens if `handbook.json` is missing? | The original loader catches exceptions broadly and prints an error; the handbook may remain empty, so rule queries may not find an answer. | The full `Handbook.from_json()` implementation raises `DataError` when the file is missing. Application-level handling of that error still needs verification. |
| Is any secret printed or logged? | Yes | No |
| How long does it take a new teammate to find the fee logic? | Longer: fee parsing and calculation are embedded in the monolithic workflow. | Shorter: fee logic is isolated in `tools.py`, with configuration in `config.py` and orchestration in `service.py`. |
| Number of global variables | 9 | 0 |
| Number of bare `except:` blocks | 3 | 0 |
| Lines in the longest function | Not measured from the complete original file. | Not measured from the complete refactored files. |
| `ruff check` issues | Many | 0 |
| Can you swap the LLM without touching the service? | Difficult: model/provider behavior is closely tied to the monolithic LLM function. | Easier in principle because `AssistantService` receives a `responder` dependency, but the actual provider-swapping workflow still needs verification. |

**Three sentences**

1. What improved most: the tuition logic is separated into deterministic functions with dedicated tests, making it easier to locate and verify.
2. What got more complex: The architecture is more complex because responsibilities are distributed across modules and their dependencies must be wired together correctly.
3. What you would still change: I would still improve startup integration and error handling, especially around missing knowledge files and office lookups, and verify the complete package with automated tests and Ruff.
