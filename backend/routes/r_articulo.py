"""Rutas para el recurso Articulo"""
# Importaciones de la biblioteca estándar
import random
import string
from typing import List

# Importaciones de terceros
from fastapi import APIRouter, HTTPException

# Importaciones locales de la aplicación
from ..config.db import SessionLocal
from ..models.m_articulo import (
    Articulo as ArticuloModel,
    CodigoBarra as CodigoBarraModel,
)
from ..schemas.sch_articulo import Articulo, ArticuloCreate


Articulo = APIRouter()


# Obtener todos los artículos
@Articulo.get("/articulos/", response_model=List[Articulo])
async def read_articulos(skip: int = 0, limit: int = 100, db=SessionLocal):
    """Obtener todos los artículos"""
    articulos = db.query(ArticuloModel).offset(skip).limit(limit).all()
    return articulos


@Articulo.get("/articulos/{articulo_id}", response_model=Articulo)
async def read_articulo(articulo_id: int, db=SessionLocal):
    """Obtener un artículo por su ID"""
    db_articulo = (
        db.query(ArticuloModel).filter(ArticuloModel.id == articulo_id).first()
    )
    if db_articulo is None:
        raise HTTPException(status_code=404, detail="Articulo not found")
    return db_articulo


# Crear un nuevo artículo
@Articulo.post("/articulos/", response_model=Articulo)
async def create_articulo(articulo: ArticuloCreate, db=SessionLocal):
    """Crear un nuevo artículo"""
    # Generar código corto
    articulo.cod_short = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )

    # Generar código de barras
    codigo_barra = "".join(random.choices(string.digits, k=13))
    db_codigo = CodigoBarraModel(ean=codigo_barra)
    db.add(db_codigo)

    db_articulo = ArticuloModel(**articulo.dict())
    db.add(db_articulo)
    db.commit()
    db.refresh(db_articulo)
    return db_articulo


# Actualizar un artículo por su ID
@Articulo.put("/articulos/{articulo_id}", response_model=Articulo)
def update_articulo(articulo_id: int, articulo: ArticuloCreate, db=SessionLocal):
    """Actualizar un artículo por su ID"""
    db_articulo = (
        db.query(ArticuloModel).filter(ArticuloModel.id == articulo_id).first()
    )
    if db_articulo is None:
        raise HTTPException(status_code=404, detail="Articulo not found")
    for var, value in vars(articulo).items():
        if value:
            setattr(db_articulo, var, value)
    db.add(db_articulo)
    db.commit()
    db.refresh(db_articulo)
    return db_articulo


# Eliminar un artículo por su ID
@Articulo.delete("/articulos/{articulo_id}", response_model=Articulo)
def delete_articulo(articulo_id: int, db=SessionLocal):
    """Eliminar un artículo por su ID"""
    db_articulo = (
        db.query(ArticuloModel).filter(ArticuloModel.id == articulo_id).first()
    )
    if db_articulo is None:
        raise HTTPException(status_code=404, detail="Articulo not found")
    db.delete(db_articulo)
    db.commit()
    return db_articulo
