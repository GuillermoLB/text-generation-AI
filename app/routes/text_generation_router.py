from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import Settings

from app.dependencies import SessionDep, SettingsDep
from app.domain.schemas import CreateModel, ReadModel, TextGenerationRead, TextGenerationCreate
from app.domain.models import TextGeneration
from app.repos import model_repo, text_generation_repo
from app.services import text_generation_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=TextGenerationRead)
def generate_text(
    text_generation_create: TextGenerationCreate,
    settings: SettingsDep,
    session: SessionDep,
):
    try:
        logger.info(f"Generating text for prompt: {
                    text_generation_create.prompt}")
        text_generation = text_generation_service.validate_and_create_prompt(
            text_generation_create.prompt)
        logger.info(f"Generated text: {text_generation.generated_text}")
        return "Generation successful"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/configure", response_model=ReadModel)
def configure_model(
    model: CreateModel,
    settings: SettingsDep,
    session: SessionDep,
):
    try:
        model_repo.create_model(
            name=settings.MODEL_NAME,
            llm=settings.LLM_ID,
            max_length=model.max_length,
            temperature=model.temperature,
            top_p=model.top_p
        )
        return "Model configuration updated successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=List[TextGenerationRead])
def get_history(
    session: SessionDep
):
    records = text_generation_repo.read_text_generations(session=session)
    return records
