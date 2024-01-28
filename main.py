"""
Este modulo es principal"""
from fastapi import FastAPI
from backend.routes.r_seccion import Seccion
from backend.routes.r_family import Familia
from backend.config.db import Base, engine


# Función para crear las tablas
def create_tables():
    """create tables"""
    Base.metadata.create_all(bind=engine)


app = FastAPI()

create_tables()

app.include_router(Seccion)
app.include_router(Familia)
