# Homework H2 — RAG Reflection (Bao04 / giabao1001)

1. RAG biến việc hỏi đáp của AI từ một bài thi vấn đáp đóng sách (nơi mô hình phải nhớ lại kiến thức và dễ bịa chuyện) thành một bài thi mở sách có sẵn tài liệu chuẩn xác.
2. Khi sinh viên đặt câu hỏi, hệ thống tìm kiếm trong các tài liệu quy định chính thức của trường để truy xuất các đoạn văn bản chứa câu trả lời liên quan nhất.
3. Các đoạn trích dẫn này được đính kèm vào đề bài để mô hình ngôn ngữ đọc và diễn đạt lại thành câu trả lời tự nhiên, súc tích cho sinh viên.
4. Một bước kiểm tra cốt lõi mà mã nguồn hệ thống thực thi nhưng mô hình AI không tự làm là kiểm định nguồn trích dẫn (grounding check): bắt buộc câu trả lời chỉ được trích dẫn các tài liệu thực sự được truy xuất và từ chối nếu không có căn cứ.
5. Nhờ đó, trợ lý ảo ngăn ngừa hoàn toàn ảo giác (hallucination) và chủ động từ chối trả lời để chuyển tiếp tới phòng Đào tạo khi gặp câu hỏi nằm ngoài phạm vi tài liệu.
