from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Database
    DB_NAME: str = "database"

    # Model settings
    MODEL_NAME: str = "Roams_generator"
    LLM_ID: str = "gpt2"

    # Security
    HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    SECRET_KEY: str = "7b4e76599972241d849cb98bf5ea1763cca2482197c1ac1715b4acfde93043a4"
    ALGORITHM: str = "HS256"

    # Logging
    LOG_LEVEL: str = "INFO"
    DISABLE_LOGGERS: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_connection_str(self) -> str:
        return f"sqlite:///./{self.DB_NAME}.db"
