# H2 — RAG Reflection (5 dòng)

1. RAG (Retrieval-Augmented Generation) giống hệt một bài thi mở sách: thay vì bắt mô hình AI phải nhớ toàn bộ kiến thức từ trí nhớ, ta cung cấp cho AI đúng trang tài liệu chứa thông tin trước khi yêu cầu viết câu trả lời.
2. Khi sinh viên đặt câu hỏi, bước đầu tiên code tìm kiếm (dùng DSA: từ điển, tập hợp, BM25) sẽ quét kho tài liệu nội bộ và trích xuất ra các đoạn văn bản liên quan nhất.
3. Nếu không tìm thấy đoạn văn nào đủ điểm phù hợp, hệ thống lập tức từ chối trả lời (abstain) và chuyển tiếp tới phòng đào tạo, tuyệt đối không gọi mô hình AI để tránh bịa đặt thông tin.
4. Khi có tài liệu phù hợp, mô hình AI chỉ đóng vai trò diễn đạt lại nội dung cho tự nhiên và thân thiện dựa trên các đoạn trích đó, đồng thời phải trả về cấu trúc JSON chứa mã nguồn trích dẫn.
5. Một điểm mấu chốt mà code kiểm tra nhưng mô hình AI không tự bảo đảm được là Grounding Check: code xác thực mọi mã nguồn (source_ids) AI trích dẫn bắt buộc phải thuộc danh sách các đoạn văn đã cung cấp, ngăn chặn hoàn toàn việc AI tự tạo ra nguồn trích dẫn không có thật.
