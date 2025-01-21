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


@router.post("/text_generations",
             response_model=TextGenerationRead,
             summary="Generate text from prompt",
             responses={
                 200: {
                     "description": "Successfully generated text",
                     "content": {
                         "application/json": {
                             "example": {
                                 "prompt": "Write a story about a dragon",
                                 "generated_text": "Once upon a time, there was a mighty dragon...",
                             }
                         }
                     }
                 },
                 400: {"description": "Invalid prompt or parameters"},
                 401: {"description": "Invalid or expired token"},
                 404: {"description": "Model not found"},
                 500: {"description": "Internal server error or AI service unavailable"}
             })
async def create_text_generation(
    text_generation_create: TextGenerationCreate,
    settings: SettingsDep,
    session: SessionDep,
    current_user: UserDep,
):
    """
    Generate text using AI model based on provided prompt.

    Requires valid authentication token.

    Parameters:
    - **prompt**: The input text to generate from

    Returns:
    - **prompt**: Original input text 
    - **generated_text**: AI generated response
    """
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
        raise HTTPException(status_code=e.code, detail=e.error)


@router.get(
    "/text_generations/all",
    response_model=List[TextGenerationRead],
    summary="Get all text generations",
    responses={
        200: {
            "description": "Successfully retrieved text generations",
            "content": {
                "application/json": {
                    "example": [{
                        "prompt": "Example prompt",
                        "generated_text": "Generated response"
                    }]
                }
            }
        },
        401: {"description": "User not authenticated"},
        500: {"description": "Internal server error"}
    }
)
def read_text_generations(
    session: SessionDep,
    current_user: UserDep,
) -> List[TextGenerationRead]:
    """
    Retrieve all text generation records from the database.

    Requires valid authentication token.

    Returns:
    - **List[TextGenerationRead]**: List of text generation records
    """
    try:
        records = text_generation_repo.read_text_generations(session=session)
        return records
    except CustomException as e:
        raise HTTPException(status_code=e.code, detail=e.error)
