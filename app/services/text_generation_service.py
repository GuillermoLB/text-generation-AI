from app.core.config import Settings
from app.domain.models import Model, TextGeneration
from app.ml.text_generation.text_generation_pipeline import get_text_generation_pipeline
from app.repos import model_repo, text_generation_repo
import logging

logger = logging.getLogger(__name__)


def validate_and_create_prompt(prompt: str) -> TextGeneration:
    logger.debug(f"Validating prompt: {prompt}")
    if prompt == "":
        raise ValueError("Prompt is required")
    logger.debug("Prompt is valid")
    logger.debug("Creating text generation record")
    text_generation = TextGeneration(prompt=prompt)
    text_generation = text_generation_repo.create_text_generation(
        text_generation)
    logger.debug("Text generation record created")
    return text_generation


def generate_text(
    text_generation: TextGeneration,
    settings: Settings,
) -> TextGeneration:
    model = model_repo.read_model()
    generator_pipeline = get_text_generation_pipeline(
        model=model, settings=settings)
    prompt = text_generation.prompt
    result = generator_pipeline(prompt=prompt, model=model)
    generated_text = result[0]["generated_text"]
    updated_text_generation = TextGeneration(
        prompt=prompt,
        generated_text=generated_text
    )
    text_generation = text_generation_repo.update_text_generation(
        text_generation, updated_text_generation)
    return text_generation
