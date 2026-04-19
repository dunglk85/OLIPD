# Story 1.1: Project Scaffold & Dependency Management

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Developer,
I want to initialize a standard `src/` layout and `pyproject.toml`,
so that the project can be installed via `pip` and easily maintained.

## Acceptance Criteria

1. **[AC1]** Toàn bộ cấu trúc thư mục (`src/olipd/`) phải khớp 100% với bản thiết kế kiến trúc [Source: architecture.md#Project Structure & Boundaries].
2. **[AC2]** Các thư viện cốt lõi (`fastapi`, `vllm==0.4.0`, `typer`, `transformers==4.40.0`) được cài đặt chính xác qua `pyproject.toml`.
3. **[AC3]** Lệnh `pip install -e .` hoạt động thành công, cho phép import `olipd` từ bất kỳ đâu trong môi trường ảo.

## Tasks / Subtasks

- [x] **Task 1: Tạo cấu trúc thư mục chuẩn (AC: #1)**
  - [x] Tạo module chính: `src/olipd/`
  - [x] Tạo các sub-modules: `api/`, `core/`, `services/`, `schemas/`, `cli/`
  - [x] Tạo thư mục `tests/` và `storage/benchmarks/`
  - [x] Tạo các tệp `__init__.py` cần thiết
- [x] **Task 2: Cấu hình Dependency & Packaging (AC: #2, #3)**
  - [x] Khởi tạo `pyproject.toml` sử dụng `setuptools` hoặc `hatchling`
  - [x] Khai báo `dependencies` với phiên bản fix cứng như kiến trúc yêu cầu
  - [x] Cấu hình `project.scripts` để ánh xạ lệnh `olipd` tới `src/olipd/cli/main.py`
- [x] **Task 3: Thiết lập môi trường Python (AC: #3)**
  - [x] Thêm tệp `.env.example` với các biến môi trường mặc định
  - [x] Đảm bảo tệp `.gitignore` chặn các file rác của Python/Venv

## Dev Notes

- **Architecture Compliance:** Tuân thủ chặt chẽ `src/` layout để tách biệt code production và code test.
- **Tech Stack:** 
  - Python 3.10+
  - Pydantic v2 cho validation.
  - vLLM Engine không được import ở cấp root để tránh chiếm GPU sớm.
- **Testing:** Khởi tạo cấu trúc `pytest` nhưng chưa cần viết test logic sâu.

### Project Structure Notes

- Tuyệt đối tuân thủ sơ đồ:
  ```text
  src/olipd/
  ├── main.py
  ├── api/ (v1/, admin/, deps.py)
  ├── cli/ (main.py, optimize.py)
  ├── core/ (config.py, hardware.py, security.py)
  ├── services/ (inference.py, optimization.py, metrics.py)
  └── schemas/
  ```

### References

- [Architecture Design: Project Structure](file:///d:/AI%20In%20Action/OLIPD/docs/planning-artifacts/architecture.md#complete-project-directory-structure)
- [PRD: Technical Success](file:///d:/AI%20In%20Action/OLIPD/docs/planning-artifacts/prd.md#thanh-cong-ve-ky-thuat-technical-success)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
