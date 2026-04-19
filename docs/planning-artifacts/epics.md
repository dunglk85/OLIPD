---
stepsCompleted: [1, 2, 3, 4]
inputDocuments: ['docs/planning-artifacts/prd.md', 'docs/planning-artifacts/architecture.md', 'docs/project-context.md']
status: 'complete'
completedAt: '2026-04-19'
---

# OLIPD - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for OLIPD, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Nén mô hình safetensors bằng AWQ/GPTQ 4-bit.
FR2: Tự động benchmark Latency, Throughput và VRAM sau nén.
FR3: So sánh kết quả và đề xuất cấu hình tối ưu (Feedback Loop).
FR4: Người dùng có thể thiết lập ngưỡng sai số tối đa trước khi lưu bản nén.
FR5: Cung cấp Inference API tương thích OpenAI Chat/Completions.
FR6: Giải phóng tài nguyên GPU khi client mất kết nối (Early Disconnect).
FR7: Theo dõi VRAM thời gian thực và dọn dẹp cache chủ động.
FR8: Header X-Inference-Time-MS đo lường thời gian xử lý thực tế.
FR9: Tự động nhận diện GPU và điều chỉnh tính năng tương thích.
FR10: Ngăn chặn tuyệt đối việc nạp mô hình .pickle.
FR11: Cài đặt qua pip và triển khai qua Docker image.
FR12: Cung cấp bộ ví dụ chạy Local/Notebook hoàn chỉnh.

### NonFunctional Requirements

NFR1: TTFT < 100ms cho mô hình 7B trên hạ tầng GPU tối thiểu.
NFR2: Throughput tối thiểu 20 tokens/giây cho mỗi request đơn lẻ.
NFR3: Chiếm dụng VRAM ổn định, không vượt 90% dung lượng khả dụng.
NFR4: Server Inference đạt mức ổn định 99.5%.
NFR5: Pipeline nén tích hợp cơ chế 3-retry cho lỗi phần cứng tạm thời.
NFR6: Endpoint /admin yêu cầu xác thực riêng biệt và tách khỏi luồng traffic public.
NFR7: Thời gian xử lý lớp wrapper OpenAI API phải < 5ms.

### Additional Requirements

- **Starter Template:** Xây dựng từ đầu với Python `src/` layout dùng FastAPI, Typer và vLLM AsyncLLMEngine.
- **Storage Strategy:** Kết quả benchmark lưu dạng JSON/CSV tại `storage/benchmarks/`.
- **Security:** Header-based API Key (`X-API-Key`) và chặn hoàn toàn tệp .pickle.
- **Consistency:** Tuân thủ PEP8, async-first, và vượt qua kiểm tra ruff/mypy.
- **Resource Management:** Bắt buộc dùng `try...finally` cho GPU resource cleanup.
- **Observability:** Tách biệt log Inference và Optimization sử dụng Loguru.

### UX Design Requirements

(No UX document found for MVP phase)

### FR Coverage Map

- **FR1 (AWQ/GPTQ):** Epic 2
- **FR2 (Benchmark):** Epic 2
- **FR3 (Feedback Loop):** Epic 4
- **FR4 (Error Threshold):** Epic 2
- **FR5 (OpenAI API):** Epic 3
- **FR6 (Early Disconnect):** Epic 3
- **FR7 (VRAM Monitor/Clear):** Epic 4
- **FR8 (Inference-Time Header):** Epic 3
- **FR9 (GPU Auto-detect):** Epic 3
- **FR10 (No Pickle):** Epic 1
- **FR11 (Pip/Docker):** Epic 1
- **FR12 (Examples/DX):** Epic 1

## Epic List

### Epic 1: Project Foundation & Security Baseline
Thiết lập khung dự án chuyên nghiệp, đảm bảo các quy tắc bảo mật (Safetensors) và khả năng phân phối qua pip. Sau Epic này, Dev có thể cài đặt môi trường và khởi chạy khung server cơ bản.
**FRs covered:** FR10, FR11, FR12.

