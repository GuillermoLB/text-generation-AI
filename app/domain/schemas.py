from typing import Optional
from pydantic import BaseModel, field_validator

from app.error.codes import Errors
from app.error.exceptions import TextGenerationException


class ModelBase(BaseModel):
    max_length: int
    temperature: float
    top_p: float

    @field_validator("max_length")
    def validate_max_length(cls, value):
        if value <= 0:
            raise TextGenerationException(error=Errors.E005, code=400)
        return value

    @field_validator("temperature")
    def validate_temperature(cls, value):
        if not (0.0 <= value <= 1.0):
            raise TextGenerationException(error=Errors.E006, code=400)
        return value

    @field_validator("top_p")
    def validate_top_p(cls, value):
        if not (0.0 <= value <= 1.0):
            raise TextGenerationException(error=Errors.E007, code=400)
        return value


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
            raise TextGenerationException(error=Errors.E004, code=400)
        return value


class TextGenerationCreate(TextGenerationBase):
    pass


class TextGenerationRead(TextGenerationBase):
    generated_text: str

    class Config:
        orm_mode = True


class TextGenerationUpdate(TextGenerationBase):
    generated_text: str
