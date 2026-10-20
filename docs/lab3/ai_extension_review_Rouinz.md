**1. Ask an AI coding assistant to extend your service with ONE feature:**

Ask an AI coding assistant to add a `version` feature to `AssistantService`. The feature recognizes `version`, `what version are you?`, and `check version`, then responds with "I am running assistant-core v0.3.0".

**2. Paste the prompt you used:**

> Add a version check feature to AssistantService. Recognize the inputs "version", "what version are you?", and "check version". Return a response stating "I am running assistant-core v0.3.0". Keep the change small and add automated tests using pytest.

**3. Review the generated code manually. Document at least three changes you made:**

| # | What the AI generated | Problem you found | What you changed | Why |
|---|---|---|---|---|
| 1 | Used `Intent.VERSION` in the `Response` object inside `service.py`. | `Intent.VERSION` does not exist in the `Intent` Enum defined in `models.py`, causing an `AttributeError`. | Added `VERSION = "version"` to the `Intent` Enum class in `models.py`. | To ensure the code compiles and respects the typed model design required by the architecture. |
| 2 | Hardcoded the version string directly inside `AssistantService.handle()`. | Hardcoding magic strings inside the service logic violates maintainability principles. | Moved the version string `"0.3.0"` to `config.py` as a setting, and passed it to the service. | Keeps configuration and constants out of the main business logic (Twelve-Factor App principle). |
| 3 | Wrote tests that instantiate `AssistantService()` with no arguments. | `AssistantService` requires `settings`, `offices`, `handbook`, and `responder` in its constructor, causing `TypeError` in tests. | Modified the test to use dummy mocks/fixtures for the required dependencies before calling `handle()`. | Proper dependency injection is required for the service tests to run in isolation without crashing. |

**Checklist:**

- [x] Interfaces respected?: Yes, the feature uses the existing `Response` model and extends the `Intent` enum correctly.
- [x] New dependencies? None.
- [x] Secrets? None.
- [x] Logging of user data? No.
- [x] Tests added and meaningful? 2 tests added to check if the version intent is correctly routed and the response is accurate.