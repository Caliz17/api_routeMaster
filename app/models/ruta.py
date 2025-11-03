from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum

class TipoRuta(str, enum.Enum):
    VENTA = "venta"
    ENTREGA = "entrega"

class Ruta(Base):
    __tablename__ = "rutas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoRuta), nullable=False)
    estado = Column(Boolean, default=True)
    creada_por_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    creada_por = relationship("User", back_populates="rutas_creadas")
    rutas_clientes = relationship("RutaCliente", back_populates="ruta")
    rutas_asignadas = relationship("RutaAsignada", back_populates="ruta")