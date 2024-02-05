""" Esquema de Articulo. """

from typing import Optional, List
from pydantic import BaseModel


class CodigoBarraBase(BaseModel):
    """Modelo base para el manejo de los códigos de barras."""

    codigos_barras: Optional[str]


class CodigoBarraCreate(CodigoBarraBase):
    """Modelo para crear un nuevo código de barras."""


class CodigoBarra(CodigoBarraBase):
    """Modelo completo para el manejo de los códigos de barras, incluyendo el ID."""

    id: int

    class Config:
        """Configuración del esquema."""

        from_attributes = True


class ArticuloBase(BaseModel):
    """Modelo base para el manejo de los artículos."""

    cod_short: Optional[str] = None  # Se generará automáticamente si no se proporciona
    name: str  # Asumiendo que quieres agregar una descripción
    codigos_barras: List[CodigoBarraCreate] = []
    family_name: Optional[str] = (
        None  # Añadir el nombre de la familia en lugar de family_id
    )
    purchase_price: float
    sale_price: float
    und: str
    tax: float = 0.18


class ArticuloCreate(ArticuloBase):
    """Modelo para crear un nuevo artículo."""


class ArticuloUpdate(BaseModel):
    """Modelo para actualizar un artículo."""

    name: Optional[str]
    cod_short: Optional[str]
    codigos_barras: List[CodigoBarraCreate] = []
    family_name: Optional[str] = (
        None  # Usar el nombre de la familia para actualizaciones
    )
    purchase_price: Optional[float]
    sale_price: Optional[float]
    und: Optional[str]
    tax: Optional[float]


class Articulo(ArticuloBase):
    """Modelo completo para el manejo de los artículos"""

    id: int
    family_id: (
        int  # Mantener el ID de la familia en la respuesta para referencias internas
    )

    class Config:
        """Configuración del esquema."""

        from_attributes = True


class ArticulosResponse(BaseModel):
    """Modelo de respuesta para obtener una lista de artículos."""

    articulos: List[Articulo]
