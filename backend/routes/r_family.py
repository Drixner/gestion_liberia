""" Rutas para el CRUD de familias """

from fastapi import APIRouter, HTTPException, status, Response
from ..models.m_family import Family
from ..models.m_seccion import Section
from ..config.db import SessionLocal
from ..schemas.sch_family import FamiliaCreate, FamiliaUpdate, FamiliaResponse

Familia = APIRouter()


# Obtener todas las familias
@Familia.get("/families")
async def get_families():
    """get all families"""
    db = SessionLocal()
    families = db.query(Family).all()
    return {"families": families}


# Función para generar el código de la familia a partir del nombre
def generate_family_code_from_name(name: str) -> str:
    """generate family code from name"""
    # Asegúrate de que el nombre sea lo suficientemente largo
    if len(name) < 4:
        raise ValueError("El nombre de la familia debe tener al menos 4 letras")
    return name[:4].upper()


# Crear una nueva familia
@Familia.post("/families", response_model=FamiliaResponse)
async def create_family(family: FamiliaCreate):
    """create a new family"""
    if not family.section_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de la sección es obligatorio.",
        )

    family_code = generate_family_code_from_name(family.name)

    db = SessionLocal()
    try:
        seccion = db.query(Section).filter(Section.name == family.section_name).first()
        if not seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La sección con el nombre {family.section_name} no existe.",
            )

        if db.query(Family).filter(Family.cod == family_code).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código de la familia generado ya existe.",
            )

        new_family = Family(name=family.name, cod=family_code, section_id=seccion.id)
        db.add(new_family)
        db.commit()
        db.refresh(new_family)

        # Devolver el objeto con la información actualizada, incluido el section_name
        return FamiliaResponse(
            id=new_family.id,
            cod=new_family.cod,
            name=new_family.name,
            section_name=seccion.name,  # Aquí asignamos el nombre de la sección del objeto sección
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
    finally:
        db.close()


# Actualizar una familia existente
@Familia.put(
    "/families/by-name/{family_name}", response_model=FamiliaResponse
)  # Actualización por nombre
async def update_family_by_name(family_name: str, family_update: FamiliaUpdate):
    """update an existing family by name"""
    db = SessionLocal()
    try:
        # Buscar la familia existente por nombre
        existing_family = db.query(Family).filter(Family.name == family_name).first()
        if not existing_family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La familia con el nombre {family_name} no existe.",
            )

        # Actualizar la familia basándose en los datos proporcionados
        if family_update.name:
            existing_family.name = family_update.name
            existing_family.cod = generate_family_code_from_name(family_update.name)

        if family_update.section_name:
            seccion = (
                db.query(Section)
                .filter(Section.name == family_update.section_name)
                .first()
            )
            if not seccion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"La sección con el nombre {family_update.section_name} no existe.",
                )
            existing_family.section_id = seccion.id

        db.commit()
        db.refresh(existing_family)

        return FamiliaResponse(
            id=existing_family.id,
            cod=existing_family.cod,
            name=existing_family.name,
            section_name=(
                seccion.name
                if family_update.section_name
                else existing_family.section.name
            ),
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
    finally:
        db.close()


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


# Eliminar una familia por nombre
@Familia.delete(
    "/families/by-name/{family_name}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_family_by_name(family_name: str):
    """delete an existing family by name"""
    db = SessionLocal()
    try:
        # Buscar la familia existente por nombre
        existing_family = db.query(Family).filter(Family.name == family_name).first()
        if not existing_family:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La familia con el nombre '{family_name}' no existe.",
            )

        # Eliminar la familia encontrada
        db.delete(existing_family)
        db.commit()

        # Retornar una respuesta vacía
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
    finally:
        db.close()
