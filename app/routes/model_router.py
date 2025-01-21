from typing import List
from fastapi import APIRouter, HTTPException
from app.dependencies import SessionDep, SettingsDep, UserDep
from app.domain.schemas import ModelRead, ModelUpdate
from app.error.exceptions import CustomException
from app.services import model_service
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
    - **name**: Model name
    - **llm**: llm id
    """
    try:
        updated_model = model_service.create_or_update_model(
            session=session, settings=settings, model=model)
        return updated_model
    except CustomException as e:
        # logger.log(f"Error updating model: {e.error}")
        raise HTTPException(status_code=e.code, detail=e.error)
