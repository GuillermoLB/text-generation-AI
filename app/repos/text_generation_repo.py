from sqlalchemy.orm import Session
from app.domain.models import TextGeneration
from app.domain.schemas import TextGenerationCreate, TextGenerationUpdate


def create_text_generation(session: Session, text_generation: TextGenerationCreate) -> TextGeneration:
    db_text_generation = TextGeneration(
        prompt=text_generation.prompt
    )
    session.add(db_text_generation)
    session.commit()
    session.refresh(db_text_generation)
    return db_text_generation


def read_text_generations(session: Session) -> list[TextGeneration]:
    return session.query(TextGeneration).all()


def update_text_generation(session: Session, text_generation_id: int, text_generation_update: TextGenerationUpdate) -> TextGeneration:
    db_text_generation = session.query(TextGeneration).filter(
        TextGeneration.id == text_generation_id).first()
    if text_generation_update.generated_text:
        db_text_generation.generated_text = text_generation_update.generated_text
    session.commit()
    session.refresh(db_text_generation)
    return db_text_generation
