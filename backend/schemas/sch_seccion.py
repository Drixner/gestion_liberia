"""Esquema para el manejo de las secciones"""

from typing import Optional
from pydantic import BaseModel


class SeccionCreate(BaseModel):
    """Modelo para crear una nueva sección"""

    cod: Optional[str]
    nombre: str

    class Config:
        """Configuraciones del modelo"""

        from_attributes = True


class SeccionUpdate(BaseModel):
    """Modelo para actualizar una sección existente"""

    nombre: Optional[str]
    cod: Optional[str]
