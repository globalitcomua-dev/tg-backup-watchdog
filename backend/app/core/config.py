from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://backup_watchdog:backup_watchdog@localhost:5432/backup_watchdog"
    )

    api_token: str = ""

    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    telegram_poll_interval: int = 5
    watchdog_check_interval: int = 300
    notify_on_initial_state: bool = False

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
