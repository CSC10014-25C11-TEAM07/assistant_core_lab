# Lab 4 homework — design for an external service that goes down

Service chosen (weather / maps / news / other approved): **Exchange Rate API**  Base URL: **`https://api.exchangerate-api.com/v4/latest/USD`**

| Failure | How you simulate it | What your API returns | What the user sees |
|---|---|---|---|
| timeout | transport raises ConnectTimeout | HTTP 200 with `stale: true` (if cached), or HTTP 503 (if no cache). | The last known exchange rate (marked as outdated), or a "Service unavailable" error if it's the first run. |
| 500 from upstream | MockTransport returns 500 | HTTP 200 with `stale: true` (if cached), or HTTP 503 (if no cache). | The last known exchange rate (marked as outdated), or a "Service unavailable" error. |
| malformed JSON | MockTransport returns `{}` | HTTP 200 with `stale: true` (if parsing fails), or HTTP 503. | The last known exchange rate (marked as outdated), or a "Service unavailable" error. |
| rate limited (429) | MockTransport returns 429 | HTTP 200 with `stale: true` (if cached), or HTTP 503. | The last known exchange rate (marked as outdated), or a "Service unavailable" error. |

Timeout value and why: **3.0 seconds.** Users expect chat assistants to be highly responsive. Waiting longer than 3 seconds degrades the user experience (UX). It is better to fail fast and fall back to cached data than to keep the user waiting indefinitely.

Retries and why: **1 retry (2 attempts total).** A single immediate retry is enough to recover from transient network glitches (like a dropped TCP packet). Retrying more times would severely delay the final response and risk hammering an upstream server that is already struggling.

Cache TTL and why: **24 hours (86400 seconds).** Global currency exchange rates fluctuate, but for the scope of a student assistant calculating tuition or daily expenses, a daily update is highly accurate. A long TTL significantly reduces the number of outgoing requests, preventing us from hitting the public API's rate limits.

Tests added (file + names): 
**`tests/test_exchange.py`**
- `test_exchange_success_updates_cache`
- `test_exchange_timeout_returns_stale_data`
- `test_exchange_upstream_500_triggers_retry_and_fallback`
- `test_exchange_malformed_json_handled_gracefully`
- `test_exchange_no_cache_returns_503`