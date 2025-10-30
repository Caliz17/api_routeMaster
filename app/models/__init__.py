from .user import User
from .role import Role

# Esto asegura que SQLAlchemy conozca todos los modelos
__all__ = ["User", "Role"]