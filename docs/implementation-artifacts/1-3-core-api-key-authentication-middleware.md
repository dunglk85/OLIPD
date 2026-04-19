# Story 1.3: Core API Key Authentication Middleware

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As an Admin,
I want to apply header-based authentication,
so that I can protect the API from unauthorized access.

## Acceptance Criteria

1. **[AC1]** Hệ thống phải quản lý cấu hình thông qua class `Settings` vững chắc, nạp dữ liệu từ biến môi trường `OLIPD_API_KEY`.
2. **[AC2]** Mọi request gửi tới API (ngoại trừ tài liệu `/docs`, `/redoc` và `/openapi.json`) phải chứa Header `X-API-Key`.
3. **[AC3]** Nếu Header thiếu hoặc Key không khớp với cấu hình, server phải trả về mã lỗi `401 Unauthorized`.
4. **[AC4]** Định dạng lỗi trả về phải tương thích với chuẩn OpenAI: `{"error": {"message": "Invalid API Key", "type": "invalid_request_error", ...}}`.
5. **[AC5]** Cung cấp cơ chế Dependency Injection trong FastAPI để các router dễ dàng yêu cầu xác thực.

## Tasks / Subtasks

- [x] **Task 1: Xây dựng Hệ thống Cấu hình (Config System) (AC: #1)**
  - [x] Tạo tệp `src/olipd/core/config.py`
  - [x] Triển khai class `Settings` kế thừa từ `Pydantic-Settings` `BaseSettings`
  - [x] Khai báo trường `api_key: SecretStr` (đọc từ `OLIPD_API_KEY`)
  - [x] Khai báo các trường cơ bản khác: `project_name`, `version`, `debug`
- [x] **Task 2: Triển khai Authentication Dependency (AC: #2, #3, #5)**
  - [x] Tạo tệp `src/olipd/api/deps.py`
  - [x] Sử dụng `fastapi.security.APIKeyHeader` để định nghĩa security scheme dùng header `X-API-Key`
  - [x] Triển khai hàm `get_api_key(api_key_header: str = Security(api_key_header))` thực hiện so sánh key
  - [x] Ném lỗi `HTTPException(status_code=401)` nếu không khớp
- [x] **Task 3: Viết Unit Test cho Authentication (AC: #3, #4)**
  - [x] Tạo `tests/test_api_auth.py`
  - [x] Sử dụng `TestClient` của FastAPI để giả lập request
  - [x] Test case: Truy cập thành công với Header đúng
  - [x] Test case: Lỗi 401 khi thiếu Header
  - [x] Test case: Lỗi 401 khi Key sai định dạng

## Dev Notes

- **Security:** Luôn sử dụng `pydantic.SecretStr` để đảm bảo API Key không bị in ra log một cách vô tình.
- **Dependency Injection:** Sử dụng mô hình `Depends()` của FastAPI giúp code sạch và dễ test (có thể dùng `dependency_overrides` trong tests).
- **Environment:** Cần cập nhật tệp `.env.example` với giá trị mẫu cho `OLIPD_API_KEY`.

### Project Structure Notes

- Module `core/config.py` là singleton chứa toàn bộ cấu hình dự án.

### References

- [Architecture Auth Patterns](file:///d:/AI%20In%20Action/OLIPD/docs/planning-artifacts/architecture.md#authentication--security)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/first-steps/)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
