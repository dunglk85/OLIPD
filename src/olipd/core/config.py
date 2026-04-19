from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Quản lý cấu hình toàn cục của dự án OLIPD.
    Tự động nạp dữ liệu từ biến môi trường hoặc tệp .env với tiền tố OLIPD_.
    """
    # Thông tin dự án
    PROJECT_NAME: str = "OLIPD"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Bảo mật
    # api_key sẽ được đọc từ OLIPD_API_KEY. 
    # Nếu không có, sẽ sử dụng giá trị mặc định cho môi trường phát triển (Dev).
    API_KEY: SecretStr = SecretStr("olipd-dev-secret-key-12345678901234567890")
    
    # Cấu hình nạp biến môi trường
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="OLIPD_",
        case_sensitive=True # Phân biệt hoa thường trong .env (ví dụ: API_KEY != api_key)
    )

# Singleton instance để sử dụng trong toàn bộ ứng dụng
settings = Settings()
