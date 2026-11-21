# Study Assistant (Lab 7 reference)

## Setup and start both servers

Open PowerShell in `lab07/starter`. Run setup once with Python 3.12.

```powershell
py -3.12 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m pip install -e .
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Open two terminals in `lab07/starter` and keep both running.

In terminal 1, start the FastAPI backend. API docs are available at http://127.0.0.1:8000/docs.

```powershell
& .\.venv\Scripts\python.exe -m uvicorn assistant_api.main:create_app --factory
```

In terminal 2, start Streamlit and open http://localhost:8501 in your browser.

```powershell
& .\.venv\Scripts\python.exe -m streamlit run ui/app.py
```

The UI calls the backend over HTTP. If the API uses a different address, set `ASSISTANT_API_URL` in terminal 2 before starting Streamlit.

## API contract (v1)
| Method | Path | Body | Success | Errors |
|---|---|---|---|---|
| GET | `/health` | — | 200 `{"status":"ok","version":...}` | — |
| POST | `/v1/chat` | `{"message": str 1–2000, "session_id": str}` | 200 `{answer, intent, sources[], degraded, request_id}` | 422 invalid, 429 rate limit |
| POST | `/v1/feedback` | `{"request_id": str, "rating": -1/0/1, "comment"?: str ≤500}` | 201 feedback with `id`, `created_at` | 422 |
| GET | `/v1/feedback` | header `X-API-Key` | 200 list | 401 |
| GET | `/v1/stats/intents` | header `X-API-Key` | 200 `[{intent, requests, avg_latency_ms, unresolved}]` | 401 |
| GET | `/v1/weather` | — | 200 `{temperature_c, wind_kmh, description, observed_at, stale}` | 503 upstream down |

All errors use one shape: `{"error": {"code": "...", "message": "..."}}`.

## Database (Lab 5)
```
python scripts/migrate.py assistant.db      # apply sql/migrations in order
python scripts/seed.py assistant.db 300     # synthetic data only
sqlite3 assistant.db < sql/queries.sql      # the five queries + product questions
```
New endpoint: `GET /v1/stats/intents` (header `X-API-Key`). `POST /v1/feedback` now returns 404 for an unknown `request_id`.

## AI services (Lab 6)
Knowledge base: `data/kb/*.md` (chunked by heading). Prompt: `src/assistant_core/prompts/answer_v1.txt`.
```
LLM_PROVIDER=stub python -m assistant_core "I lost my student card"      # offline
LLM_PROVIDER=ollama LLM_MODEL=llama3.2 python -m assistant_core "..."     # local model (ollama pull llama3.2)
python eval/compare_paths.py                                              # deterministic vs retrieval vs LLM
```
`/v1/chat` responses now include `path` (deterministic | retrieval | llm | tool | abstain), `escalate` and `confidence`.

## Tests
```
pytest -q                          # unit + API tests (external API mocked)
bash api-tests/curl_tests.sh       # manual tests against a running server
```
Postman / Bruno: import `api-tests/study-assistant.postman_collection.json`.