#### Story 1.1: Project Scaffold & Dependency Management
As a Developer,
I want to initialize a standard `src/` layout and `pyproject.toml`,
So that the project can be installed via `pip` and easily maintained.

**Acceptance Criteria:**
**Given** A fresh project directory
**When** Running `pip install -e .`
**Then** All directory structure (`src/olipd/`) matches the architectural design
**And** Core dependencies (`fastapi`, `vllm==0.4.0`, `typer`) are installed correctly.

#### Story 1.2: Implementation of Security Middleware (Safetensors Filter)
As a SRE/Security Engineer,
I want the system to automatically verify model formats,
So that I can block potential malicious code execution from `.pickle` files.

**Acceptance Criteria:**
**Given** A request to load a model
**When** The model file has a `.pickle` extension (e.g., `pytorch_model.bin`)
**Then** The system returns "Security Violation: Only .safetensors allowed" and stops the process
**And** Only files ending in `.safetensors` are permitted to load.

#### Story 1.3: Core API Key Authentication Middleware
As an Admin,
I want to apply header-based authentication,
So that I can protect the API from unauthorized access.

**Acceptance Criteria:**
**Given** The server is running
**When** Sending a request without `X-API-Key` or with an incorrect key
**Then** The system returns a 401 Unauthorized status code.

#### Story 1.4: Base Dockerization for GPU Environment
As a DevOps,
I want to have a multi-stage Dockerfile,
So that I can package a lightweight application compatible with GPU infrastructure.

**Acceptance Criteria:**
**Given** Current source code
**When** Running `docker build`
**Then** A production-ready image is created supporting `nvidia-container-toolkit` and CUDA runtime.

### Epic 2: Precision Optimization Pipeline
Xây dựng luồng nén mô hình (AWQ/GPTQ) tích hợp bộ công cụ Benchmark. Sau Epic này, ML Engineer có thể nén mô hình và nhận được báo cáo Latency/VRAM thực tế.
**FRs covered:** FR1, FR2, FR4.

#### Story 2.1: CLI for Automated Model Quantization (AWQ/GPTQ)
As a ML Engineer,
I want to quantize models via a simple CLI command,
So that I can save time and ensure reproducibility.

**Acceptance Criteria:**
**Given** An original model in `.safetensors` format
**When** Running `olipd optimize --model <path> --method awq`
**Then** A 4-bit quantized version is created and stored successfully.

#### Story 2.2: Automated Performance Benchmarking Engine
As a ML Engineer,
I want the system to automatically measure performance after quantization,
So that I know the exact trade-off between size and speed.

**Acceptance Criteria:**
**Given** A quantized model
**When** The optimization process completes
**Then** The system outputs a report including: TTFT, Throughput (TPS), and VRAM usage.

#### Story 2.3: Accuracy Guardrail & Safety Threshold
As a ML Engineer,
I want the system to block saving the quantized model if the error exceeds a threshold,
So that I can ensure the quality of model responses.

**Acceptance Criteria:**
**Given** A configuration with `max_error_threshold: 3%`
**When** The measured error after quantization is 5%
**Then** The system notifies an error, deletes the failed quantization file, and requests a retry with different parameters.

#### Story 2.4: Structured Benchmark Results Storage
As a ML Engineer,
I want the measurement results to be stored in a standard format (JSON/CSV),
So that I can compare between different quantization versions.

**Acceptance Criteria:**
**Given** The benchmarking process completes
**Then** A file is created in `storage/benchmarks/` containing full metadata (GPU card, method, results).

### Epic 3: High-Performance Inference Serving
Triển khai API phục vụ mô hình chuẩn OpenAI với cơ chế bảo vệ tài nguyên GPU (Early Disconnect). Sau Epic này, hệ thống có thể phục vụ hàng ngàn yêu cầu inference với độ trễ thấp và độ tin cậy cao.
**FRs covered:** FR5, FR6, FR8, FR9.

