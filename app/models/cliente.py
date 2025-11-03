from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    nit = Column(String(20), unique=True, index=True)
    direccion = Column(Text)
    telefono = Column(String(20))
    contacto = Column(String(255))
    estado = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    rutas_clientes = relationship("RutaCliente", back_populates="cliente")
    pedidos = relationship("Pedido", back_populates="cliente")