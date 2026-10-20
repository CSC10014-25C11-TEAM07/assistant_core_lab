# AI Use Log – H1

## 1. AI tool used

- Tool: ChatGPT / GitHub Copilot
- Task: Generate a prototype for a new feature in the `assistant_core` service.

## 2. Prompt and purpose

I asked the AI coding assistant to propose a new student scholarship lookup feature that follows the existing service architecture.

The goal was to explore how the feature could be implemented and identify potential issues through manual review.

## 3. AI-generated output

The AI proposed changes to the service logic and potentially related models or routing components.

The generated code was treated as a prototype and reviewed before deciding whether it was suitable for the project.

## 4. Human review

I reviewed the generated code for:

1. Hard-coded values and maintainability.
2. Input validation and error handling.
3. Missing unit tests and edge cases.

## 5. Actions taken

I documented the proposed improvements in the AI Extension Review report and excluded experimental AI-generated code from the final pull request to avoid conflicts with the team's shared codebase.

## 6. Limitations

The AI-generated code requires human verification. Its correctness, compatibility, and test coverage should not be assumed without actual testing.