# Story 1.4: Base Dockerization for GPU Environment

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a DevOps,
I want to have a multi-stage Dockerfile,
so that I can package a lightweight application compatible with GPU infrastructure.

## Acceptance Criteria

1. **[AC1]** Tệp `Dockerfile` sử dụng base image chính thức từ NVIDIA (ưu tiên CUDA 12.1.1 + Ubuntu 22.04).
2. **[AC2]** Triển khai cơ chế Multi-stage Build:
   - **Stage 1 (Builder):** Cài đặt đầy đủ compiler và dependencies nặng (`vllm`, `transformers`).
   - **Stage 2 (Runtime):** Chỉ copy các thư viện đã build và mã nguồn ứng dụng, giúp giảm đáng kể kích thước Image.
3. **[AC3]** Image phải cài đặt gói `olipd` ở chế độ production (`pip install .`) để lệnh CLI `olipd` khả dụng mọi lúc.
4. **[AC4]** Container phải được thiết lập để chạy dưới quyền người dùng không phải root (non-root) vì lý do bảo mật.
5. **[AC5]** Thiết lập các biến môi trường mặc định tối ưu: `PYTHONUNBUFFERED=1`, `PYTHONDONTWRITEBYTECODE=1`.

## Tasks / Subtasks

- [x] **Task 1: Xây dựng Stage 1 - Builder (AC: #1, #2)**
  - [x] Chọn image base: `nvidia/cuda:12.1.1-devel-ubuntu22.04`
  - [x] Cài đặt Python 3.10 và các công cụ build hệ thống
  - [x] Cài đặt dependencies từ `pyproject.toml`
- [x] **Task 2: Xây dựng Stage 2 - Runtime & App (AC: #2, #3, #5)**
  - [x] Chọn image base: `nvidia/cuda:12.1.1-runtime-ubuntu22.04`
  - [x] Copy Site-packages từ Builder stage
  - [x] Copy mã nguồn dự án vào `/app/src`
  - [x] Thực hiện `pip install --no-deps .` để đăng ký CLI
- [x] **Task 3: Cấu hình Container Execution (AC: #4)**
  - [x] Tạo group và user `olipd_user`
  - [x] Phân quyền thư mục `/app` và `storage/` cho user này
  - [x] Thiết lập `USER olipd_user` và `ENTRYPOINT` khởi chạy CLI hoặc API
- [x] **Task 4: Kiểm thử Docker Build & Run (Manual)**
  - [x] Chạy lệnh `docker build -t olipd:latest .`
  - [x] Kiểm tra lệnh `olipd version` bên trong container: `docker run --rm olipd:latest version`

## Dev Notes

- **vLLM & CUDA:** vLLM yêu cầu phiên bản CUDA rất cụ thể. CUDA 12.1 hiện là lựa chọn ổn định nhất cho `vllm>=0.4.0`.
- **GPU Access:** Lưu ý khi chạy container thực tế cần flag `--gpus all`.
- **Caching:** Đặt các lệnh cài đặt dependencies trước khi copy mã nguồn để tận dụng tối đa Docker cache layer.

### Project Structure Notes

- Tệp `Dockerfile` nằm ở gốc dự án.
- Tệp `.dockerignore` cần được tạo để loại bỏ `__pycache__`, `.git`, và `storage/benchmarks/`.

### References

- [Architecture Infrastructure Decisions](file:///d:/AI%20In%20Action/OLIPD/docs/planning-artifacts/architecture.md#infrastructure--deployment)
- [NVIDIA Docker Hub](https://hub.docker.com/r/nvidia/cuda)

## Dev Agent Record

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List
