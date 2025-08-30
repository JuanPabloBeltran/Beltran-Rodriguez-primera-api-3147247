from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# ✅ Cargar variables de entorno desde .env
load_dotenv()

# ✅ URL de la base de datos, por defecto SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fastapi_app.db")

# ✅ Crear engine SQLAlchemy
# SQLite necesita check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# ✅ Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base para declarar modelos
Base = declarative_base()

# ✅ Dependencia de FastAPI para inyectar la sesión en rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
