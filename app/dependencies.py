from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.domain.models import User as UserModel
from app.domain.schemas import User
from app.error.codes import Errors
from app.error.exceptions import AuthenticationException
from app.services.user_service import verify_token

from .core.config import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@lru_cache
def get_settings():
    return Settings()


# Create the SQLAlchemy engine
engine = create_engine(get_settings().get_connection_str())

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_user(
    db: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
    try:
        token_data = verify_token(token, get_settings(), None)
        user = db.query(UserModel).filter(
            UserModel.username == token_data.username).first()
        if user is None:
            raise AuthenticationException(
                error=Errors.E011, code=401)  # User not found
        return user
    except AuthenticationException as e:
        raise HTTPException(
            status_code=e.code,
            detail=Errors.E010,  # Invalid or expired token
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise AuthenticationException(error=Errors.E003, code=400)
    return current_user


SessionDep = Annotated[Session, Depends(get_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
UserDep = Annotated[User, Depends(get_current_active_user)]
