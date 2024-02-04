""" Rutas para el CRUD de secciones """

from fastapi import APIRouter, HTTPException
from ..models.m_seccion import Section
from ..config.db import SessionLocal
from ..schemas.sch_seccion import SeccionCreate, SeccionUpdate

Seccion = APIRouter()


# Obtener todas las secciones
@Seccion.get("/sections")
async def get_sections():
    """get all sections"""
    db = SessionLocal()
    sections = db.query(Section).all()
    return {"sections": sections}


# Crear una nueva sección
@Seccion.post("/sections", response_model=SeccionCreate)
async def create_section(section: SeccionCreate):
    """create a new section"""
    with SessionLocal() as db:
        # Generar el código corto
        short_code = section.nombre[:4].upper()

        new_section = Section(
            name=section.nombre, cod=short_code, description=section.descripcion
        )
        db.add(new_section)
        db.commit()
        db.refresh(new_section)
        return section


# Actualizar una sección existente
@Seccion.put("/sections/{section_id}", response_model=SeccionUpdate)
async def update_section(section_id: int, section: SeccionUpdate):
    """update an existing section"""
    db = SessionLocal()
    db_section = db.query(Section).get(section_id)
    if db_section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    db_section.name = section.nombre if section.nombre else db_section.name
    db_section.cod = section.cod if section.cod else db_section.cod
    db_section.description = (
        section.descripcion if section.descripcion else db_section.description
    )
    db.commit()
    db.refresh(db_section)
    return SeccionUpdate(
        nombre=db_section.name, cod=db_section.cod, descripcion=db_section.description
    )


# Eliminar una sección
@Seccion.delete("/sections/{section_id}")
async def delete_section(section_id: int):
    """delete an existing section"""
    db = SessionLocal()
    section = db.query(Section).get(section_id)
    if section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    db.delete(section)
    db.commit()
    return {"message": "Section deleted"}
