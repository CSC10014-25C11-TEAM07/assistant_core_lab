# Lab 3 — AI extension review (<vndt4>)

**1. Ask an AI coding assistant to extend your service with ONE feature:**
- Extend `logging_setup.py` with a structured event logging helper (`log_handled`) and configurable log level support in `get_logger`, so the service automatically logs `"handled"` at `WARNING` level when a fallback is used (`degraded=True`) and `INFO` otherwise, while strictly whitelisting allowed metadata keys.

**2. Paste the prompt you used:**
- *"I am working on `logging_setup.py` in `assistant_core`, which defines `JsonFormatter` and `get_logger`. Please extend `logging_setup.py` with ONE new feature: add a `log_handled(logger, intent, latency_ms, session='local', degraded=False)` helper and allow `get_logger` to configure the handler cleanly. Ensure the JSON output only includes allowed structured fields and write unit tests in `test_logging.py`."*

**3. Review the generated code manually. Document at least three changes you made:**

| # | What the AI generated | Problem you found | What you changed | Why |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Merged all `record.__dict__` extra attributes directly into `data` inside `JsonFormatter.format` | Any extra field passed by callers (such as `api_key` or raw `user_message`) would be serialized into the JSON log, violating privacy and security constraints. | Restricted serialized fields using an explicit tuple whitelist `ALLOWED_KEYS = ("intent", "latency_ms", "session", "degraded")` with `hasattr`/`getattr`. | Guarantees that only safe operational metadata is logged — never the API key or full user message. |
| 2 | Added `logger.addHandler(handler)` unconditionally inside `get_logger` and left `logger.propagate = True` | Calling `get_logger("assistant_core")` multiple times across requests or unit tests attached duplicate `StreamHandler` instances and propagated records to the root logger, printing each JSON line multiple times. | Added `if not logger.handlers:` guard before attaching `StreamHandler()` and set `logger.propagate = False`. | Ensures idempotent logger initialization and prevents duplicate log output in both CLI runs and `pytest` suites. |
| 3 | Used `logging.StreamHandler(sys.stdout)` and `json.dumps(data)` (with default `ensure_ascii=True`) | Emitting logs to `stdout` mixed JSON logs with the user-facing answer, breaking `2> app.log