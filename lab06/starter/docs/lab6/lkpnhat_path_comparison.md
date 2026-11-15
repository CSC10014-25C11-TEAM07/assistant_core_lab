# Lab 06 Path Comparison — Lê Kim Phúc Nhật (lkpnhat2514-glitch)

## 1. Kết quả so sánh 3 đường dẫn trả lời (20 câu hỏi cơ sở)

| Đường dẫn (Path) | Đúng (Correct /20) | Từ chối đúng (Abstain OK /5) | p50 (ms) | Max (ms) | Các câu thất bại (Failures) |
|---|---:|---:|---:|---:|---|
| Deterministic | 7/20 | 5/5 | 0.0 | 0.5 | E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15 |
| Retrieval | 16/20 | 4/5 | 0.0 | 0.1 | E13 E14 E15 E19 |
| LLM (stub) | 16/20 | 4/5 | 0.1 | 0.4 | E13 E14 E15 E19 |

### Ba câu nhận xét (theo yêu cầu PDF trang 16):
1. **Lựa chọn đường dẫn cho sổ tay sinh viên:** Đối với các câu hỏi về sổ tay sinh viên và chính sách học vụ, tôi sẽ chọn đường dẫn **Retrieval** (kết hợp cơ chế fallback an toàn) để triển khai thực tế.
2. **Lý do lựa chọn:** Đường dẫn Retrieval đạt độ chính xác tương đương LLM stub (16/20) mà tốc độ xử lý nhanh hơn nhiều (p50: 0.0 ms so với 0.1-0.2 ms), trích dẫn nguyên văn chính xác từ tài liệu đã duyệt và hoàn toàn loại trừ rủi ro sinh thông tin sai lệch (hallucination) khi tích hợp mô hình ngôn ngữ lớn thực tế.
3. **Lỗi ưu tiên khắc phục:** Tôi ưu tiên khắc phục lỗi **E19** ("is the final exam open-book") vì đây là câu hỏi ngoài phạm vi tài liệu, nhưng một đoạn về vắng thi có độ tương đồng từ khóa cao khiến hệ thống trả lời sai thay vì từ chối; cần tinh chỉnh ngưỡng điểm `RETRIEVAL_MIN_SCORE` hoặc bổ sung bộ kiểm tra độ liên quan trước khi trả về.

---

## 2. H1 — Đánh giá sau khi bổ sung 5 câu hỏi mới (Tổng cộng 25 câu)

Bộ đánh giá mở rộng gồm 25 câu hỏi (7 câu cần từ chối):

| Đường dẫn (Path) | Đúng (Correct /25) | Từ chối đúng (Abstain OK /7) | p50 (ms) | Max (ms) | Các câu thất bại (Failures) |
|---|---:|---:|---:|---:|---|
| Deterministic | 9/25 | 7/7 | 0.0 | 0.4 | E01 E02 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15 E21 E22 E23 |
| Retrieval | 20/25 | 6/7 | 0.0 | 0.1 | E13 E14 E15 E19 E23 |
| LLM (stub) | 20/25 | 6/7 | 0.1 | 0.4 | E13 E14 E15 E19 E23 |

### Giải thích câu thất bại trong 5 câu mới:
- Câu **E23** ("What is the replacement fee for a lost student card?") bị thất bại ở cả 3 đường dẫn do router nhận diện từ khóa "fee" và chuyển nhầm câu hỏi sang luồng tính học phí (`calc_fee`), khiến trợ lý yêu cầu nhập số tín chỉ thay vì chuyển sang luồng tra cứu đoạn `S26#3` trong Campus Services.
