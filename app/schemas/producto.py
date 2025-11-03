from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ProductoBase(BaseModel):
    nombre: str
    sku: str
    descripcion: Optional[str] = None
    precio: Decimal
    stock: int

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    sku: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = None
    stock: Optional[int] = None
    estado: Optional[bool] = None

class ProductoResponse(ProductoBase):
    id: int
    estado: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True