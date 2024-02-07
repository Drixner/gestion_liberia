"""Rutas para el recurso Articulo"""

# Importaciones de la biblioteca estándar
import random
import string
from typing import List

# Importaciones de terceros
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Importaciones locales de la aplicación
from ..config.db import get_db
from ..models.m_articulo import (
    Articulo as ArticuloModel,
    CodigoBarra as CodigoBarraModel,
)
from ..schemas.sch_articulo import Articulo, ArticuloCreate, ArticulosResponse
from ..models.m_family import Family


articulo_router = APIRouter()


# Obtener una lista de articulos
@articulo_router.get(
    "/articulos", response_model=ArticulosResponse
)  # Cambia List[Articulo] por ArticulosResponse
async def get_articulos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todos los artículos de la base de datos."""
    articulos = db.query(ArticuloModel).offset(skip).limit(limit).all()
    return ArticulosResponse(articulos=articulos)


# Obtener articulo por código de barra
@articulo_router.get("/articulos/codigo/{codigo_barra}", response_model=Articulo)
async def read_articulo_by_codigo(codigo_barra: str, db: Session = Depends(get_db)):
    """Obtener un artículo por su código de barra"""
    db_articulo = (
        db.query(ArticuloModel)
        .join(CodigoBarraModel)
        .filter(CodigoBarraModel.codigos_barras == codigo_barra)
        .first()
    )
    if db_articulo is None:
        raise HTTPException(status_code=404, detail="Articulo not found")
    return db_articulo


# Obtener articulo por nombre
@articulo_router.get("/articulos/nombre/{nombre}", response_model=List[Articulo])
async def read_articulo_by_nombre(nombre: str, db: Session = Depends(get_db)):
    """Obtener un artículo por su nombre"""
    db_articulos = (
        db.query(ArticuloModel).filter(ArticuloModel.name.ilike(f"%{nombre}%")).all()
    )
    if not db_articulos:
        raise HTTPException(status_code=404, detail="Articulo not found")
    return db_articulos


def generar_codigo_barra_aleatorio():
    """Generar un código de barras aleatorio"""
    base = "775" + "".join(random.choices(string.digits, k=9))
    digito_control = calcular_digito_control_ean13(base)
    return base + digito_control


def calcular_digito_control_ean13(base):
    """Calcular el dígito de control de un código EAN-13."""
    suma = sum((3 if i % 2 == 0 else 1) * int(n) for i, n in enumerate(base[:12]))
    modulo = suma % 10
    digito_control = (10 - modulo) % 10
    return str(digito_control)


# Crear un nuevo artículo
@articulo_router.post("/articulos/", response_model=Articulo)
async def create_articulo(articulo_data: ArticuloCreate, db: Session = Depends(get_db)):
    """Crear un nuevo artículo."""
    # Generar código corto único
    while True:
        cod_short = "".join(random.choices(string.digits, k=6))
        if (
            not db.query(ArticuloModel)
            .filter(ArticuloModel.cod_short == cod_short)
            .first()
        ):
            break

    # Encontrar el ID de la familia por el nombre
    familia = db.query(Family).filter(Family.name == articulo_data.family_name).first()
    if not familia:
        raise HTTPException(status_code=404, detail="Familia not found")

    # Preparar el diccionario
    articulo_dict = articulo_data.dict(
        exclude_unset=True, exclude={"family_name", "codigos_barras"}
    )
    articulo_dict.update({"family_id": familia.id, "cod_short": cod_short})

    db_articulo = ArticuloModel(**articulo_dict)
    try:
        db.add(db_articulo)
        db.commit()
        db.refresh(db_articulo)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Error al crear el artículo, posible duplicado."
        ) from exc

    # Manejar códigos de barras
    codigos_barras_provided = articulo_data.codigos_barras
    if codigos_barras_provided:
        for codigo in codigos_barras_provided:
            db_codigo = CodigoBarraModel(
                codigos_barras=codigo.codigos_barras, articulo_id=db_articulo.id
            )
            db.add(db_codigo)
    else:
        # Generar un código de barras si no se proporciona ninguno
        codigo_barra = generar_codigo_barra_aleatorio()
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
