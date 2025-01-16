from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import Settings

from app.dependencies import SessionDep, SettingsDep
from app.domain.schemas import Prompt, ConfigureModel
from app.services import text_generation_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=str)
def generate_text(
    prompt: Prompt,
    config: ConfigureModel,
    settings: SettingsDep,
    session: SessionDep,
):
    try:
        logger.info(f"Generating text for prompt: {prompt.prompt}")
        text_generation = text_generation_service.validate_prompt(
            prompt.prompt)

        return generated_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/configure", response_model=str)
def configure_model_endpoint(
    config: ConfigureModel,
    settings: SettingsDep,
    session: SessionDep,
):
    try:
        text_generation_service.configure_model(
            settings=settings,
            max_length=config.max_length,
            temperature=config.temperature,
            top_p=config.top_p
        )
        return "Model configuration updated successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
