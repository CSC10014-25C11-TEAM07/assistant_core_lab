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
