"""database connection and session creation"""

import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config.database import Base

load_dotenv()  # take environment variables from .env.

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
database_name = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{user}:{password}@127.0.0.1/{database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Función para obtener una sesión de base de datos
def get_db():
    """get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
