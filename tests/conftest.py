from pathlib import Path

import pytest

# Import các class từ package assistant_core
from assistant_core.config import Settings
from assistant_core.knowledge import Handbook, OfficeDirectory


@pytest.fixture
def settings():
    """Tạo cấu hình mặc định dùng cho môi trường test."""
    return Settings(
        data_dir=Path("data"), llm_provider="stub", credit_rate_vnd=450000, retake_multiplier=1.5, max_credits=30
    )


@pytest.fixture
def offices():
    """Đọc và trả về danh sách văn phòng từ file CSV."""
    # Đường dẫn tính từ thư mục gốc của project (nơi chạy lệnh pytest)
    return OfficeDirectory.from_csv(Path("data/offices.csv"))


@pytest.fixture
def handbook():
    """Đọc và trả về sổ tay quy định từ file JSON."""
    # Thiết kế theo Step 5: Handbook có hàm from_json tương tự OfficeDirectory
    return Handbook.from_json(Path("data/handbook.json"))
