from typing import Optional
from pydantic import BaseModel, field_validator


class ModelBase(BaseModel):
    name: str
    llm: str
    max_length: int
    temperature: float
    top_p: float


class ModelCreate(ModelBase):
    pass


class ModelRead(ModelBase):
    id: int

    class Config:
        orm_mode = True


class Prompt(BaseModel):
    prompt: str


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: Optional[int] = None
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class TextGenerationBase(BaseModel):
    prompt: str

    @field_validator("prompt")
    def prompt_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Prompt must not be empty")
        return value


class TextGenerationCreate(TextGenerationBase):
    pass


class TextGenerationRead(TextGenerationBase):
    generated_text: str

    class Config:
        orm_mode = True


class TextGenerationUpdate(TextGenerationBase):
    generated_text: str
