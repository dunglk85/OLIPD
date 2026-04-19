---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-02b-vision', 'step-02c-executive-summary', 'step-03-success', 'step-04-journeys', 'step-05-domain', 'step-06-innovation', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish']
classification:
  projectType: 'developer_tool'
  domain: 'scientific'
  complexity: 'medium'
  projectContext: 'greenfield'
inputDocuments: ['docs/brief-distillate.md', 'docs/project-context.md']
workflowType: 'prd'
---

# Product Requirements Document - OLIPD

**Author:** Admin
**Date:** 2026-04-19

## Executive Summary

### Tầm nhìn và Mục tiêu
OLIPD (LLM Inference Optimization Toolkit) cung cấp hạ tầng AI hiệu năng cao chuẩn production cho các đội ngũ phát triển và startup tại Việt Nam. Sản phẩm tự động hóa toàn bộ quy trình từ nén mô hình đến phục vụ API, giúp ML Engineer triển khai LLM tối ưu chỉ trong một lần chạy mà không cần kiến thức chuyên sâu về phần cứng tầng thấp.

### Điểm khác biệt cốt lõi
Sức mạnh của OLIPD nằm ở kiến trúc **Closed-loop (Vòng lặp khép kín)** tích hợp: Quantization, Serving và Benchmark. Hệ thống tự động nhận diện phần cứng (NVIDIA T4 vs A10/A100), thực hiện benchmark và chọn lựa cấu hình nén (AWQ/GPTQ) tối ưu nhất. Thay vì phỏng đoán, người dùng nhận được dữ liệu thực tế về Latency, Throughput và **Cost per 1k requests** ngay lập tức.

## Success Criteria

### Thành công đối với người dùng (User Success)
*   **Aha! Moment:** Triển khai mô hình lần đầu thành công trong **< 15 phút**.
*   **Hiệu năng:** Đạt **x2 - x3 lần Throughput** so với cấu hình mặc định trên cùng tài nguyên GPU.
*   **Chất lượng:** Sai số sau khi nén (Quantization 4-bit) không vượt quá **5%**.

### Thành công về Kỹ thuật (Technical Success)
*   **Tính thích ứng:** Tự động điều chỉnh cấu hình theo kiến trúc GPU phát hiện được.
*   **Độ ổn định:** Không rò rỉ bộ nhớ (Memory Leak) trong các tác vụ streaming dài hạn.
*   **Tính đo lường:** Cung cấp chỉ số Latency, Throughput và Cost chính xác qua hệ thống tích hợp.

### Kết quả đo lường (Measurable Outcomes)
*   **Tỉ lệ áp dụng:** Có ít nhất 10 đội ngũ AI tại Việt Nam sử dụng trong 6 tháng đầu.
*   **Tiết kiệm:** Giảm trung bình **30 - 40% chi phí vận hành GPU**.

## Product Scope

### Phase 1: MVP (Minimum Viable Product)
*   Pipeline nén mô hình cơ bản (AWQ và GPTQ).
*   Inference Server chuẩn OpenAI API (FastAPI + vLLM core).
*   Công cụ Benchmark CLI đo lường hiệu năng.
*   Cơ chế giải phóng GPU khi ngắt kết nối (**Early Disconnect**).
*   Admin API quản lý VRAM và dọn dẹp cache.

### Phase 2: Growth Features
*   **Feedback Loop:** Tự động tối ưu cấu hình dựa trên dữ liệu benchmark thực tế.
*   Mở rộng hỗ trợ các dòng model thế hệ mới (Phi-3, Qwen).
*   Templates triển khai chuẩn MLOps (Kubernetes, Prometheus).

### Phase 3: Vision (Expansion)
*   Hỗ trợ **Multi-GPU** (Tensor Parallelism).
*   **Dashboard UI** theo dõi lịch sử và chi phí vận hành thời gian thực.
*   Hệ thống Quản trị phân quyền (RBAC) cho Enterprise.

## User Journeys

### Hành trình 1: Nam (Kỹ sư ML) – Triển khai trên hạ tầng tối ưu
Nam cần triển khai Llama-3 70B lên card **NVIDIA T4** để tiết kiệm chi phí. Nam nạp model vào OLIPD pipeline. Hệ thống tự động benchmark AWQ và GPTQ trên card T4 và báo cáo: *"GPTQ cho thông lượng cao hơn 15% trên phần cứng này"*. Nam xác nhận và deploy thành công, tiết kiệm hàng ngàn USD chi phí thuê GPU cao cấp.

### Hành trình 2: Dương (DevOps/SRE) – Quản trị tài nguyên chủ động
Hệ thống báo động Latency tăng cao do phân mảnh VRAM vào ban đêm. Dương truy cập Admin API, kiểm tra metric `X-Inference-Time-MS` thay vì restart server. Dương thực hiện lệnh `/admin/cache/clear` để thu hồi bộ nhớ mà không gây downtime. Hệ thống tự hồi phục ngay lập tức.

