from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from app.config.database import Base

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text)
    module = Column(String(50))  # Ej: "users", "products", "orders"
    action = Column(String(50))  # Ej: "create", "read", "update", "delete"
    is_active = Column(Boolean, default=True)
    
    # Relación con roles (la otra parte de la relación muchos-a-muchos)
    roles = relationship("Role", secondary="role_permission", back_populates="permissions")