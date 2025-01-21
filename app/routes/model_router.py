from typing import List
from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep, SettingsDep, UserDep
from app.domain.schemas import ModelCreate, ModelRead, ModelUpdate, TextGenerationRead, TextGenerationCreate
from app.domain.models import TextGeneration
from app.error.exceptions import CustomException
from app.repos import model_repo, text_generation_repo
from app.services import model_service, text_generation_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.put("/models",
            response_model=ModelRead,
            summary="Update model parameters",
            responses={
                200: {
                    "description": "Successfully updated model",
                    "content": {
                        "application/json": {
                            "example": {
                                "max_length": 100,
                                "temperature": 0.7,
                                "top_p": 0.9
                            }
                        }
                    }
                },
                400: {
                    "description": "Not correct value..."
                },
                401: {
                    "description": "Invalid or expired token"
                }
            })
def update_model(
    model: ModelUpdate,
    settings: SettingsDep,
    session: SessionDep,
    current_user: UserDep,
):
    """
    Update model configuration parameters.

    Requires valid authentication token.

    Parameters:
    - **max_length**: Maximum length of generated text
    - **temperature**: Sampling temperature
    - **top_p**: Top-p sampling parameter

    Returns:
    - **max_length**: Maximum length of generated text
    - **temperature**: Sampling temperature
    - **top_p**: Top-p sampling parameter
    """
    try:
        model_service.create_or_update_model(
            session=session, settings=settings, model=model)
        return model
    except CustomException as e:
        # logger.log(f"Error updating model: {e.error}")
        raise HTTPException(status_code=e.code, detail=e.error)
