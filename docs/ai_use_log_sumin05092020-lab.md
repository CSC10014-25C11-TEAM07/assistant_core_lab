# AI Use Log (sumin05092020-lab)

- **Công cụ sử dụng:** GitHub Copilot Chat
- **Mục đích:** Hỗ trợ viết tính năng thông báo hạn nộp đơn vắng thi (exam absence) cho bài tập H1, bao gồm việc chỉnh sửa router, models và service.
- **Prompt đã dùng:** "I am working on a Python service called assistant_core. Please write the Python code to extend my service with ONE new feature: Add an 'exam absence' intent. When the user asks about being absent from an exam, the bot should tell students the deadline to submit the absence form based on the handbook. Show me the changes needed in router.py, models.py, and service.py."
- **Đánh giá:** Copilot làm rất tốt việc đọc hiểu ngữ cảnh, tự động tìm thấy luật "3 working days" trong sổ tay và thêm được 5 files (+98 -3 lines) giúp pass 23 tests. Tuy nhiên, vẫn cần tinh chỉnh thủ công để tránh hardcode logic.
