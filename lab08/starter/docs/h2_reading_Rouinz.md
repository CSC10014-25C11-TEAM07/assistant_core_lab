# Lab 8 H2 — Rouinz

Em chưa nghĩ đến việc một đoạn tài liệu được truy xuất có thể chứa chỉ thị ẩn, dụ mô hình bỏ qua yêu cầu của người dùng và bịa mã trích dẫn để làm câu trả lời sai trông đáng tin.
Lớp grounding check trong parse_draft() sẽ chặn câu trả lời có mã nguồn ngoài allowed_ids bằng ProviderError, sau đó RagAnswerer thử lại và dùng trích đoạn nguồn đã truy xuất nếu đầu ra vẫn không hợp lệ.

## Reading references

- [pytest Get Started](https://docs.pytest.org/en/stable/getting-started.html)
- [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
