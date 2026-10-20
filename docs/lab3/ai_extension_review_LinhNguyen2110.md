**1. Ask an AI coding assistant to extend your service with ONE feature:**

Ask an AI coding assistant to add a `help` feature to `AssistantService`. The feature recognizes `help`, `what can you do?`, and `what can you help me with?`, then explains that the assistant can help with tuition fee calculations, office information, and university rules.

**2. Paste the prompt you used:**

> Add a help feature to AssistantService. Recognize the inputs "help", "what can you do?", and "what can you help me with?". Return a helpful response listing tuition fee calculations, office information, and university rules. Keep the change small and add automated tests.

**3. Review the generated code manually. Document at least three changes you made:**

| # | What the AI generated | Problem you found | What you changed | Why |
|---|---|---|---|---|
| 1 | Help handling inside `handle()` after importing `route()`. | `router.py` was empty, so importing `route()` failed before the help request could be handled. | Moved help handling before the router import. | The help feature should handle its supported inputs without depending on the router. |
| 2 | Tests that initialized `AssistantService` normally. | The constructor imported `TemplateResponder`, but `responder.py` was empty, causing an `ImportError`. | Used `AssistantService.__new__()` in the experimental tests to bypass the constructor. | This isolated the help path from unrelated missing components during testing. |
| 3 | Help response classified as `Intent.UNKNOWN`, with exact-string matching. | There is no dedicated help intent, and inputs such as `help me` are not recognized. | Kept `Intent.UNKNOWN` for this experiment and documented the limitations. | Avoided expanding shared interfaces for a small experiment, while recording the limitations for future improvement. |

**Checklist:**

- [x] Interfaces respected?: the experiment reused the existing `Response` model and `Intent` enum.
- [x] New dependencies? None.
- [x] Secrets? None.
- [x] Logging of user data? No
- [x] Tests added and meaningful? 2 tests check the help response content and uppercase input.