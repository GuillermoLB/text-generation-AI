from sqlalchemy.orm import Session
from app.domain.models import Model


def create_model(session: Session, name: str, llm: str, max_length: int, temperature: float, top_p: float) -> Model:
    db_model = Model(
        name=name,
        llm=llm,
        max_length=max_length,
        temperature=temperature,
        top_p=top_p
    )
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    return db_model


def read_model(session: Session, name: str) -> Model:
    return session.query(Model).filter(Model.name == name).first()
