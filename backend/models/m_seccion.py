"""Modelo de la tabla secciones."""
from sqlalchemy import Column, Integer, String

# Necesaio para cada modelo
from ..config.database import Base


class Section(Base):
    """
    Define la tabla de secciones."""

    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    cod = Column(String(10), unique=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(String(255))
