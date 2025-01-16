from typing import Optional
from pydantic import BaseModel


class ConfigureModel(BaseModel):
    max_length: int = 50
    temperature: float = 1.0
    top_p: float = 0.9


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
