from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class TipoRuta(str, Enum):
    VENTA = "venta"
    ENTREGA = "entrega"

# SCHEMAS PARA RUTA CLIENTE
class RutaClienteBase(BaseModel):
    cliente_id: int
    orden: int

class RutaClienteCreate(RutaClienteBase):
    pass

class RutaClienteResponse(RutaClienteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# SCHEMAS PARA RUTA ASIGNADA
class RutaAsignadaBase(BaseModel):
    usuario_id: int
    fecha: datetime

class RutaAsignadaCreate(RutaAsignadaBase):
    pass

class RutaAsignadaResponse(RutaAsignadaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# SCHEMAS PARA RUTA
class RutaBase(BaseModel):
    nombre: str
    tipo: TipoRuta

class RutaCreate(RutaBase):
    creada_por_id: int
    clientes: Optional[List[RutaClienteCreate]] = None

class RutaUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[TipoRuta] = None
    estado: Optional[bool] = None

class RutaResponse(RutaBase):
    id: int
    estado: bool
    creada_por_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    rutas_clientes: List[RutaClienteResponse] = []
    rutas_asignadas: List[RutaAsignadaResponse] = []
    
    class Config:
        from_attributes = True