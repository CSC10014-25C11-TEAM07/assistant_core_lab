import os
from pathlib import Path
from pydantic import BaseModel
from .errors import ConfigError


class Settings(BaseModel):
    data_dir: Path = Path("data")
    llm_provider: str = "stub"
    llm_api_key: str | None = None
    credit_rate_vnd: int = 450000
    retake_multiplier: float = 1.5
    max_credits: int = 30


def load_dotenv(path: str | Path, override: bool = False) -> None:
    env_file = Path(path)
    if not env_file.exists():
        return

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if override or key not in os.environ:
            os.environ[key] = value


def load_settings(env_file: str | Path | None = ".env") -> Settings:
    if env_file:
        load_dotenv(env_file, override=False)

    s = Settings(
        data_dir=Path(os.getenv("ASSISTANT_DATA_DIR", "data")),
        llm_provider=os.getenv("LLM_PROVIDER", "stub"),
        llm_api_key=os.getenv("LLM_API_KEY") or None,
        credit_rate_vnd=int(os.getenv("CREDIT_RATE_VND", "450000")),
        retake_multiplier=float(os.getenv("RETAKE_MULTIPLIER", "1.5")),
        max_credits=int(os.getenv("MAX_CREDITS", "30")),
    )

    if s.llm_provider != "stub" and not s.llm_api_key:
        raise ConfigError(f"LLM_API_KEY is required when LLM_PROVIDER={s.llm_provider!r}")

    return s