from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.auth.utils import get_current_user
from app.models.user import User
from app.models.role import Role

security = HTTPBearer()

async def get_current_active_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependencia para obtener el usuario actual activo
    """
    user = get_current_user(credentials.credentials, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo"
        )
    
    return user

async def get_admin_user(current_user: User = Depends(get_current_active_user)):
    """
    Dependencia para verificar que el usuario es admin
    """
    if not any(role.name == "administrador" for role in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    return current_user

async def get_gerente_user(current_user: User = Depends(get_current_active_user)):
    """
    Dependencia para verificar que el usuario es gerente
    """
    if not any(role.name == "gerente" for role in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de gerente"
        )
    return current_user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user

def require_admin_role(current_user: User = Depends(get_current_active_user)):
    if not current_user.role or current_user.role.name != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador"
        )
    return current_user

def require_manager_role(current_user: User = Depends(get_current_active_user)):
    if not current_user.role or current_user.role.name != "gerente":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de gerente"
        )
    return current_user