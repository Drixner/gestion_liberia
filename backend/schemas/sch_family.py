"""Esquemas para el modelo Familia"""
from typing import Optional
from pydantic import BaseModel


class FamiliaCreate(BaseModel):
    """Modelo para crear una nueva familia"""

    id: Optional[int]
    cod: str
    nombre: str
    descripcion: Optional[str]
    seccion_id: int  # Asegúrate de incluir el id de la sección a la que pertenece la familia

    class Config:
        """Configuraciones del modelo"""

        from_attributes = True


class FamiliaUpdate(BaseModel):
    """Modelo para actualizar una familia existente"""

    nombre: Optional[str]
    cod: Optional[str]
    descripcion: Optional[str]
    seccion_id: Optional[int]
