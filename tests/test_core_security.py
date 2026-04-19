import pytest
import os
from pathlib import Path
from olipd.core.security import validate_model_dir, SecurityError

def test_validate_model_dir_all_safe(tmp_path):
    """Kiểm tra thư mục chứa toàn tệp tin an toàn."""
    # Tạo các file an toàn giả lập
    (tmp_path / "model.safetensors").write_text("safe weights", encoding="utf-8")
    (tmp_path / "config.json").write_text("{}", encoding="utf-8")
    (tmp_path / "tokenizer.model").write_text("vocab data", encoding="utf-8")
    
    safe_files = validate_model_dir(tmp_path)
    
    # Kiểm tra số lượng và tên file
    assert len(safe_files) == 3
    filenames = {f.name for f in safe_files}
    assert "model.safetensors" in filenames
    assert "config.json" in filenames
    assert "tokenizer.model" in filenames

def test_validate_model_dir_detects_pickle(tmp_path):
    """Kiểm tra việc phát hiện tệp tin .bin nguy hiểm."""
    (tmp_path / "model.safetensors").write_text("safe")
    (tmp_path / "pytorch_model.bin").write_text("dangerous pickle data")
    
    # Phải ném lỗi SecurityError
    with pytest.raises(SecurityError) as excinfo:
        validate_model_dir(tmp_path)
    
    assert "Security Violation" in str(excinfo.value)
    assert "pytorch_model.bin" in str(excinfo.value)

def test_validate_model_dir_detects_pth(tmp_path):
    """Kiểm tra việc phát hiện tệp tin .pth nguy hiểm."""
    (tmp_path / "checkpoint.pth").write_text("dangerous")
    
    with pytest.raises(SecurityError):
        validate_model_dir(tmp_path)

def test_validate_model_dir_ignore_unrecognized_files(tmp_path):
    """Kiểm tra việc bỏ qua các file không nằm trong diện nguy hiểm nhưng cũng không phải metadata."""
    (tmp_path / "model.safetensors").write_text("safe")
    (tmp_path / "random_script.py").write_text("print('hello')") # Không nằm trong whitelist metadata
    
    safe_files = validate_model_dir(tmp_path)
    
    # Chỉ file safetensors được giữ lại
    assert len(safe_files) == 1
    assert safe_files[0].name == "model.safetensors"

def test_validate_model_dir_not_exists():
    """Kiểm tra lỗi khi thư mục không tồn tại."""
    with pytest.raises(FileNotFoundError):
        validate_model_dir("/path/to/non/existent/dir/that/does/not/exist/at/all")
