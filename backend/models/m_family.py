"""Modelo de tabla familia"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Necesaio para cada modelo
from ..config.database import Base


class Family(Base):
    """Define la tabla de familias."""

    __tablename__ = "families"
    id = Column(Integer, primary_key=True, index=True)
    cod = Column(String(10), unique=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(String(255))
    section_id = Column(Integer, ForeignKey("sections.id"))
    section = relationship("Section", back_populates="families")
