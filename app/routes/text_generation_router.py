from typing import List
from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep, SettingsDep, UserDep
from app.domain.schemas import ModelCreate, ModelRead, TextGenerationRead, TextGenerationCreate
from app.domain.models import TextGeneration
from app.error.codes import Errors
from app.error.exceptions import CustomException, ModelException
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
    current_user: UserDep,
):
    try:
        logger.info(f"Generating text for prompt: {
                    text_generation_create.prompt}")

        model = model_repo.read_model_by_name(
            session=session, name=settings.MODEL_NAME)
        if not model:
            raise ModelException(error=Errors.E001, code=404)

        text_generation = text_generation_repo.create_text_generation(
            session=session, text_generation=text_generation_create)
        text_generation = text_generation_service.generate_text(
            session=session,
            settings=settings,
            model=model,
            text_generation=text_generation
        )

        logger.info(f"Generated text: {text_generation.generated_text}")
        return text_generation

    except CustomException as e:
        # logger.error(f"Error generating text: {e.error}")
        raise HTTPException(status_code=e.code, detail=e.error)


@router.get("/text_generations/all", response_model=List[TextGenerationRead])
def read_text_generations(
    session: SessionDep,
    current_user: UserDep,
):
    try:
        records = text_generation_repo.read_text_generations(session=session)
        return records
    except CustomException as e:
        # logger.error(f"Error reading history: {e.error}")
        raise HTTPException(status_code=e.code, detail=e.error)
