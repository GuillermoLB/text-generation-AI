from typing import List
from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep, SettingsDep
from app.domain.schemas import ModelCreate, ModelRead, TextGenerationRead, TextGenerationCreate
from app.domain.models import TextGeneration
from app.repos import model_repo, text_generation_repo
from app.services import model_service, text_generation_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=TextGenerationRead)
def generate_text(
    text_generation_create: TextGenerationCreate,
    settings: SettingsDep,
    session: SessionDep,
):

    logger.info(f"Generating text for prompt: {
                text_generation_create.prompt}")

    model = model_repo.read_model(
        session=session, name=settings.MODEL_NAME)
    # TODO: Add custom error if no model is found
    text_generation = text_generation_repo.create_text_generation(
        session=session, text_generation=text_generation_create)
    text_generation = text_generation_service.generate_text(session=session, settings=settings, model=model,
                                                            text_generation=text_generation)
    logger.info(f"Generated text: {text_generation.generated_text}")
    return text_generation


@router.post("/configure", response_model=ModelRead)
def configure_model(
    model: ModelCreate,
    settings: SettingsDep,
    session: SessionDep,
):
    model_service.create_or_update_model(
        session=session, settings=settings, model=model)
    return model


@router.get("/history", response_model=List[TextGenerationRead])
def get_history(
    session: SessionDep
):
    records = text_generation_repo.read_text_generations(session=session)
    return records
