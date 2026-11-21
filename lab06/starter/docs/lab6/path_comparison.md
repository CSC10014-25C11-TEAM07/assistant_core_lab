# Lab06 — Part F: Path Comparison
## 1. Kết quả đánh giá

Chạy lệnh:

`python eval/compare_paths.py`

| Path | Correct | Abstain OK | p50 (ms) | Max (ms) |
|---|---|---|---|---|
| Deterministic | 9/25 | 7/7 | 0.0 | 0.6 |
| Retrieval | 20/25 | 6/7 | 0.0 | 0.1 |
| LLM (stub) | 20/25 | 6/7 | 0.2 | 0.7 |

## 2. Các trường hợp chưa đạt

- **Deterministic:** E01, E02, E05, E06, E07, E08, E09, E10, E11, E12, E13, E14, E15, E21, E22, E23.
- **Retrieval:** E13, E14, E15, E19, E23.
- **LLM (stub):** E13, E14, E15, E19, E23.

## 3. Nhận xét (3 câu)

1. Đối với handbook, nên ưu tiên phương pháp Retrieval vì đạt 20/25 câu đúng, cao hơn Deterministic (9/25), đồng thời có độ trễ thấp trong lần đánh giá này.
2. Phương pháp LLM (stub) cũng đạt 20/25 câu đúng nhưng có độ trễ cao hơn Retrieval, trong khi Deterministic xử lý tốt cả 7/7 trường hợp cần từ chối.
3. Lỗi cần ưu tiên khắc phục là trường hợp từ chối chưa chính xác của Retrieval và LLM (stub), đồng thời kiểm tra các câu E13, E14, E15, E19 và E23 để cải thiện khả năng truy xuất thông tin.