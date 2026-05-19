from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    AITUNNEL_API_KEY: str
    AITUNNEL_BASE_URL: str

    DB_USER: str = "edtech_user"
    DB_PASSWORD: str = "secret_pass"
    DB_NAME: str = "edtech_bot_db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()