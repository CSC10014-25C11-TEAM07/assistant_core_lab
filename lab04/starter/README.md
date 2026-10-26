# Study Assistant — backend (Lab 4 reference)

## Setup (Windows / Git Bash)
Run these commands from `lab04/starter`. Python 3.12 works with the pinned lab dependencies.
```bash
py -3.12 -m venv .venv312
source .venv312/Scripts/activate
python -m pip install -r requirements.txt
python -m pip install -e .
test -f .env || cp .env.example .env
```
The local `.env` and virtual environments are ignored by Git.

## Run the API
```
python -m uvicorn assistant_api.main:create_app --factory --reload
```
Open http://127.0.0.1:8000/docs for the interactive OpenAPI documentation.

## API contract (v1)
| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | `/health` | — | 200 `{"status":"ok","version":...}` | — |
| POST | `/v1/chat` | `{"message": str 1–2000, "session_id": str}` | 200 `{answer, intent, sources[], degraded, request_id}` | 422 invalid; 429 only with the optional rate-limit bonus |
| POST | `/v1/feedback` | `{"request_id": str, "rating": -1/0/1, "comment"?: str ≤500}` | 201 feedback with `id`, `created_at` | 422 |
| GET | `/v1/feedback` | header `X-API-Key` | 200 list | 401 |
| GET | `/v1/weather` | — | 200 `{temperature_c, wind_kmh, description, observed_at, stale}` | 503 upstream down |
| GET | `/v1/offices` | — | 200 list of `{name, room, hours}`, sorted by name | — |

All errors use one shape: `{"error": {"code": "...", "message": "..."}}`.

## Tests
```
python -m pytest -q                # unit + API tests (external API mocked)
bash api-tests/curl_tests.sh       # manual tests against a running server
```
Postman / Bruno: import `api-tests/study-assistant.postman_collection.json`.
