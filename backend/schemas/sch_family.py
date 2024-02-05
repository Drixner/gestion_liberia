"""Esquemas para el modelo Familia"""

from typing import Optional
from pydantic import BaseModel


class FamiliaCreate(BaseModel):
    """Modelo para crear una nueva familia"""

    id: Optional[int]
    cod: str
    name: str
    section_name: Optional[str]

    class Config:
        """Configuraciones del modelo"""

        from_attributes = True


class FamiliaResponse(BaseModel):
    """Modelo para la respuesta de una familia"""

    id: int
    cod: str
    name: str
    section_name: str


class FamiliaUpdate(BaseModel):
    """Modelo para actualizar una familia existente"""

    name: Optional[str]
    cod: Optional[str]
    section_name: Optional[str]
