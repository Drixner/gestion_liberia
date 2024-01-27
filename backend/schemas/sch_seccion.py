"""Esquema para el manejo de las secciones"""
from typing import Optional
from pydantic import BaseModel


class SeccionCreate(BaseModel):
    """Modelo para crear una nueva sección"""

    id: Optional[int]
    cod: str
    nombre: str
    descripcion: Optional[str]

    class Config:
        """Configuraciones del modelo"""

        from_attributes = True


class SeccionUpdate(BaseModel):
    """Modelo para actualizar una sección existente"""

    nombre: Optional[str]
    cod: Optional[str]
    descripcion: Optional[str]
