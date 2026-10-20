# Lab 3 — Before / after maintainability comparison (giabao1001)

| Question | Before | After |
| :--- | :--- | :--- |
| Where would you change the credit rate? How many places? | 1 place: hardcoded constant `RATE = 450000` at module level (line 8) | 1 place: configurable in `Settings(credit_rate_vnd=...)` in `src/assistant_core/config.py` |
| Can you run the tests without internet or an API key? | No: ad-hoc `test()` calls simulated `llm()` with hardcoded key, 0.2s sleep, and 10% random failure | Yes: 100% offline and deterministic. `StubLLMResponder` and `TemplateResponder` run without internet or API key (all 43 tests pass offline) |
| What happens if `handbook.json` is missing? | Prints `"could not load handbook"` to stdout via bare `except:`, leaves `handbook = []`, and subsequent queries return `"Sorry I dont know"` | Raises `DataError` cleanly at knowledge loading; service returns `Intent.UNKNOWN` with `degraded=False` without crash |
| Is any secret printed or logged? | Yes: `API_KEY = "sk-test-2b7c1d9e4f0a"` is hardcoded and printed in debug mode (`print("[debug] calling", MODEL, "with key", API_KEY)`) | No: No API keys hardcoded or printed. Service logging logs only generic warning `"provider failed; using template fallback"` without leaking user questions or keys |
| How long does it take a new teammate to find the fee logic? | Slow: mixed inside a 56-line monolithic `handle()` function with string parsing and math | Fast: isolated in dedicated pure functions `parse_credits()` and `tuition()` in `src/assistant_core/tools.py` |
| Number of global variables | 9 module-level data globals (`API_KEY`, `MODEL`, `RATE`, `RETAKE_RATE`, `DEBUG`, `history`, `offices`, `handbook`, `BASE`), including 3 mutable globals (`history`, `offices`, `handbook`) | 1 module-level assigned data global across all `src/`: `log = logging.getLogger(__name__)` in `service.py`. 0 mutable business data globals |
| Number of bare `except:` blocks | 3 bare `except:` blocks (in `load()` for offices, `load()` for handbook, and `main()`) plus 1 broad `except Exception:` | 0 bare `except:` blocks across all `src/`. Handlers catch specific exceptions (`except ProviderError:`, `except (FileNotFoundError, json.JSONDecodeError):`) |
| Lines in the longest function | 56 physical lines (`handle()` function, lines 44–99) | 30 physical lines (`tuition()` in `src/assistant_core/tools.py`, lines 33–62) |
| `ruff check` issues | 8 issues in monolith (E401, I001, E711, BLE001, E501, 3x E722) | 0 issues in assigned files (`responder.py`, `test_responder.py`). (Upstream team files have 6 formatting/import issues pending team review) |
| Can you swap the LLM without touching the service? | No: `llm()` function is hardcoded and called directly inside `handle()` | Yes: `AssistantService` accepts any `responder: Responder` via dependency injection (Protocol adapter pattern). Swapping between `TemplateResponder`, `StubLLMResponder`, or future real LLM provider requires zero changes to `service.py` |

**Three sentences:**
1. **What improved most:** The introduction of the `Responder` Protocol and Dependency Injection completely decoupled LLM response generation from business service logic, enabling 100% offline deterministic testing and seamless provider swapping with automated template fallback.
2. **What got more complex:** The system evolved from a simple script into a multi-module package requiring formal contracts, Pydantic request/response models, custom exception hierarchies, and typing protocols.
3. **What you would still change:** I would connect `Settings` to real `.env` loading and finish end-to-end integration testing once teammates' remaining router and knowledge pull requests are merged into `main`.
