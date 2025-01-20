from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.dependencies import SessionDep, SettingsDep
from app.domain import schemas
from app.error.codes import Errors
from app.error.exceptions import CustomException, UserException
from app.repos import user_repo
from app.services.user_service import (authenticate_user,
                                       create_access_token)
import logging


settings = Settings()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        settings: SettingsDep,
        session: SessionDep,
        form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = authenticate_user(
            session, form_data.username, form_data.password)
        if not user:
            raise UserException(error=Errors.E001, code=404)
        access_token = create_access_token(
            data={"sub": user.username}, settings=settings)
    except CustomException as e:
        # logger.error(f"Error in token generation: {str(e)}")
        raise HTTPException(status_code=e.code, detail=e.error)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, session: SessionDep):
    try:
        return user_repo.create_user(session, user)
    except CustomException as e:
        # logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=e.code, detail=e.error)
