from fastapi import FastAPI

app = FastAPI(title="Mi Primera API")

@app.get("/")
def hello_world():
    return {"message": "¡Mi primera API FastAPI!"}

@app.get("/info")
def info():
    return {"api": "FastAPI", "week": 1, "status": "running"}

@app.get("/greeting/{name}")
def greet_user(name: str):
    return {"greeting": f"¡Hola {name}!"}
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenido a mi API"}

@app.get("/info")
def info():
    return {"version": "1.0", "description": "API de prueba"}

# Endpoint personalizado
@app.get("/my-profile")
def my_profile():
    return {
        "name": "David-Baquero",           # Aquí pones tu nombre
        "bootcamp": "FastAPI",
        "week": 1,
        "date": "2025",
        "likes_fastapi": True      # Cambia a False si no te gustó
    }
