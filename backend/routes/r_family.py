""" Rutas para el CRUD de familias """
from fastapi import APIRouter, HTTPException, status
from ..models.m_family import Family
from ..models.m_seccion import Section
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
    if not family.section_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El código de la sección es obligatorio.",
        )

    with SessionLocal() as db:
        # Verificar si la sección existe
        seccion = db.query(Section).filter(Section.id == family.section_id).first()
        if not seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La sección con el código {family.section_id} no existe.",
            )

        new_family = Family(
            name=family.name,
            cod=family.cod,
            description=family.description,
            section_id=family.section_id,
        )
        db.add(new_family)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            ) from e
        db.refresh(new_family)
        return new_family


# Actualizar una familia existente
@Familia.put("/families/{family_id}", response_model=FamiliaUpdate)
async def update_family(family_id: int, family: FamiliaUpdate):
    """update an existing family"""
    db = SessionLocal()
    db_family = db.query(Family).get(family_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    db_family.name = family.name if family.name else db_family.name
    db_family.cod = family.cod if family.cod else db_family.cod
    db_family.description = (
        family.description if family.description else db_family.description
    )
    db_family.section_id = (
        family.section_id if family.section_id else db_family.section_id
    )
    db.commit()
    db.refresh(db_family)
    return FamiliaUpdate(
        name=db_family.name,
        cod=db_family.cod,
        description=db_family.description,
        section_id=db_family.section_id,
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