#### Story 3.1: OpenAI-Compatible Chat Completions API
As an Application Developer,
I want to use quantized models via standard OpenAI API,
So that I can integrate into existing apps without changing libraries.

**Acceptance Criteria:**
**Given** OLIPD server is running with Llama-3 4-bit
**When** Sending a valid OpenAI POST request to `/v1/chat/completions`
**Then** System returns a complete and valid response from the quantized model.

#### Story 3.2: SSE Streaming for Real-time Generation
As a Chatbot User,
I want to receive real-time token-by-token feedback via streaming,
So that I feel a faster sense of response.

**Acceptance Criteria:**
**Given** A request with `stream: true`
**Then** System uses Server-Sent Events (SSE) to push each token to the client as generated.

#### Story 3.3: GPU Resource Cleanup on Early Disconnect
As a DevOps/SRE,
I want the system to automatically release GPU resources when a client disconnects unexpectedly,
So that I can prevent wasting GPU for orphaned requests.

**Acceptance Criteria:**
**Given** An active inference process
**When** A client disconnects or stops the request prematurely
**Then** System detects the disconnect and immediately halts the inference process for that specific request
**And** Clear the associated GPU cache/vRAM for that request.

#### Story 3.4: Hardware-Aware Engine Auto-Configuration
As a ML Engineer,
I want the system to automatically detect GPU architecture upon startup,
So that I can apply optimal vLLM configurations.

**Acceptance Criteria:**
**Given** System starts on an NVIDIA T4 card
**Then** Logs show "Turing Architecture detected - Applying Safe Defaults"
**And** Parameters like `enforce_eager` are adjusted according to hardware capabilities.

#### Story 3.5: Performance Metadata Header (X-Inference-Time-MS)
As a Developer,
I want to know exactly how long the server took to process the request,
So that I can monitor application performance.

**Acceptance Criteria:**
**Then** All successful responses must include an `X-Inference-Time-MS` header containing the actual server processing time.

### Epic 4: Strategic Admin & Feedback Loop
Cung cấp giao diện quản trị Admin để dọn dẹp bộ nhớ và cơ chế tự động hóa Feedback Loop (tự chọn cấu hình nén tốt nhất). Đây là khâu hoàn thiện vòng lặp tối ưu hóa.
**FRs covered:** FR3, FR7.

#### Story 4.1: Real-time VRAM Monitoring API
As a DevOps/SRE,
I want to view real-time VRAM usage metrics via API,
So that I can monitor system health without manual terminal commands.

**Acceptance Criteria:**
**Given** A GET request to `/admin/metrics` with valid API Key
**Then** System returns a JSON object containing: VRAM Used, VRAM Free, and Fragmentation percentage.

#### Story 4.2: Admin Control for Active Cache Clearing
As a DevOps,
I want to have a command to proactively clear the cache,
So that I can reclaim fragmented memory without server restarts.

**Acceptance Criteria:**
**When** Sending a POST request to `/admin/cache/clear`
**Then** System executes vLLM's KV cache clearing command
**And** Returns the amount of memory successfully released.

#### Story 4.3: Automated Feedback Loop (Best Config Selection)
As a ML Engineer,
I want the system to automatically recommend the best configuration based on saved benchmark data,
So that I don't have to guess the output quality and speed.

**Acceptance Criteria:**
**Given** Benchmark data for AWQ and GPTQ exists for a specific model
**When** Running the command `olipd recommend --model <id>`
**Then** System analyzes historical data and suggests the optimal method (e.g., "GPTQ is recommended for T4").

#### Story 4.4: Local Execution & DX Pack (Notebook Examples)
As a New User,
I want to have Jupyter Notebook examples ready to run on Local/Colab,
So that I can get started with OLIPD in less than 15 minutes.

**Acceptance Criteria:**
**Then** A directory `examples/` is provided containing `.ipynb` files guiding from optimization to API serving.
