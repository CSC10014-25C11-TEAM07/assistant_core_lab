# Lab 3 — AI extension review (giabao1001)

**1. Ask an AI coding assistant to extend your service with ONE feature:**
- Add an 'office list' (`Intent.OFFICE_LIST`) intent. When the user asks to list campus offices, the assistant should retrieve and return a formatted, alphabetized list of all available office names based on the loaded offices directory.

**2. Paste the prompt you used:**
- *"I am working on a Python service called assistant_core. Please write the Python code to extend my service with ONE new feature: Add an 'office list' intent. When the user asks 'list offices', the bot should return a list of all campus office names based on the loaded offices CSV. Show me the changes needed in router.py, models.py, and service.py, along with unit tests."*

**3. Review the generated code manually. Document at least three changes you made:**

| # | What the AI generated | Problem you found | What you changed | Why |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `names = ", ".join(self.offices.names)` in `service.py` | `self.offices.names` is a Python `set[str]`, which does not guarantee element ordering. The generated response had arbitrary ordering across runs, causing non-deterministic behavior and flaky test assertions. | Changed to `names = ", ".join(sorted(self.offices.names))` | Ensures deterministic, alphabetical ordering of office names for consistency and reliable automated testing. |
| 2 | Checked only exact English string `if text == "list offices":` in `router.py` | Vietnamese university students frequently query in Vietnamese (e.g. "danh sách văn phòng", "danh sach van phong") or with varied casing/whitespace, causing the bot to return `UNKNOWN`. | Added normalized alias set: `OFFICE_LIST_ALIASES = {"list offices", "danh sách văn phòng", "danh sach van phong"}` with `.strip().lower()`. | Enhances real-world usability and intent recognition across bilingual student inputs. |
| 3 | Returned `f"Offices: {names}."` without verifying if the directory contains offices | If `offices.csv` is empty or missing, `names` is an empty string, producing `"Offices: ."` which is grammatically broken and provides poor UX. | Added empty check: `answer = f"Offices: {', '.join(names)}." if names else "No offices available."` | Gracefully handles empty data edge cases while preserving standard `Response` contracts (`sources=[]`, `degraded=False`). |

**Checklist:**
- **Interfaces respected?** Yes. Adheres to `Response(answer=str, intent=Intent.OFFICE_LIST, sources=[], degraded=False)`.
- **New dependencies?** None. Uses existing standard library and Pydantic models.
- **Secrets?** None. No keys or credentials used or stored.
- **Logging of user data?** No. Respects privacy guidelines.
- **Tests added and meaningful?** Yes. Created 3 unit tests covering alphabetical sorting determinism, empty directory fallback, and Vietnamese alias recognition.

**Lưu ý thực hiện theo quy định nhóm:**
- Tính năng AI được sinh mã, kiểm thử và rà soát trong môi trường thử nghiệm riêng biệt.
- Sau khi hoàn thành đánh giá và lưu trữ kết quả kiểm chứng, mã nguồn thử nghiệm AI không được đưa vào PR chính thức để tránh xung đột mã nguồn chung (`router.py`, `models.py`, `service.py`) với các thành viên khác trong nhóm. Pull Request chỉ giữ lại mã nguồn module được phân công (`responder.py`, `test_responder.py`) và 3 tệp báo cáo cá nhân.
