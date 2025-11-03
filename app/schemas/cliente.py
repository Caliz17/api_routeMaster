from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ClienteBase(BaseModel):
    nombre: str
    nit: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    contacto: Optional[str] = None
    # ✅ NUEVOS CAMPOS
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion_geocodificada: Optional[str] = None

    @validator('latitud')
    def validate_latitud(cls, v):
        if v is not None and (v < -90 or v > 90):
            raise ValueError('La latitud debe estar entre -90 y 90')
        return v

    @validator('longitud')
    def validate_longitud(cls, v):
        if v is not None and (v < -180 or v > 180):
            raise ValueError('La longitud debe estar entre -180 y 180')
        return v

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    nit: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    contacto: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    direccion_geocodificada: Optional[str] = None
    estado: Optional[bool] = None

class ClienteResponse(ClienteBase):
    id: int
    estado: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True