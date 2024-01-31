"""Rutas para el recurso Articulo"""
# Importaciones de la biblioteca estándar
import random
import string
from typing import List

# Importaciones de terceros
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

# Importaciones locales de la aplicación
from ..config.db import get_db
from ..models.m_articulo import (
    Articulo as ArticuloModel,
    CodigoBarra as CodigoBarraModel,
)
from ..schemas.sch_articulo import Articulo, ArticuloCreate


articulo_router = APIRouter()


# Obtener todos los artículos
@articulo_router.get("/articulos/", response_model=List[Articulo])
async def get_articulos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los artículos"""
    articulos = db.query(ArticuloModel).offset(skip).limit(limit).all()
    return articulos


@articulo_router.get("/articulos/{articulo_id}", response_model=Articulo)
async def read_articulo(articulo_id: int, db: Session = Depends(get_db)):
    """Obtener un artículo por su ID"""
    db_articulo = (
        db.query(ArticuloModel).filter(ArticuloModel.id == articulo_id).first()
    )
    if db_articulo is None:
        raise HTTPException(status_code=404, detail="Articulo not found")
    return db_articulo


# Crear un nuevo artículo
@articulo_router.post("/articulos/", response_model=Articulo)
async def create_articulo(articulo: ArticuloCreate, db: Session = Depends(get_db)):
    """Crear un nuevo artículo"""
    # Generar código corto
    articulo.cod_short = "".join(random.choices(string.digits, k=6))

    db_articulo = ArticuloModel(**articulo.dict())
    db.add(db_articulo)
    db.commit()
    db.refresh(db_articulo)

    # Generar código de barras
    codigo_barra = "".join(random.choices(string.digits, k=13))
    db_codigo = CodigoBarraModel(
        codigos_barras=codigo_barra, articulo_id=db_articulo.id
    )
    db.add(db_codigo)
    db.commit()

    return db_articulo


# Actualizar un artículo por su ID
@articulo_router.put("/articulos/{articulo_id}", response_model=Articulo)
def update_articulo(
    articulo_id: int, articulo: ArticuloCreate, db: Session = Depends(get_db)
):
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
@articulo_router.delete("/articulos/{articulo_id}", response_model=Articulo)
def delete_articulo(articulo_id: int, db: Session = Depends(get_db)):
    """Eliminar un artículo por su ID"""
    db_articulo = (
        db.query(ArticuloModel).filter(ArticuloModel.id == articulo_id).first()
    )
    if db_articulo is None:
        raise HTTPException(status_code=404, detail="Articulo not found")
    db.delete(db_articulo)
    db.commit()
    return db_articulo
