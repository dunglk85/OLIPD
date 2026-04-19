from pathlib import Path
from typing import List, Set, Union

class SecurityError(Exception):
    """Ngoại lệ được ném ra khi phát hiện tệp tin không an toàn trong thư mục mô hình."""
    pass

# Danh sách các đuôi file bị cấm tuyệt đối vì rủi ro thực thi mã độc (Arbitrary Code Execution)
FORBIDDEN_EXTENSIONS: Set[str] = {".bin", ".pth", ".pkl", ".pickle", ".pt"}

# Danh sách các đuôi file metadata được phép tải
ALLOWED_METADATA_EXT: Set[str] = {".json", ".txt", ".model", ".tiktoken", ".yaml", ".yml"}

def is_safe_file(file_path: Path) -> bool:
    """
    Kiểm tra một tệp tin đơn lẻ có an toàn để nạp hay không.
    
    Args:
        file_path: Đối tượng Path của tệp tin cần kiểm tra.
        
    Returns:
        True nếu tệp an toàn (safetensors hoặc whitelist metadata), False nếu không.
    """
    suffix = file_path.suffix.lower()
    
    # 1. Định dạng ưu tiên hàng đầu và tuyệt đối an toàn
    if suffix == ".safetensors":
        return True
    
    # 2. Chặn các đuôi file nguy hiểm đã biết
    if suffix in FORBIDDEN_EXTENSIONS:
        return False
        
    # 3. Cho phép các tệp metadata nằm trong danh sách trắng
    if suffix in ALLOWED_METADATA_EXT:
        return True
        
    # 4. Mặc định là không an toàn cho các loại file lạ trong MVP
    return False

def validate_model_dir(model_path: Union[str, Path]) -> List[Path]:
    """
    Quét thư mục mô hình và kiểm tra tính an toàn của tất cả các tệp tin bên trong.
    
    Args:
        model_path: Đường dẫn tới thư mục chứa mô hình.
        
    Returns:
        Danh sách các đối tượng Path của các tệp tin an toàn được tìm thấy.
        
    Raises:
        FileNotFoundError: Nếu thư mục không tồn tại.
        SecurityError: Nếu phát hiện bất kỳ tệp tin nào thuộc danh sách cấm.
    """
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Thư mục mô hình không tồn tại: {model_path}")
        
    safe_files: List[Path] = []
    
    for file in path.iterdir():
        # Bỏ qua các thư mục con trong lần quét này
        if file.is_dir():
            continue
            
        suffix = file.suffix.lower()
        
        # Kiểm tra tính an toàn
        if not is_safe_file(file):
            if suffix in FORBIDDEN_EXTENSIONS:
                raise SecurityError(
                    f"Security Violation: Phát hiện tệp tin nguy hiểm '{file.name}'. "
                    "OLIPD chỉ hỗ trợ nạp định dạng .safetensors để đảm bảo an toàn cho hạ tầng GPU. "
                    "Vui lòng chuyển đổi mô hình trước khi sử dụng."
                )
            # Đối với các file lạ khác (không thuộc blacklist nhưng cũng không thuộc whitelist), 
            # chúng ta chỉ đơn giản là không liệt kê vào safe_files thay vì ném lỗi chặn đứng.
        else:
            safe_files.append(file)
            
    return safe_files
