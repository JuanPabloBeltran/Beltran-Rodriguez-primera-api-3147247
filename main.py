from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship, joinedload

# ------------------------------
# APP
# ------------------------------
app = FastAPI(
    title="Mi Biblioteca + API FastAPI",
    description="API combinada: Biblioteca Personal + Productos + Usuarios con BD + Categorías",
    version="2.0.0"
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
    return db_producto

def eliminar_producto(db: Session, producto_id: int):
    db_producto = obtener_producto(db, producto_id)
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto

def contar_productos(db: Session):
    return db.query(ProductoDB).count()

# ------------------------------
# ENDPOINTS Usuarios
# ------------------------------
@app.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users", response_model=List[User])
def list_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()

# ------------------------------
# ENDPOINTS Categorías
# ------------------------------
@app.post("/categorias/", response_model=Categoria)
def crear_categoria_endpoint(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    return crear_categoria(db, categoria)

@app.get("/categorias/", response_model=List[Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    return obtener_categorias(db)

@app.get("/categorias/{categoria_id}", response_model=Categoria)
def obtener_categoria_endpoint(categoria_id: int, db: Session = Depends(get_db)):
    cat = obtener_categoria_con_productos(db, categoria_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return cat

# ------------------------------
# ENDPOINTS Productos
# ------------------------------
@app.post("/productos/", response_model=ProductoResponse)
def crear_producto_endpoint(producto: ProductoCreate, db: Session = Depends(get_db)):
    return crear_producto(db, producto)

@app.get("/productos/", response_model=List[ProductoResponse])
def listar_productos_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return obtener_productos(db, skip=skip, limit=limit)

@app.get("/productos/{producto_id}", response_model=ProductoResponse)
def obtener_producto_endpoint(producto_id: int, db: Session = Depends(get_db)):
    prod = obtener_producto(db, producto_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod

@app.patch("/productos/{producto_id}", response_model=ProductoResponse)
def actualizar_producto_endpoint(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    prod = actualizar_producto(db, producto_id, producto)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod

@app.delete("/productos/{producto_id}")
def eliminar_producto_endpoint(producto_id: int, db: Session = Depends(get_db)):
    prod = eliminar_producto(db, producto_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": f"Producto {producto_id} eliminado correctamente"}

@app.get("/productos/buscar/")
def buscar_productos_endpoint(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    productos = db.query(ProductoDB).options(joinedload(ProductoDB.categoria)).filter(
        or_(ProductoDB.nombre.contains(q), ProductoDB.descripcion.contains(q))
    ).all()
    return {"busqueda": q, "productos": productos, "total": len(productos)}

@app.get("/productos/stats/")
def estadisticas_productos_endpoint(db: Session = Depends(get_db)):
    productos = db.query(ProductoDB).all()
    if not productos:
        return {"total": 0, "precio_promedio": 0, "precio_max": 0, "precio_min": 0}
    precios = [p.precio for p in productos]
    return {
        "total": len(productos),
        "precio_promedio": sum(precios)/len(precios),
        "precio_max": max(precios),
        "precio_min": min(precios)
    }

# ------------------------------
# SERVIDOR
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
