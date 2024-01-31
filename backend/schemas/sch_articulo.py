""" Esquema de Articulo. """
from typing import Optional, List
from pydantic import BaseModel


class CodigoBarraBase(BaseModel):
    """Modelo para el manejo de los códigos de barras."""

    ean: str


class CodigoBarraCreate(CodigoBarraBase):
    """Modelo para crear un nuevo código de barras."""


class CodigoBarra(CodigoBarraBase):
    """Modelo para el manejo de los códigos de barras."""

    id: int

    class Config:
        """Configuración del esquema."""

        from_attributes = True


class ArticuloBase(BaseModel):
    """Modelo para el manejo de los artículos."""

    cod_short: Optional[str]
    name: str
    description: Optional[str]
    codigos_barras: List[CodigoBarraCreate] = []
    family_id: int
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
    description: Optional[str]
    ean: List[CodigoBarraCreate] = []
    family_id: Optional[int]
    purchase_price: Optional[float]
    sale_price: Optional[float]
    und: Optional[str]
    tax: Optional[float]


class Articulo(ArticuloBase):
    """Modelo para el manejo de los artículos."""

    id: int

    class Config:
        """Configuración del esquema."""

        from_attributes = True
