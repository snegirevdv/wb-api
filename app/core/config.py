from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки проекта."""

    app_title: str = "WB-API"
    app_description: str = "API для получения информации о товарах WB"
    schedule_interval_minutes = 30
    wb_url = (
        "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm="
    )

    api_token: str = "defaulttoken"
    bot_token: str = "defaulttoken"
    jobs_db_url: str = "sqlite:///sqlite3.db"

    postgres_user: str | None = None
    postgres_password: str | None = None
    postgres_host: str = "db"
    postgres_port: str = "5432"
    postgres_db: str = "db"

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def database_url(self) -> str:
        """URL для подключения к БД."""
        if self.postgres_user and self.postgres_password:
            return (
                f"postgresql+asyncpg://{self.postgres_user}:"
                f"{self.postgres_password}@{self.postgres_host}:"
                f"{self.postgres_port}/{self.postgres_db}"
            )

        return "sqlite+aiosqlite:///sqlite3.db"


settings = Settings()
