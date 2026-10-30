Ở Lab 3, em gọi trực tiếp service.handle() trong chương trình Python và nhận lại một đối tượng Response. <br>
Ở Lab 4, em gửi dữ liệu JSON qua POST /v1/chat; phía server vẫn gọi service.handle() rồi trả kết quả dưới dạng JSON. <br>
Khi dùng API, dữ liệu đầu vào được kiểm tra và kết quả hoặc lỗi được biểu diễn bằng phản hồi có mã trạng thái HTTP. <br>
Nhóm có thể dùng chung API cho giao diện web hay ứng dụng khác mà không cần các bên cùng chạy mã Python của service. <br>
Cách này giúp tách việc làm giao diện khỏi xử lý nghiệp vụ, nhưng cần tính thêm độ trễ, thời gian chờ và lỗi kết nối.
