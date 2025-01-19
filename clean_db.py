# filepath: /home/guillermo/Prueba-tecnica-Roams/clean_db.py

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app.core.config import Settings


def clean_database():
    settings = Settings()
    connection_str = settings.get_connection_str()
    engine = create_engine(connection_str)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    metadata = MetaData()
    metadata.reflect(bind=engine)

    try:
        for table in reversed(metadata.sorted_tables):
            session.execute(table.delete())
            print(f"Deleted all records from {table.name}")
        session.commit()
        print("All records deleted successfully.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    clean_database()
