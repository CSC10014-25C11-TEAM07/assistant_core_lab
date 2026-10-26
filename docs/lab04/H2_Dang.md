Ở Lab 3, tôi gọi service.handle() trực tiếp trong chương trình Python bằng một đối tượng Message.
Ở Lab 4, tôi gửi câu hỏi dưới dạng JSON qua HTTP bằng POST /v1/chat.
FastAPI nhận yêu cầu, gọi service xử lý rồi trả kết quả JSON kèm request_id cho phía gửi.
Nhờ HTTP, giao diện web hoặc ứng dụng điện thoại có thể sử dụng chức năng của trợ lý.
Cách này giúp nhóm phát triển giao diện và backend riêng, cùng dựa trên một API thống nhất.