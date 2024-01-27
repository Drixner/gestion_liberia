"""
Este modulo es principal"""
from fastapi import FastAPI
from backend.routes.r_seccion import Seccion
from backend.routes.r_family import Familia

app = FastAPI()

app.include_router(Seccion)
app.include_router(Familia)
