from sqlalchemy import Column, Integer, String, Float
from database import Base

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    precio = Column(Float, nullable=False)
    descripcion = Column(String, nullable=False)
