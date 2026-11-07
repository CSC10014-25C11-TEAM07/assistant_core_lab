# Lab 5 - Báo cáo kiểm thử và review tích hợp (Bao04)

Người phụ trách: **Trần Gia Bảo - Bao04 - `giabao1001`**. Ngày kiểm thử: **07/11/2026**.

**Kết luận: chưa đủ điều kiện merge bản tích hợp hoặc tạo tag `v0.5-data`.**
H1 cá nhân đã đạt 15/15. R1 đã được tích hợp qua PR #49 vào main `724c228`. PR #64 của Nhật (`6c1afec`) triển khai R2 và đạt 27/27 test Assistant gốc, 46/46 khi thêm test Bao04. Đã gửi review REQUEST_CHANGES vì Q12 trong phần H1 đi kèm còn thiếu sắp xếp theo tên môn khi bằng số đăng ký. D1-D3 và bản tích hợp cuối vẫn chờ nghiệm thu.

Cập nhật review Nhật: [kết quả và lỗi tái hiện ở PR #64](review_pr64_giabao1001.md). Các số liệu main `945ebbf` bên dưới là kết quả baseline trước khi R1 được merge, không phải trạng thái main mới nhất.

## Phạm vi và phiên bản

- Căn cứ: bảng phân công `Lab05_Bang_phan_cong_nhom.docx.md` và tutorial `CSC10014_2026_Lab05_Data_SQL_Persistence_Tutorial.docx.pdf`, đặc biệt phần C, D, E và yêu cầu nộp bài. Theo phân công, Bao04 làm H1 cá nhân và kiểm thử/review tích hợp; phần triển khai D1-D3 thuộc Tân, R1 thuộc Bao06, R2 thuộc Nhật.
- Baseline đã pull ban đầu: `945ebbf030751884d9e3a1f6b4a9ae9d28980361`, gồm starter chính thức từ PR #51. Remote main được fetch lại ở `724c228f90436fba3fc4c03bf5900458d878ca50` khi review Nhật; working branch QA được giữ nguyên.
- H1 Bao04: `fdbd652a33a23d93c38faa9da0c3a2ef8ebf8222`, [PR #56](https://github.com/CSC10014-25C11-TEAM07/assistant_core_lab/pull/56), branch `feat/lab05-h1-giabao1001`.
- R1: [PR #49](https://github.com/CSC10014-25C11-TEAM07/assistant_core_lab/pull/49), head `65c10e36b1916830efc399ff027d43c4e660f8f1`, branch `feat/lab05-r1-rouinz`.
- Môi trường: Python 3.12.14, SQLite 3.53.1, SQLModel 0.0.22, SQLAlchemy 2.0.57; các dependency trực tiếp đúng `lab05/starter/requirements.txt`.

## Kết quả thực tế

| Đối tượng kiểm tra | Bộ kiểm thử | Kết quả | Minh chứng |
| --- | --- | --- | --- |
| H1 Bao04 tại `fdbd652` | `python check.py` | **15/15** | [Log H1](evidence/h1-giabao1001.txt) |
| Main: D1-D3 | 5 test được cung cấp | **1 pass, 4 fail** | [Log practice gốc](evidence/main-practice-official.txt) |
| Main: D1-D3 | 5 test gốc + 10 test Bao04 | **2 pass, 13 fail** | [Log practice + QA](evidence/main-practice-with-qa.txt) |
| Main: Assistant | 27 test được cung cấp | **25 pass, 2 fail** | [Log starter gốc](evidence/main-starter-official.txt) |
| Main: Assistant | 27 test gốc + 19 test Bao04 | **32 pass, 14 fail** | [Log starter + QA](evidence/main-starter-with-qa.txt) |
| Main + `db.py` từ PR #49 | 27 test được cung cấp | **26 pass, 1 fail (R2)** | [Log R1 gốc](evidence/r1-starter-official.txt) |
| Main + `db.py` từ PR #49 | 27 test gốc + 19 test Bao04 | **37 pass, 9 fail (R2)** | [Log R1 + QA](evidence/r1-starter-with-qa.txt) |
| Lab 3 ở root | `python -m pytest -q` | **66 pass** | Chạy trực tiếp trên working tree |

Các lỗi main tái hiện `NotImplementedError` tại các TODO tương ứng; không bỏ qua test hay đổi kỳ vọng để làm xanh kết quả. Starter có một `DeprecationWarning` từ Starlette/AnyIO, không ảnh hưởng kết quả.

PR #49 xuất phát từ trước khi starter được thêm vào main. Để kiểm tra riêng R1, tạo bản sao Lab 5 của main trong thư mục tạm rồi thay **duy nhất** `starter/src/assistant_api/db.py` bằng file ở commit `65c10e3`; thêm hai file test Bao04 vào bản sao. Đây là kiểm tra tương thích trên snapshot, **chưa phải một merge thành công**. Log giữ nguyên kết quả/exit code và thay đường dẫn máy bằng `<repo>` / `<review-tmp>`.

## Các ca kiểm thử bổ sung

`lab05/practice/test_school_repo_integration.py` bổ sung **10 ca**:

- D1: tên có dấu nháy, payload SQL injection ở tên/chương trình được giữ nguyên như dữ liệu; kết nối SQLite thứ hai đọc được ngay bản ghi để xác nhận `commit()`.
- Ví dụ có sẵn: lọc chương trình không bị payload `OR 1=1` làm lộ toàn bộ danh sách.
- D2: toàn `NULL` trả `None`; bỏ qua `NULL` nhưng tính cả điểm 0; trung bình được làm tròn hai chữ số; mã môn dạng injection không khớp dữ liệu.
- D3: sinh viên không tồn tại hoặc ID dạng injection trả danh sách rỗng; hai môn khác mã nhưng trùng tên đều được giữ; thứ tự tên môn và điểm `None` đúng.

`lab05/starter/tests/test_feedback_integration.py` bổ sung **19 ca**:

- R1: POST với từng rating -1/0/1 trả 201, có ID/timestamp và bản ghi thực trong DB; comment Unicode/dấu nháy được giữ nguyên. Request ID lạ trả 404 và không ghi bản ghi. Rating ngoài khoảng, ID rỗng và comment hơn 500 ký tự trả 422, không ghi DB.
- Persistence: đóng engine rồi dùng **tiến trình Python mới** đọc file SQLite, độc lập với R2. Kiểm tra luồng API sau khi tạo lại ứng dụng/engine trên cùng file DB.
- R2: DB rỗng; sắp xếp `created_at DESC` với thời gian cố định được chèn lệch thứ tự ID; giới hạn 0/1/2/100; dữ liệu vẫn đọc được sau khi Session đóng.
- API R2: thiếu/sai API key trả 401; key hợp lệ trả 200; `limit=2` được truyền xuống repository và trả đúng thứ tự/định dạng. Seed feedback trực tiếp bằng SQLModel để lỗi R1 không che mất lỗi R2.

Hai phép thử persistence có phạm vi riêng: tiến trình mới kiểm tra độ bền dữ liệu trên đĩa; TestClient kiểm tra tạo lại ứng dụng và engine. Cả hai đã đạt trên commit PR #64. Chu trình dừng/chạy lại Uvicorn qua HTTP thật trên bản tích hợp cuối vẫn chưa được xác nhận.

## Lỗi và kết luận review

| Mã | Mức độ | Bằng chứng / tác động | Hướng xử lý / người phụ trách |
| --- | --- | --- | --- |
| B04-01 | Chặn nghiệm thu | `school_repo.py`: D1, D2, D3 đều `raise NotImplementedError`; 4/5 test gốc thất bại, gồm injection. | Tân hoàn tất ba hàm, dùng tham số `?`, commit D1, làm tròn D2, JOIN D3; chạy lại cả hai file test. |
| B04-02 | Đã xử lý | R1 chưa triển khai ở baseline `945ebbf`; nay đã merge qua PR #49 vào `724c228`. | Kiểm thử R1/R2 trên PR #64 đạt 46/46 test. |
| B04-03 | Đã đạt trên PR, chờ merge | R2 của PR #64 trả danh sách đúng thứ tự, limit và xác thực API key; test độc lập đạt. | Chờ tác giả sửa lỗi H1 Q12 trong PR kết hợp và Tech Lead quyết định tích hợp. |
| B04-04 | Đã xử lý | Conflict add/add của PR #49 đã được giải quyết tại `cd5161f`; PR đã merge vào `724c228`. | Bảo toàn R1 khi tích hợp R2 và chạy lại test trên commit cuối. |

Review phần R1 ban đầu ở `65c10e3`: truy vấn kiểm tra interaction trước khi ghi; ID lạ trả `None`; dùng SQLModel `add`, `commit`, `refresh` rồi trả đối tượng. Test độc lập xác nhận POST 201/404, dữ liệu hợp lệ và persistence đều đạt. Lần kiểm tra này chỉ lưu kết quả trong repo. Sau khi R1 được merge, Bao04 đã gửi review REQUEST_CHANGES lên PR #64 cho lỗi sắp xếp Q12; phần R2 không có lỗi chặn được phát hiện.

D1-D3 và review bản tích hợp cuối vẫn chờ nghiệm thu. Kết quả đạt của R1/R2 trên PR #64 không thay thế kiểm thử các phần còn lại của nhóm.

## Kiểm chứng chất lượng bộ test Bao04

Đã chạy bộ test trên **bản tham chiếu tạm**, triển khai D1-D3/R2 theo hành vi mô tả trong tutorial và dùng R1 từ PR #49. Kết quả: practice **15/15 test**, Assistant **46/46 test**; xem [log practice tham chiếu](evidence/reference-only-practice-with-qa.txt) và [log Assistant tham chiếu](evidence/reference-only-starter-with-qa.txt).

Mục đích là kiểm tra bộ test có chấp nhận hành vi yêu cầu. **Các số pass này không phải kết quả của main/PR tích hợp và không thay thế việc test mã của Tân/Nhật.** Mã tham chiếu chỉ tồn tại trong thư mục tạm, không đưa vào commit. Ruff check/format của hai file test mới đạt; `git diff --check` đạt.

## Chạy lại khi mã nhóm sẵn sàng

Từ root, dùng Python của môi trường đã cài `lab05/starter/requirements.txt`:

```sh
python -m pip install -r lab05/starter/requirements.txt
```

Chạy trong `lab05/practice/`:

```sh
python make_school_db.py
python check.py
python -m pytest -q test_school_repo.py
python -m pytest -q test_school_repo.py test_school_repo_integration.py
```

H1 phải được kiểm tra trên branch/PR H1 cá nhân. Branch QA xuất phát từ main nên không chứa đáp án H1; nếu cần kiểm tra H1 Bao04 khi đang ở branch QA, xuất file đáp án sang thư mục tạm rồi dùng đối số của checker:

```sh
git show fdbd652:lab05/practice/my_answers.sql > /tmp/lab05-h1-giabao1001.sql
python check.py /tmp/lab05-h1-giabao1001.sql
```

`check.py` chỉ in điểm, vẫn có thể trả exit code 0 khi đáp án sai; phải xác nhận dòng **`Score: 15/15`**. `make_school_db.py` tạo lại dữ liệu practice; chỉ chạy trên bản dữ liệu bài tập có thể tái tạo.

Chạy trong `lab05/starter/`:

```sh
python -m pytest -q
python -m pytest -q tests/test_feedback_integration.py
```

Chạy ở root chỉ chạy bộ test Lab 3, không thay thế hai lệnh trên vì mỗi lab có package/config pytest riêng.

Điều kiện xác nhận tích hợp cuối:

- [x] H1 Bao04 đạt 15/15 và có PR riêng #56.
- [x] Hoàn tất test bổ sung, log, báo cáo và review sơ bộ R1.
- [ ] D1-D3 của nhóm đạt 5/5 test gốc và 10/10 test bổ sung.
- [ ] R1/R2 được tích hợp, Assistant đạt 27/27 test gốc và 19/19 test bổ sung.
- [x] Review PR R2 #64 trên đúng commit `6c1afec`, lưu log và gửi kết quả lên GitHub.
- [ ] Review lại Q12 sau khi sửa và diff cuối của PR tích hợp trên đúng commit đã kiểm thử.
- [ ] Kiểm tra API qua Uvicorn: POST 201, ID lạ 404, GET thiếu/sai key 401, key đúng 200; restart server vẫn đọc được feedback.
- [ ] Cập nhật báo cáo theo commit tích hợp thực tế; Tech Lead chọn một H1, quyết định merge và tạo tag `v0.5-data`.
