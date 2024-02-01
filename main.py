"""
Este modulo es principal"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.r_seccion import Seccion
from backend.routes.r_family import Familia
from backend.routes.r_articulo import articulo_router
from backend.config.db import Base, engine


# Función para crear las tablas
def create_tables():
    """create tables"""
    Base.metadata.create_all(bind=engine)


app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)


create_tables()

app.include_router(Seccion)
app.include_router(Familia)
app.include_router(articulo_router)
