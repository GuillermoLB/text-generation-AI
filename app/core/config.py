from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv(override=True)


class Settings(BaseSettings):
    DB_NAME: str = "database"
    MODEL_NAME: str = "Roams_generator"
    LLM_ID: str = "gpt2"
    HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    # run `openssl rand -hex 32` to generate a new secret key
    SECRET_KEY: str = "7b4e76599972241d849cb98bf5ea1763cca2482197c1ac1715b4acfde93043a4"
    ALGORITHM: str = "HS256"

    def get_connection_str(self) -> str:
        return f"sqlite:///./{self.DB_NAME}.db"
