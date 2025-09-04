# main.py (VERSIÓN COMPLETA con Roles + Logs + Debug endpoint + Posts + get_current_admin)
import logging
from fastapi import FastAPI, HTTPException, Query, Depends, status
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship, joinedload
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# ------------------------------
# LOGGING
# ------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------
# APP
# ------------------------------
app = FastAPI(
    title="Mi Biblioteca + API FastAPI",
    description="API combinada: Biblioteca Personal + Productos + Usuarios con BD + Categorías + Autenticación + Roles + Posts",
    version="2.1.1"
)

# ------------------------------
# BD SQLite
# ------------------------------
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ------------------------------
# MODELOS
# ------------------------------
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True)
    phone = Column(String(15), nullable=True)

class CategoriaDB(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, index=True)
    descripcion = Column(String(250))
    productos = relationship("ProductoDB", back_populates="categoria")

class ProductoDB(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    descripcion = Column(String(250), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    categoria = relationship("CategoriaDB", back_populates="productos")

# Modelo SQLAlchemy para autenticación (ahora con campo role)
class AuthUserDB(Base):
    __tablename__ = "auth_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user", nullable=False)  # <-- campo role

Base.metadata.create_all(bind=engine)

# ------------------------------
# DEPENDENCIA DB
# ------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------
# SCHEMAS
# ------------------------------
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: Optional[int] = Field(None, ge=0, le=120)
    phone: Optional[str] = Field(None, pattern=r"^\+?\d{7,15}$")

class UserCreate(UserBase): pass
class User(UserBase):
    id: int
    class Config: from_attributes = True

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str

class CategoriaCreate(CategoriaBase): pass
class Categoria(CategoriaBase):
    id: int
    class Config: from_attributes = True

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    descripcion: str
    categoria_id: Optional[int] = None

class ProductoCreate(ProductoBase): pass
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None

class ProductoResponse(ProductoBase):
    id: int
    categoria: Optional[Categoria] = None
    class Config: from_attributes = True

# ------------------------------
# CRUD Categorías
# ------------------------------
def crear_categoria(db: Session, categoria: CategoriaCreate):
    db_categoria = CategoriaDB(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    logger.info(f"Categoría creada: {db_categoria.nombre}")
    return db_categoria

def obtener_categoria(db: Session, categoria_id: int):
    return db.query(CategoriaDB).filter(CategoriaDB.id == categoria_id).first()

def obtener_categorias(db: Session):
    return db.query(CategoriaDB).all()

def obtener_categoria_con_productos(db: Session, categoria_id: int):
    return db.query(CategoriaDB).options(joinedload(CategoriaDB.productos)).filter(CategoriaDB.id == categoria_id).first()

# ------------------------------
# CRUD Productos
# ------------------------------
def crear_producto(db: Session, producto: ProductoCreate):
    if producto.categoria_id:
        cat = obtener_categoria(db, producto.categoria_id)
        if not cat:
            raise HTTPException(status_code=400, detail="Categoría no existe")
    db_producto = ProductoDB(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    logger.info(f"Producto creado: {db_producto.nombre}")
    return db_producto

def obtener_producto(db: Session, producto_id: int):
    return db.query(ProductoDB).options(joinedload(ProductoDB.categoria)).filter(ProductoDB.id == producto_id).first()

def obtener_productos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ProductoDB).options(joinedload(ProductoDB.categoria)).offset(skip).limit(limit).all()

def actualizar_producto(db: Session, producto_id: int, producto: ProductoUpdate):
    db_producto = obtener_producto(db, producto_id)
    if db_producto:
        if producto.categoria_id:
            cat = obtener_categoria(db, producto.categoria_id)
            if not cat:
                raise HTTPException(status_code=400, detail="Categoría no existe")
        for key, value in producto.dict(exclude_unset=True).items():
            setattr(db_producto, key, value)
        db.commit()
        db.refresh(db_producto)
        logger.info(f"Producto actualizado: {db_producto.nombre}")
    return db_producto

def eliminar_producto(db: Session, producto_id: int):
    db_producto = obtener_producto(db, producto_id)
    if db_producto:
        logger.warning(f"Producto eliminado: {db_producto.nombre}")
        db.delete(db_producto)
        db.commit()
    return db_producto

def contar_productos(db: Session):
    return db.query(ProductoDB).count()

# ------------------------------
# AUTH: Hashing + JWT
# ------------------------------
SECRET_KEY = "cambia-esta-clave-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

# ------------------------------
# DEPENDENCIAS: USUARIO / ADMIN
# ------------------------------
def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    username = verify_token(token.credentials)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.query(AuthUserDB).filter(AuthUserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return {"id": user.id, "username": user.username, "role": user.role}

def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return current_user

# ------------------------------
# DEBUG endpoint (opcional)
# ------------------------------
@app.get("/debug/verify-token")
def verify_token_debug(token: str = Depends(security)):
    """Solo para debugging - NO usar en producción"""
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Token verificado: {payload}")
        return {
            "valid": True,
            "payload": payload,
            "username": payload.get("sub"),
            "expires": payload.get("exp")
        }
    except JWTError as e:
        logger.error(f"Error verificando token: {str(e)}")
        return {
            "valid": False,
            "error": str(e)
        }

# ------------------------------
# Endpoints Auth
# ------------------------------
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str
    username: str

@app.post("/login", response_model=TokenOut)
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Intento de login para usuario: {data.username}")
    user = db.query(AuthUserDB).filter(AuthUserDB.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        logger.warning(f"Login fallido para usuario: {data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(username=user.username)
    logger.info(f"Login exitoso para usuario: {data.username}")
    return {"access_token": token, "token_type": "bearer", "username": user.username}

# ------------------------------
# POSTS (Ejercicio Semana 5)
# ------------------------------
class Post(BaseModel):
    title: str
    content: str

posts = []  # lista en memoria

@app.post("/posts")
def create_post(post: Post, current_user: dict = Depends(get_current_user)):
    new_post = {
        "id": len(posts) + 1,
        "title": post.title,
        "content": post.content,
        "author": current_user["username"]
    }
    posts.append(new_post)
    logger.info(f"Post creado por {current_user['username']}: {post.title}")
    return new_post

@app.get("/posts/my")
def get_my_posts(current_user: dict = Depends(get_current_user)):
    user_posts = [p for p in posts if p["author"] == current_user["username"]]
    return user_posts

@app.get("/posts/all")
def get_all_posts(current_admin: dict = Depends(get_current_admin)):
    """Solo admin puede ver todos los posts"""
    return posts

# ------------------------------
# SERVIDOR
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
