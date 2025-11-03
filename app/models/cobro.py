from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum

class MetodoPago(str, enum.Enum):
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"
    TRANSFERENCIA = "transferencia"

class EstadoCobro(str, enum.Enum):
    COMPLETADO = "completado"
    PENDIENTE = "pendiente"
    ANULADO = "anulado"

class Cobro(Base):
    __tablename__ = "cobros"
    
    id = Column(Integer, primary_key=True, index=True)
    entrega_id = Column(Integer, ForeignKey("entregas.id"), nullable=False)
    fecha_cobro = Column(DateTime(timezone=True), server_default=func.now())
    monto = Column(DECIMAL(10, 2), nullable=False)
    metodo_pago = Column(Enum(MetodoPago), nullable=False)
    estado = Column(Enum(EstadoCobro), default=EstadoCobro.PENDIENTE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    entrega = relationship("Entrega", back_populates="cobro")