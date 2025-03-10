from typing import Optional
from sqlalchemy import Boolean, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    disabled: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)


class Model(Base):
    __tablename__ = 'models'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    llm: Mapped[str] = mapped_column(String, nullable=False)
    max_length: Mapped[int] = mapped_column(Integer, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    top_p: Mapped[float] = mapped_column(Float, nullable=False)


class TextGeneration(Base):
    __tablename__ = 'text_generations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    prompt: Mapped[str] = mapped_column(String, nullable=False)
    generated_text: Mapped[Optional[str]
                           ] = mapped_column(String, nullable=True)
