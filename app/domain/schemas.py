from typing import Optional
from pydantic import BaseModel


class ModelBase(BaseModel):
    name: str
    llm: str
    max_length: int
    temperature: float
    top_p: float


class CreateModel(ModelBase):
    pass


class ReadModel(ModelBase):
    pass


class ReadModel(ModelBase):
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


class TextGenerationCreate(TextGenerationBase):
    pass


class TextGenerationRead(TextGenerationBase):
    generated_text: str

    class Config:
        orm_mode = True
