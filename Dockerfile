# Stage 1: Builder - Cài đặt và biên dịch các dependencies
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04 AS builder

# Thiết lập các biến môi trường cho quá trình build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /build

# Cài đặt Python 3.10 và các gói hệ thống cần thiết cho việc biên dịch
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3-dev \
    git \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Cài đặt các thư viện cơ bản trước để tận dụng Docker Layer Cache
# Lưu ý: Cài đặt wheel và setuptools trước để tránh lỗi khi cài các gói nặng
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

# Copy tệp cấu hình dependency
COPY pyproject.toml .
COPY src/ src/

# Cài đặt ứng dụng và toàn bộ dependencies
# vLLM sẽ được tải xuống dưới dạng wheel hoặc biên dịch tại đây
RUN pip3 install --no-cache-dir .

# Stage 2: Final Runtime - Image gọn nhẹ để chạy thực tế
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

LABEL maintainer="Admin"
LABEL project="OLIPD"

# Thiết lập môi trường thực thi
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

WORKDIR /app

# Cài đặt Python runtime (vừa đủ để chạy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Sao chép các gói Python đã cài đặt từ Builder stage
COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Sao chép mã nguồn và tệp cấu hình cần thiết
COPY . .

# Tạo người dùng không có quyền root để tăng cường bảo mật container
RUN groupadd -g 1000 olipd && \
    useradd -u 1000 -g olipd -s /bin/sh olipd && \
    chown -R olipd:olipd /app

# Đảm bảo thư mục lưu trữ benchmark có quyền ghi cho user
RUN mkdir -p storage/benchmarks && chown -R olipd:olipd storage/

USER olipd

# Khai báo Port API (mặc định cho FastAPI)
EXPOSE 8000

# Thiết lập điểm khởi chạy mặc định là lệnh CLI của dự án
ENTRYPOINT ["olipd"]

# Nếu không có tham số truyền vào khi chạy docker run, nó sẽ hiển thị version
CMD ["version"]
