from app.core.config import Settings
from sqlalchemy.orm import Session
from app.domain.models import Model, TextGeneration
from app.ml.text_generation.text_generation_pipeline import get_text_generation_pipeline
from app.repos import model_repo, text_generation_repo
import logging

logger = logging.getLogger(__name__)


def generate_text(
    session: Session,
    settings: Settings,
    model: Model,
    text_generation: TextGeneration,
) -> TextGeneration:
    generator_pipeline = get_text_generation_pipeline(
        model=model)
    prompt = text_generation.prompt
    logger.debug(f"Prompt: {prompt}")
    result = generator_pipeline(text_inputs=prompt, max_length=model.max_length,
                                temperature=model.temperature, top_p=model.top_p)
    generated_text = result[0]["generated_text"]
    logger.debug(f"Text generated: {generated_text}")
    updated_text_generation = TextGeneration(
        prompt=prompt,
        generated_text=generated_text
    )
    text_generation = text_generation_repo.update_text_generation(session=session,
                                                                  text_generation_id=text_generation.id, text_generation_update=updated_text_generation)
    return text_generation
