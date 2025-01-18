from requests import Session
from app.core.config import Settings
from app.domain.models import Model
from app.domain.schemas import ModelCreate, ModelUpdate
from app.repos import model_repo
import logging

logger = logging.getLogger(__name__)


def create_or_update_model(session: Session, settings: Settings, model: ModelUpdate) -> Model:
    name = settings.MODEL_NAME
    existing_model = model_repo.read_model_by_name(session=session, name=name)
    if existing_model:
        model_repo.update_model(
            session=session, name=name, model=model)
        logger.debug(f"Updated model: {name}")
        return existing_model
    # If model does not exist, create a new one
    model_create = ModelCreate(
        name=name,
        llm=settings.LLM_ID,
        max_length=model.max_length,
        temperature=model.temperature,
        top_p=model.top_p
    )
    model = model_repo.create_model(session=session, model=model_create)
    logger.debug(f"Created model: {name}")
    return model
