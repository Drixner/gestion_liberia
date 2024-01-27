"""
Este modulo es principal"""
from fastapi import FastAPI
from backend.routes.r_seccion import Seccion

app = FastAPI()

app.include_router(Seccion)
app.include_router(Familia)
