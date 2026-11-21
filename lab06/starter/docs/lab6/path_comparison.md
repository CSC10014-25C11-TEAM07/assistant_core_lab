# Lab 06 Path Comparison

Bộ đánh giá gồm 20 câu hỏi, trong đó có 5 câu cần từ chối.

| Cách trả lời | Đúng | Từ chối đúng | p50 (ms) | Max (ms) |
|---|---:|---:|---:|---:|
| Deterministic | 7/20 | 5/5 | 0.0 | 0.6 |
| Retrieval | 16/20 | 4/5 | 0.0 | 0.1 |
| LLM (stub) | 16/20 | 4/5 | 0.2 | 0.6 |

1. Mình chọn retrieval cho các câu hỏi về sổ tay sinh viên.
2. Trong lần chạy này, retrieval đúng 16/20 câu, bằng LLM stub, và có thời gian phản hồi trung vị thấp hơn.
3. Mình sẽ ưu tiên sửa E19 vì hệ thống vẫn trả lời câu hỏi về thi mở sách dù tài liệu truy xuất không đủ để kết luận.
## H1 — Đánh giá sau khi thêm 5 câu

Bộ đánh giá hiện có 25 câu, trong đó 7 câu cần từ chối.

| Cách trả lời | Đúng | Từ chối đúng | p50 (ms) | Max (ms) |
|---|---:|---:|---:|---:|
| Deterministic | 9/25 | 7/7 | 0.0 | 0.6 |
| Retrieval | 20/25 | 6/7 | 0.0 | 0.1 |
| LLM (stub) | 20/25 | 6/7 | 0.2 | 0.5 |

Trong 5 câu mới, E23 thất bại ở cả ba cách vì router chuyển câu hỏi về phí cấp lại thẻ sinh viên sang luồng tính học phí, nên trợ lý hỏi số tín chỉ thay vì lấy thông tin từ mục `S26#3`.