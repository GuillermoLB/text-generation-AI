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


@router.post("/text_generations", response_model=TextGenerationRead)
def create_text_generation(
    text_generation_create: TextGenerationCreate,
    settings: SettingsDep,
    session: SessionDep,
):
    try:
        logger.info(f"Generating text for prompt: {
                    text_generation_create.prompt}")

        model = model_repo.read_model(
            session=session, name=settings.MODEL_NAME)
        text_generation = text_generation_repo.create_text_generation(
            session=session, text_generation=text_generation_create)
        text_generation = text_generation_service.generate_text(session=session, settings=settings, model=model,
                                                                text_generation=text_generation)
        logger.info(f"Generated text: {text_generation.generated_text}")
        return text_generation
    except CustomException as e:
        raise HTTPException(status_code=e.code, detail=e.error)


@router.get("/text_generations/all", response_model=List[TextGenerationRead])
def read_text_generations(
    session: SessionDep
):
    try:
        records = text_generation_repo.read_text_generations(session=session)
        return records
    except CustomException as e:
        raise HTTPException(status_code=e.code, detail=e.error)
