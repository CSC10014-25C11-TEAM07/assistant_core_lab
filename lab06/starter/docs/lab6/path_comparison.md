# Lab 6 — So sánh ba phương án trả lời

Kết quả từ `python eval/compare_paths.py` với BM25, ngưỡng 2.0 và LLM stub. Độ trễ tính bằng ms và làm tròn đến một chữ số thập phân.

| Phương án | Đúng | Từ chối đúng | p50 (ms) | Max (ms) | Câu chưa đạt |
|---|---:|---:|---:|---:|---|
| deterministic | 7/20 | 5/5 | 0.0 | 0.6 | E01, E02, E05–E15 |
| retrieval | 16/20 | 4/5 | 0.0 | 0.0 | E13, E14, E15, E19 |
| llm (stub) | 16/20 | 4/5 | 0.2 | 1.0 | E13, E14, E15, E19 |

Mình chọn retrieval cho câu hỏi về sổ tay sinh viên. Trong lần chạy này, retrieval đúng 16/20 như LLM stub, trả lời bằng trích đoạn có nguồn và có độ trễ thấp hơn. Mình sẽ ưu tiên sửa E19 để trợ lý hỏi tên môn hoặc thể lệ của kỳ thi cụ thể trước khi kết luận bài thi có mở sách hay không.

## H1 — Chạy lại sau khi thêm năm câu

E21–E23 có mã nguồn đối chiếu từ kho tài liệu, còn E24–E25 yêu cầu từ chối vì ngoài phạm vi.

| Phương án | Đúng | Từ chối đúng | p50 (ms) | Max (ms) | Câu chưa đạt trong H1 |
|---|---:|---:|---:|---:|---|
| deterministic | 9/25 | 7/7 | 0.0 | 0.4 | E21, E22, E23 |
| retrieval | 20/25 | 6/7 | 0.0 | 0.1 | E23 |
| llm (stub) | 20/25 | 6/7 | 0.2 | 0.5 | E23 |

Deterministic không tra kho tài liệu cho E21–E22, còn E23 bị chuyển sang nhánh tính học phí ở cả ba phương án dù BM25 xếp đúng nguồn `F26#3` đầu tiên khi truy vấn trực tiếp.
