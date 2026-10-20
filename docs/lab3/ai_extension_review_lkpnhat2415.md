# AI Extension Review (H1)

**Feature requested:** Add a `help` feature to list what the bot can do.

**AI Tool used:** Gemini

### 3 Improvements made to the AI-generated code:

1. **Refactoring for Separation of Concerns (Architecture):**
   * **AI's Approach:** The AI wrote the code so that `router.py` directly returned the full help text string. 
   * **My Improvement:** I refactored the code to adhere strictly to the Single Responsibility Principle. I updated `router.py` to only return `Intent.HELP`. I then moved the actual help message generation into `service.py` to keep the routing layer clean and separated from the presentation/response logic.

2. **Enhancing Response Formatting (UX/UI Readiness):**
   * **AI's Approach:** The AI provided a single, plain, and unformatted string (e.g., "I can help with tuition fees, finding offices, and school rules.").
   * **My Improvement:** I improved the response payload by utilizing structured Markdown with bullet points. This makes the output much more readable and prepares the response for better rendering in the UI layer (which will be built in Lab 7).

3. **Expanding Test Coverage with Parameterization (Testing):**
   * **AI's Approach:** The AI provided only one basic test case checking the exact keyword "help" in `tests/test_router.py`.
   * **My Improvement:** I improved the test suite by utilizing `@pytest.mark.parametrize` to cover multiple variations and edge cases of user inputs (e.g., "can you help me?", "what can you do?", "commands", "how does this work?"). This ensures the router is robust and handles natural language variations effectively.