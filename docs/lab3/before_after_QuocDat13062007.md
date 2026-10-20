# Before / After Maintainability Worksheet

**Author:** Đạt (QuocDat13062007)
**Area:** Knowledge and data (`knowledge.py`, `offices.csv`, `handbook.json`)

## 1. Comparison table

| Question | Monolith | assistant_core |
|---|---|---|
| Places to change the credit rate | 1 constant in code (`RATE`) | 1 variable in `.env` (`CREDIT_RATE_VND`) |
| Tests run offline and deterministically? | No (random LLM failure, `sleep`) | Yes (15 knowledge tests, no network, no randomness) |
| Missing `handbook.json` | prints "could not load handbook" and continues silently | `DataError` raised at startup |
| Missing `offices.csv` | prints "could not load offices" and continues silently | `DataError` raised at startup |
| Malformed data (bad JSON, missing column or key) | hidden by bare `except:` or crashes later | `DataError` with a clear message |
| Secret printed or logged? | Yes (`API_KEY` printed in `llm()`) | No |
| Module-level globals | 9 (3 mutable) | 0 in `knowledge.py` (only the constant `MIN_KEYWORD_LENGTH`) |
| Bare `except:` | 3 | 0 |
| Longest function (lines) | ~65 (`handle`) | ~22 (`OfficeDirectory.from_csv`) |
| Swap the LLM without touching the service? | No | Yes (`Responder` protocol) |
| File paths | string concatenation `BASE + "/data/..."` | `pathlib.Path` |

## 2. What I changed (my part)

- Replaced the globals `offices` and `handbook` with `OfficeDirectory` and `Handbook`, which load data once.
- Replaced two bare `except:` in `load()` with `FileNotFoundError`, `JSONDecodeError`, `OSError` and `UnicodeDecodeError`, all re-raised as `DataError`.
- Kept the old behaviour: office lookup by name, rule search by keyword overlap (words longer than 3 characters, first rule wins on ties). Characterisation test: "can I register my thesis with 118 credits" returns `H26-5.3`.

## 3. What got more complex?

More files and a few more concepts (dataclasses, classmethods, custom exceptions). The trade-off is worth it because more than one person maintains the code and it must be tested and extended.

## 4. Remaining problems

- `Handbook.search()` is only a keyword-overlap baseline.
- `service.py` and `conftest.py` must create the knowledge objects with `from_csv` / `from_json`.