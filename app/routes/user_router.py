from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import Settings
from app.dependencies import SessionDep, SettingsDep
from app.domain.schemas import Token, UserCreate, UserRead
from app.error.exceptions import CustomException
from app.repos import user_repo
from app.services.user_service import (authenticate_user,
                                       create_access_token)
import logging


settings = Settings()
router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/token",
             response_model=Token,
             summary="Create access token",
             responses={
                 200: {
                     "description": "Successfully created access token",
                     "content": {
                         "application/json": {
                             "example": {
                                 "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                 "token_type": "bearer"
                             }
                         }
                     }
                 },
                 400: {
                     "description": "Incorrect username or password"
                 }
             })
async def login_for_access_token(
    settings: SettingsDep,
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()

):
    """
    Create JWT access token for authentication.

    Parameters:
    - **username**: Required username
    - **password**: Required password

    Returns:
    - **access_token**: JWT token for authentication
    - **token_type**: Bearer
    """
    try:
        user = authenticate_user(
            session, form_data.username, form_data.password)
        access_token = create_access_token(
            data={"sub": user.username}, settings=settings)
    except CustomException as e:
        raise HTTPException(status_code=e.code, detail=e.error)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users",
             response_model=UserRead,
             summary="Create new user",
             responses={
                 200: {
                     "description": "Successfully created user",
                     "content": {
                         "application/json": {
                             "example": {
                                 "id": 1,
                                 "username": "johndoe",
                                 "disabled": False
                             }
                         }
                     }
                 },
                 400: {
                     "description": "Username already exists",
                     "content": {
                         "application/json": {
                             "example": {"detail": "[E008] Username johndoe already exists"}
                         }
                     }
                 }
             })
def create_user(user: UserCreate, session: SessionDep):
    """
    Create a new user account.

    Parameters:
    - **username**: Required unique username
    - **password**: Required password for the account

    Returns:
    - **username**: Username of the created user
    (password is not returned)
    """
    try:
        return user_repo.create_user(session, user)
    except CustomException as e:
        raise HTTPException(status_code=e.code, detail=e.error)
