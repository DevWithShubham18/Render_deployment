from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    ENV: str
    GROQ_API_KEY: SecretStr
    VOYAGE_API_KEY: str
    PINECONE_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore",
    )


settings = Settings()  # type: ignore
