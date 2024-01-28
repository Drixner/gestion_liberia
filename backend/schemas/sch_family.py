"""Esquemas para el modelo Familia"""
from typing import Optional
from pydantic import BaseModel


class FamiliaCreate(BaseModel):
    """Modelo para crear una nueva familia"""

    id: Optional[int]
    cod: str
    name: str
    description: Optional[str]
    section_id: int  # Asegúrate de incluir el id de la sección a la que pertenece la familia

    class Config:
        """Configuraciones del modelo"""

        from_attributes = True


class FamiliaUpdate(BaseModel):
    """Modelo para actualizar una familia existente"""

    name: Optional[str]
    cod: Optional[str]
    description: Optional[str]
    section_id: Optional[int]
