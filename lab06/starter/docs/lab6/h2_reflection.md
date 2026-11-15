# H2 — RAG Reflection
1. RAG (Retrieval-Augmented Generation) là phương pháp giúp AI trả lời câu hỏi bằng cách tìm kiếm thông tin liên quan từ các tài liệu đáng tin cậy.
2. RAG giống như một kỳ thi mở sách, khi sinh viên được phép tra cứu tài liệu trước khi đưa ra câu trả lời.
3. Hệ thống RAG sẽ tìm những tài liệu phù hợp và cung cấp thông tin đó cho mô hình ngôn ngữ để tạo câu trả lời chính xác hơn.
4. Tuy nhiên, mô hình ngôn ngữ không thể tự bảo đảm rằng tất cả nguồn trích dẫn trong câu trả lời đều hợp lệ.
5. Vì vậy, chương trình cần kiểm tra các `source_ids` có thuộc danh sách `allowed_ids` hay không để tránh sử dụng những nguồn trích dẫn không hợp lệ.