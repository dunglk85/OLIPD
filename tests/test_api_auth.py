import pytest
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from olipd.api.deps import get_api_key
from olipd.core.config import settings

# Khởi tạo một ứng dụng FastAPI ảo để test middleware
app = FastAPI()

# Override exception handler để trả về chuẩn OpenAI (không có wrap 'detail')
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.get("/protected")
async def protected_route(api_key: str = Depends(get_api_key)):
    """Endpoint yêu cầu xác thực."""
    return {"status": "success", "message": "Bạn đã vượt qua lớp bảo mật"}

client = TestClient(app)

def test_auth_success():
    """Kiểm tra truy cập khi cung cấp đúng API Key."""
    valid_key = settings.API_KEY.get_secret_value()
    response = client.get("/protected", headers={"X-API-Key": valid_key})
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_auth_missing_key():
    """Kiểm tra lỗi 401 khi không gửi Header X-API-Key."""
    response = client.get("/protected")
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "missing_api_key"
    assert "Thiếu API Key" in data["error"]["message"]

def test_auth_invalid_key():
    """Kiểm tra lỗi 401 khi gửi sai API Key."""
    response = client.get("/protected", headers={"X-API-Key": "wrong-secret-key-123"})
    
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "invalid_api_key"
    assert "không hợp lệ" in data["error"]["message"]

def test_auth_error_format_consistency():
    """Đảm bảo định dạng lỗi tuân thủ cấu trúc OpenAI."""
    response = client.get("/protected")
    data = response.json()
    
    # Cấu trúc bắt buộc của OpenAI Error Object
    assert "error" in data
    assert all(k in data["error"] for k in ["message", "type", "param", "code"])
    assert data["error"]["type"] == "invalid_request_error"
