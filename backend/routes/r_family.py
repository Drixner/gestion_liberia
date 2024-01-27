""" Rutas para el CRUD de familias """
from fastapi import APIRouter, HTTPException
from ..models.m_family import Family
from ..config.db import SessionLocal
from ..schemas.sch_family import FamiliaCreate, FamiliaUpdate

Familia = APIRouter()


# Obtener todas las familias
@Familia.get("/families")
async def get_families():
    """get all families"""
    db = SessionLocal()
    families = db.query(Family).all()
    return {"families": families}


# Crear una nueva familia
@Familia.post("/families", response_model=FamiliaCreate)
async def create_family(family: FamiliaCreate):
    """create a new family"""
    with SessionLocal() as db:
        new_family = Family(
            name=family.nombre,
            cod=family.cod,
            description=family.descripcion,
            section_id=family.seccion_id,
        )
        db.add(new_family)
        db.commit()
        db.refresh(new_family)
        return family


# Actualizar una familia existente
@Familia.put("/families/{family_id}", response_model=FamiliaUpdate)
async def update_family(family_id: int, family: FamiliaUpdate):
    """update an existing family"""
    db = SessionLocal()
    db_family = db.query(Family).get(family_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    db_family.name = family.nombre if family.nombre else db_family.name
    db_family.cod = family.cod if family.cod else db_family.cod
    db_family.description = (
        family.descripcion if family.descripcion else db_family.description
    )
    db_family.section_id = (
        family.seccion_id if family.seccion_id else db_family.section_id
    )
    db.commit()
    db.refresh(db_family)
    return FamiliaUpdate(
        nombre=db_family.name,
        cod=db_family.cod,
        descripcion=db_family.description,
        seccion_id=db_family.section_id,
    )


# Eliminar una familia
@Familia.delete("/families/{family_id}")
async def delete_family(family_id: int):
    """delete an existing family"""
    db = SessionLocal()
    family = db.query(Family).get(family_id)
    if family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    db.delete(family)
    db.commit()
    return {"message": "Family deleted"}
