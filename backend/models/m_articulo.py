"""Modelo de la tabla secciones."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

# Necesaio para cada modelo
from ..config.database import Base


class Articulo(Base):
    """Define la tabla de artículos."""

    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True, index=True)
    cod_short = Column(String(6), unique=True, index=True)
    name = Column(String)
    description = Column(String)
    ean = relationship("CodigoBarra", back_populates="articulo")
    family_id = Column(Integer, ForeignKey("families.id"))
    purchase_price = Column(Float)
    sale_price = Column(Float)
    und = Column(String)
    tax = Column(Float, default=0.18)


class CodigoBarra(Base):
    """Define la tabla de códigos de barras."""

    __tablename__ = "codigos_barras"

    id = Column(Integer, primary_key=True, index=True)
    ean = Column(String, unique=True, index=True)
    articulo_id = Column(Integer, ForeignKey("articulos.id"))
    articulo = relationship("Articulo", back_populates="codigos_barras")
