from functools import lru_cache
from os import getenv


class Settings:
    app_name: str = "AI Consulting Case Simulator API"
    openai_api_key: str | None = getenv("OPENAI_API_KEY")
    openai_model: str = getenv("OPENAI_MODEL", "gpt-4o-mini")
    request_timeout_seconds: float = float(getenv("OPENAI_TIMEOUT_SECONDS", "20"))
    min_response_length: int = int(getenv("MIN_RESPONSE_LENGTH", "80"))
    max_response_length: int = int(getenv("MAX_RESPONSE_LENGTH", "4000"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
