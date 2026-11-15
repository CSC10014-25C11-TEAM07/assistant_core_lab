# AI Use Log (Nhat)

## Lab 05
- **Tool used:** ChatGPT (hoặc điền tên công cụ bạn dùng, ví dụ: Copilot, Gemini)
- **Purpose:** To assist in designing and implementing the `help` feature. This feature enables the `AssistantService` to recognize user requests for assistance (e.g., "help", "what can you do?") and returns a structured list of available capabilities (fees, offices, and rules).
- **Prompt used:** "Add a 'help' feature to the AssistantService to list what the bot can do. Recognize inputs like 'help' or 'what can you do?'. Return a list of features. Keep it simple and provide tests."
- **Evaluation:** The AI effectively generated the core logic to detect help requests, but its implementation violated the service architecture. It modified `router.py` to directly return a plain text string instead of utilizing the required `Response` and `Intent` models. Additionally, the AI failed to update the `Intent` Enum in `models.py` to include `Intent.HELP`. I manually refactored the code to adhere to the Single Responsibility Principle by keeping only `Intent.HELP` in the router and moving the Markdown-formatted response generation into `service.py`. I also expanded the AI's single test case by using `@pytest.mark.parametrize` to ensure robustness against various phrasing. After these corrections, the test suite passed and the code met the architectural standards.

## Lab 06 — S1–S3, A1–A2, Path Comparison & H1–H2 Individual Submission
- **Tool used:** Antigravity / Claude 3.5 Sonnet
- **Purpose:** 
  1. Verify inverted index (`build_index`) and ranking algorithm (`search`) for Mini Search (S1–S3).
  2. Verify TODO A1 early abstention logic in `answerer.py` and TODO A2 citation grounding verification in `llm.py`.
  3. Execute three-path evaluation via `compare_paths.py` on 20 baseline questions and 25 questions with H1 extensions.
  4. Formulate the three required observations and the 5-line RAG educational reflection (H2).
- **Prompt used:** "Analyze three-path comparison results between deterministic, retrieval, and LLM stub paths. Formulate concise observations on handbook question handling and compose a 5-line analogy of RAG as an open-book exam highlighting the grounding check."
- **Evaluation:** AI assistance helped structure the evaluation report and ensure that all strict constraints (e.g., exactly 5 lines for H2, 3 specific sentences for Part F, proper JSON schema and error handling for A2) were fully met. All code, test suites (4 practice tests, 42 starter tests), and comparison evaluations were run and verified independently on the local environment.
