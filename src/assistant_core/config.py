from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    data_dir: Path = Path("data")
    llm_provider: str = "stub"
    credit_rate_vnd: int = 450000
    retake_multiplier: float = 1.5
    max_credits: int = 30
