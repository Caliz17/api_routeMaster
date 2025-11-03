from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, Date, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum

class EstadoEntrega(str, enum.Enum):
    PENDIENTE = "pendiente"
    ENTREGADO = "entregado"
    RECHAZADO = "rechazado"

class Entrega(Base):
    __tablename__ = "entregas"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    repartidor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fecha_entrega = Column(Date, nullable=False)
    estado = Column(Enum(EstadoEntrega), default=EstadoEntrega.PENDIENTE)
    observacion = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    pedido = relationship("Pedido", back_populates="entrega")
    repartidor = relationship("User", back_populates="entregas")
    cobro = relationship("Cobro", back_populates="entrega", uselist=False)