### Hành trình 3: Minh (Frontend Dev) – Tích hợp Chatbot Streaming
Minh tích hợp stream response cho ứng dụng mobile. Minh thử nghiệm kịch bản người dùng ngắt mạng đột ngột. Hệ thống OLIPD tự nhận diện tín hiệu ngắt kết nối và giải phóng GPU vRAM ngay sau 500ms, giúp server không bị treo bởi các tiến trình inference "rác".

## Domain-Specific Requirements (Scientific/AI)

### Tuân thủ & An toàn
*   **Safe Weights Only:** Bắt buộc định dạng `.safetensors`. Chặn tuyệt đối `.pickle` để ngăn thực thi mã độc.
*   **Reproducibility:** Ghi nhật ký chi tiết Driver GPU, CUDA version và cấu hình phần cứng kèm theo báo cáo benchmark.

### Ràng buộc kỹ thuật
*   **Accuracy Baseline:** Tự động kiểm tra sai số sau nén; chặn cấu hình nếu sai số vượt **3%**.
*   **Hardware Fallback:** Tự động điều chỉnh hoặc tắt các tính năng vLLM không tương thích trên kiến trúc Turing (T4).
*   **VRAM Safeguard:** Tự động kích hoạt dọn dẹp cache khi độ phân mảnh VRAM vượt **15%**.

## Innovation & Novel Patterns

### Các khu vực đột phá
*   **Automated Feedback Loop:** Benchmark trực tiếp điều chỉnh tham số nén mà không cần con người can thiệp.
*   **Hardware-Aware Auto-Tuning:** Tự động chọn thuật toán nén (AWQ/GPTQ) và siêu tham số dựa trên GPU đích.
*   **Zero-Guesswork Deployment:** Công khai chỉ số **Cost per Request** giúp quyết định triển khai dựa trên bài toán kinh tế.

### Phương pháp kiểm chứng
*   **Leaderboard of Configs:** Hiển thị kết quả tất cả cấu hình đã thử nghiệm để chứng minh tính tối ưu.
*   **Performance Signatures:** Gán nhãn hiệu năng cho từng bộ mô hình + phần cứng cụ thể.

## Developer Tool & API Specific Requirements

### Đặc tả API
*   **Standard Interface:** Tuân thủ 1:1 chuẩn OpenAI API (`/v1/chat/completions`, v.v.).
*   **Streaming:** Hỗ trợ SSE (Server-Sent Events) ổn định.
*   **Control Interface:** Cung cấp `/admin/pipeline/optimize`, `/admin/metrics` và `/admin/cache/clear`.

### Phân phối
*   **Library (pip):** Gói `olipd` cho sử dụng thư viện và chạy local.
*   **Server (Docker):** Container tích hợp sẵn môi trường CUDA/vLLM tối ưu.

### Bảo mật & Trải nghiệm
*   **Auth:** API Key đơn giản qua Header `X-API-Key`.
*   **DX:** Tập trung vào tài liệu hướng dẫn chạy trực tiếp trên Local/Colab.

## Functional Requirements

### Optimization & Serving
*   **FR1:** Nén mô hình `safetensors` bằng AWQ/GPTQ 4-bit.
*   **FR2:** Tự động benchmark Latency, Throughput và VRAM sau nén.
*   **FR3:** So sánh kết quả và đề xuất cấu hình tối ưu (**Feedback Loop**).
*   **FR4:** Người dùng có thể thiết lập ngưỡng sai số tối đa trước khi lưu bản nén.
*   **FR5:** Cung cấp Inference API tương thích OpenAI Chat/Completions.
*   **FR6:** Giải phóng tài nguyên GPU khi client mất kết nối (**Early Disconnect**).

### Admin & Infrastructure
*   **FR7:** Theo dõi VRAM thời gian thực và dọn dẹp cache chủ động.
*   **FR8:** Header `X-Inference-Time-MS` đo lường thời gian xử lý thực tế.
*   **FR9:** Tự động nhận diện GPU và điều chỉnh tính năng tương thích.
*   **FR10:** Ngăn chặn tuyệt đối việc nạp mô hình `.pickle`.

### Distribution
*   **FR11:** Cài đặt qua `pip` và triển khai qua `Docker image`.
*   **FR12:** Cung cấp bộ ví dụ chạy Local/Notebook hoàn chỉnh.

## Non-Functional Requirements

### Performance & Reliability
*   **Latency:** TTFT **< 100ms** cho mô hình 7B trên hạ tầng GPU tối thiểu.
*   **Throughput:** Tối thiểu **20 tokens/giây** cho mỗi request đơn lẻ.
*   **Memory:** Chiếm dụng VRAM ổn định, không vượt **90%** dung lượng khả dụng.
*   **Uptime:** Server Inference đạt mức ổn định **99.5%**.
*   **Resilience:** Pipeline nén tích hợp cơ chế **3-retry** cho lỗi phần cứng tạm thời.

### Security & Integration
*   **Isolation:** Endpoint `/admin` yêu cầu xác thực riêng biệt và tách khỏi luồng traffic public.
*   **Overhead:** Thời gian xử lý lớp wrapper OpenAI API phải **< 5ms**.
