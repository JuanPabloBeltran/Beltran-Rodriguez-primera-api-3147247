# Modelos optimizados para catálogo de elementos (Tipo D)
from sqlalchemy import Column, Integer, String, Numeric, Index, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ElementoCatalogo(Base):
    __tablename__ = "elementos_catalogo"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    precio = Column(Numeric)
    stock = Column(Integer)
    activo = Column(Integer, default=1)
    creado = Column(DateTime, server_default=func.now())
    __table_args__ = (
        Index('idx_nombre', 'nombre'),
        Index('idx_precio', 'precio'),
        Index('idx_stock', 'stock'),
    )

class InventarioElemento(Base):
    __tablename__ = "inventario_elementos"
    id = Column(Integer, primary_key=True)
    elemento_id = Column(Integer, index=True)
    cantidad = Column(Integer)
    actualizado = Column(DateTime, server_default=func.now(), onupdate=func.now())
    __table_args__ = (
        Index('idx_elemento_id', 'elemento_id'),
        Index('idx_cantidad', 'cantidad'),
    )

class TransaccionInventario(Base):
    __tablename__ = "transacciones_inventario"
    id = Column(Integer, primary_key=True)
    elemento_id = Column(Integer, index=True)
    tipo = Column(String)  # entrada/salida
    cantidad = Column(Integer)
    fecha = Column(DateTime, server_default=func.now())
    __table_args__ = (
        Index('idx_elemento_id_trans', 'elemento_id'),
        Index('idx_tipo', 'tipo'),
    )
