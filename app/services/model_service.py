

from app.core.config import Settings
from app.domain.models import Model
from app.repos import model_repo


def configure_model(settings: Settings, max_length: int,
                    temperature: float,
                    top_p: float,) -> Model:
    model = model_repo.create_model(name=settings.MODEL_NAME,
                                    llm=settings.LLM_ID,
                                    max_length=max_length,
                                    temperature=temperature,
                                    top_p=top_p)
    return model
