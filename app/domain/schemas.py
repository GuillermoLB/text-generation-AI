from typing import Optional
from pydantic import BaseModel, field_validator


class ModelBase(BaseModel):
    max_length: int
    temperature: float
    top_p: float
    # TODO: validator for max_length, temperature, top_p


class ModelCreate(ModelBase):
    name: str
    llm: str


class ModelRead(ModelBase):
    max_length: int
    temperature: float
    top_p: float

    class Config:
        orm_mode = True


class ModelUpdate(ModelBase):
    pass


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
