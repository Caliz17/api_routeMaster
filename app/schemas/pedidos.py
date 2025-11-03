from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal
from enum import Enum

class EstadoPedido(str, Enum):
    PENDIENTE_ENTREGA = "pendiente_entrega"
    ENTREGADO = "entregado"
    RECHAZADO = "rechazado"
    CANCELADO = "cancelado"

# SCHEMAS PARA DETALLE PEDIDO
class DetallePedidoBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: Decimal

class DetallePedidoCreate(DetallePedidoBase):
    pass

class DetallePedidoResponse(DetallePedidoBase):
    id: int
    subtotal: Decimal
    created_at: datetime
    
    class Config:
        from_attributes = True

# SCHEMAS PARA PEDIDO
class PedidoBase(BaseModel):
    cliente_id: int
    vendedor_id: int
    fecha_pedido: Optional[datetime] = None

class PedidoCreate(PedidoBase):
    detalles: List[DetallePedidoCreate]
    
    @validator('detalles')
    def validate_detalles(cls, v):
        if not v or len(v) == 0:
            raise ValueError('El pedido debe tener al menos un producto')
        return v

class PedidoUpdate(BaseModel):
    estado: Optional[EstadoPedido] = None

class PedidoResponse(PedidoBase):
    id: int
    total: Decimal
    estado: EstadoPedido
    created_at: datetime
    updated_at: Optional[datetime] = None
    detalles: List[DetallePedidoResponse] = []
    
    class Config:
        from_attributes = True