# AI Use Log (giabao1001)

- **Họ và tên:** Trần Gia Bảo
- **GitHub Username:** `giabao1001`
- **Công cụ hỗ trợ:** Claude Code (Anthropic Claude)
- **Mục đích sử dụng:**
  1. Hỗ trợ xây dựng giao diện `Responder` (Protocol), triển khai `TemplateResponder` và `StubLLMResponder` cùng hệ thống unit tests kiểm chứng cơ chế fallback trên `AssistantService` theo yêu cầu Lab 3.
  2. Thực hiện bài tập H1: Hỗ trợ sinh mã tính năng mở rộng danh sách văn phòng trường (`office_list`), rà soát kỹ thuật và tối ưu hóa giải pháp.
- **Prompt sử dụng cho bài tập H1:**
  *"I am working on a Python service called assistant_core. Please write the Python code to extend my service with ONE new feature: Add an 'office list' intent. When the user asks 'list offices', the bot should return a list of all campus office names based on the loaded offices CSV. Show me the changes needed in router.py, models.py, and service.py, along with unit tests."*
- **Đánh giá kết quả sinh mã từ AI:**
  - **Điểm tốt:** AI nắm bắt nhanh cấu trúc kiến trúc của dự án, tuân thủ đúng định dạng `Response` và bổ sung giá trị enum `Intent.OFFICE_LIST` hợp lý.
  - **Điểm cần cải thiện:** Mã do AI sinh gặp vấn đề về tính bất định (lấy thứ tự ngẫu nhiên từ `set`), chưa hỗ trợ ngôn ngữ tiếng Việt tự nhiên cho sinh viên, và bỏ sót trường hợp dữ liệu rỗng.
- **Các cải tiến đã áp dụng:**
  - Chuẩn hóa thứ tự tên văn phòng bằng `sorted()` để đảm bảo kết quả phản hồi luôn nhất quán.
  - Mở rộng tập từ khóa khớp câu hỏi với các biến thể tiếng Việt có dấu và không dấu.
  - Bổ sung xử lý biên khi danh sách văn phòng rỗng.
- **Xử lý mã nguồn theo quy định nhóm:**
  - Toàn bộ quá trình sinh mã và thử nghiệm tính năng H1 được thực hiện trong môi trường độc lập.
  - Sau khi kiểm thử đạt 3/3 test và ghi nhận báo cáo, mã nguồn thử nghiệm AI đã được loại bỏ khỏi cây mã nguồn chính thức để giữ Pull Request sạch sẽ, chỉ bao gồm module `responder.py`, `tests/test_responder.py` và 3 tệp báo cáo cá nhân.

---

## Lab 06 — AI Services & RAG

- **Công cụ hỗ trợ:** Antigravity / Claude Code
- **Mục đích sử dụng:**
  1. Hỗ trợ rà soát logic triển khai S1 (`build_index`) và S2–S3 (`search`) trong `mini_search.py`.
  2. Hỗ trợ hoàn thiện các chốt chặn an toàn: A1 (`abstain` trước khi gọi LLM) và A2 (`grounding check` kiểm tra trích dẫn nguồn).
  3. Xây dựng 5 câu hỏi đánh giá mới cho H1 (3 câu miền quy định trường học, 2 câu từ chối) và phân tích sâu thực nghiệm H3 (ảnh hưởng của chuẩn hóa bỏ hậu tố 's' đến độ chính xác BM25).
- **Prompt chính:**
  *"Analyze the Lab 06 RAG pipeline requirements. Provide clean implementations for S1-S3, A1, and A2 ensuring strict validation and zero hallucinations. Propose 5 diverse test queries for H1 covering handbook regulations, out-of-scope questions, and privacy requests. Evaluate the trailing-s normalization on BM25 retrieval."*
- **Đánh giá kết quả từ AI:**
  - **Điểm tốt:** AI đề xuất cấu trúc giải pháp chính xác, điều kiện kiểm tra tập nguồn trích dẫn `set(draft.source_ids) <= allowed_ids` gọn gàng và phân tích rõ tại sao H3 gây ra hiện tượng hồi quy (regression) trên câu hỏi E20.
  - **Điểm cần lưu ý & cải tiến của người học:** Cần tinh chỉnh câu hỏi E23 ("How can I reset my password online with recovery email") để tránh bị router hiểu nhầm thành thực thể văn phòng `IT Helpdesk`, bảo đảm truy xuất đúng phân đoạn quy định `S26#2`.
- **Kiểm chứng độc lập:**
  - `lab06/practice/test_mini_search.py`: 4/4 test passed.
  - `lab06/starter/tests/`: 42/42 test passed.
  - `eval/compare_paths.py`: 21/25 passed trên retrieval và llm (stub), không có câu hỏi H1 nào thất bại.
