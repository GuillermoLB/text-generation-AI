from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv(override=True)


class Settings(BaseSettings):
    MODEL_NAME: str = "Roams_generator"
    DB_NAME: str = "database"
    LLM_ID: str = "gpt2"
    HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def get_connection_str(self) -> str:
        return f"sqlite:///./{self.DB_NAME}.db"
