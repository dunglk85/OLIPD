# Story 1.2: Implementation of Security Middleware (Safetensors Filter)

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a SRE/Security Engineer,
I want the system to automatically verify model formats,
so that I can block potential malicious code execution from `.pickle` files.

## Acceptance Criteria

1. **[AC1]** Khi quét thư mục chứa mô hình, nếu phát hiện tệp tin có đuôi nguy hiểm (`.bin`, `.pth`, `.pkl`, `.pickle`), hệ thống phải đưa ra cảnh báo bảo mật.
2. **[AC2]** Chỉ cho phép tải các tệp trọng số mô hình nếu chúng có định dạng `.safetensors`.
3. **[AC3]** Hệ thống phải cho phép các tệp tin cấu hình thiết yếu (Whitelist) như: `config.json`, `generation_config.json`, `tokenizer.json`, `tokenizer_config.json`, `*.model`, `*.txt`.
4. **[AC4]** Module bảo mật phải cung cấp hàm kiểm tra nhanh (`validate_model_dir`) có thể tái sử dụng trong cả CLI và API.

## Tasks / Subtasks

- [x] **Task 1: Xây dựng Core Security Module (AC: #1, #2, #3)**
  - [x] Tạo tệp `src/olipd/core/security.py`
  - [x] Định nghĩa `FORBIDDEN_EXTENSIONS = {".bin", ".pth", ".pkl", ".pickle", ".pt"}`
  - [x] Định nghĩa `ALLOWED_METADATA_FILES = {".json", ".txt", ".model", ".tiktoken"}`
  - [x] Triển khai hàm `is_safe_file(filename: str) -> bool`
- [x] **Task 2: Triển khai Logic quét thư mục (AC: #4)**
  - [x] Triển khai hàm `validate_model_dir(model_path: Path) -> List[Path]`
  - [x] Hàm phải ném ngoại lệ `SecurityError` nếu tìm thấy tệp trong Blacklist
  - [x] Trả về danh sách các tệp hợp lệ nếu vượt qua vòng kiểm tra
- [x] **Task 3: Viết Unit Test cho Security Module (AC: #1, #2)**
  - [x] Tạo `tests/test_core_security.py`
  - [x] Test case: Thư mục chỉ chứa `safetensors` -> Pass
  - [x] Test case: Thư mục chứa `pytorch_model.bin` -> Fail (SecurityError)
  - [x] Test case: Thư mục chứa `config.json` -> Pass

## Dev Notes

- **Rủi ro Serialization:** Tệp `.pickle` trong Python (thường đi kèm đuôi `.bin` của PyTorch) cho phép thực thi mã tùy ý khi load. Việc ép buộc dùng `safetensors` là tiêu chuẩn bảo mật hiện đại của HuggingFace.
- **Implementation:** Sử dụng `pathlib.Path.suffix` và `pathlib.Path.iterdir()` để duyệt file hiệu quả.
- **Error Handling:** Định nghĩa custom exception `SecurityError` trong `core/security.py`.

### Project Structure Notes

- Module này nằm trong `core/` vì nó là quy tắc dùng chung cho toàn dự án.

### References

- [PRD Security Requirements](file:///d:/AI%20In%20Action/OLIPD/docs/planning-artifacts/prd.md#bao-mat-security)
- [FR10: Ngăn chặn tuyệt đối việc nạp mô hình .pickle](file:///d:/AI%20In%20Action/OLIPD/docs/planning-artifacts/epics.md#fr10-ngan-chan-tuyet-doi-viec-nap-mo-hinh-pickle)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
