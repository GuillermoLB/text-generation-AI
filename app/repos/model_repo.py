from sqlalchemy.orm import Session
from app.domain.models import Model
from app.domain.schemas import ModelCreate, ModelUpdate

# TODO: arguments should be schemas


def create_model(session: Session, model: ModelCreate) -> Model:
    db_model = Model(
        name=model.name,
        llm=model.llm,
        max_length=model.max_length,
        temperature=model.temperature,
        top_p=model.top_p
    )
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    return db_model


def read_model(session: Session, name: str) -> Model:
    return session.query(Model).filter(Model.name == name).first()


def update_model(session: Session, name: str, model: ModelUpdate) -> Model:
    db_model = session.query(Model).filter(Model.name == name).first()
    db_model.max_length = model.max_length
    db_model.temperature = model.temperature
    db_model.top_p = model.top_p
    session.commit()
    session.refresh(db_model)
    return db_model
