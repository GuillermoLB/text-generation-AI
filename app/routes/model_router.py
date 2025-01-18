from typing import List
from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep, SettingsDep
from app.domain.schemas import ModelCreate, ModelRead, TextGenerationRead, TextGenerationCreate
from app.domain.models import TextGeneration
from app.error.exceptions import CustomException
from app.repos import model_repo, text_generation_repo
from app.services import model_service, text_generation_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.put("/models", response_model=ModelRead)
def update_model(
    model: ModelCreate,
    settings: SettingsDep,
    session: SessionDep,
):
    try:
        model_service.create_or_update_model(
            session=session, settings=settings, model=model)
        return model
    except CustomException as e:
        raise HTTPException(status_code=e.code, detail=e.error)
