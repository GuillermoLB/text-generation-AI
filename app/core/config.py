from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DB_NAME: str = "database"

    # Model settings
    MODEL_NAME: str = "Roams_generator"
    LLM_ID: str = "gpt2"

    # Security
    HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # Logging
    APP_LOG_DIR: str = "/app/var/log"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_connection_str(self) -> str:
        return f"sqlite:///./{self.DB_NAME}.db"
