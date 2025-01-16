from sqlalchemy.orm import Session
from app.domain.models import TextGeneration


def create_text_generation(session: Session, text_generation: TextGeneration) -> TextGeneration:
    db_text_generation = TextGeneration(
        prompt=text_generation.prompt
    )
    if text_generation.generated_text:
        db_text_generation.generated_text = text_generation.generated_text
    session.add(db_text_generation)
    session.commit()
    session.refresh(db_text_generation)
    return db_text_generation


def read_text_generations(session: Session) -> list[TextGeneration]:
    return session.query(TextGeneration).all()


def update_text_generation(session: Session, text_generation: TextGeneration, text_generation_update: TextGeneration) -> TextGeneration:
    db_text_generation = session.query(TextGeneration).filter(
        TextGeneration.id == text_generation.id).first()
    db_text_generation.prompt = text_generation_update.prompt
    db_text_generation.generated_text = text_generation_update.generated_text
    session.commit()
    session.refresh(db_text_generation)
    return db_text_generation
