from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from olipd.core.config import settings

# Định nghĩa Header name mà chúng ta kỳ vọng
API_KEY_NAME = "X-API-Key"

# Khởi tạo Security Scheme cho FastAPI
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Dependency Injection để xác thực API Key gán trong Header X-API-Key.
    
    Args:
        api_key: Giá trị lấy từ Header X-API-Key.
        
    Returns:
        api_key nếu hợp lệ.
        
    Raises:
        HTTPException: Lỗi 401 nếu thiếu hoặc sai Key.
    """
    # 1. Kiểm tra sự tồn tại của Key
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": "Thiếu API Key. Vui lòng cung cấp Header X-API-Key.",
                    "type": "invalid_request_error",
                    "param": None,
                    "code": "missing_api_key"
                }
            }
        )
        
    # 2. Kiểm tra tính chính xác của Key (so sánh với cấu hình)
    if api_key != settings.API_KEY.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "message": "API Key không hợp lệ.",
                    "type": "invalid_request_error",
                    "param": None,
                    "code": "invalid_api_key"
                }
            }
        )
        
    return api_key
