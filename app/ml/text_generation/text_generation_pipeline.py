from transformers import pipeline

from app.core.config import Settings
from app.domain.models import Model


def get_text_generation_pipeline(model: Model) -> pipeline:

    text_generation_pipeline = pipeline("text-generation", model=model.llm)
    return text_generation_pipeline
