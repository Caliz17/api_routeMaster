from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum

class EstadoAsignacion(str, enum.Enum):
    PROGRAMADA = "programada"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"

class RutaAsignada(Base):
    __tablename__ = "rutas_asignadas"
    
    id = Column(Integer, primary_key=True, index=True)
    ruta_id = Column(Integer, ForeignKey("rutas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    estado = Column(Enum(EstadoAsignacion), default=EstadoAsignacion.PROGRAMADA)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    ruta = relationship("Ruta", back_populates="rutas_asignadas")
    usuario = relationship("User", back_populates="rutas_asignadas")