from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum

class EstadoPedido(str, enum.Enum):
    PENDIENTE_ENTREGA = "pendiente_entrega"
    ENTREGADO = "entregado"
    RECHAZADO = "rechazado"
    CANCELADO = "cancelado"

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    vendedor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fecha_pedido = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(DECIMAL(10, 2), nullable=False)
    estado = Column(Enum(EstadoPedido), default=EstadoPedido.PENDIENTE_ENTREGA)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    cliente = relationship("Cliente", back_populates="pedidos")
    vendedor = relationship("User", back_populates="pedidos")
    detalle_pedidos = relationship("DetallePedido", back_populates="pedido")
    entrega = relationship("Entrega", back_populates="pedido", uselist=False)