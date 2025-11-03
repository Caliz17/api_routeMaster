from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.auth.utils import get_current_user
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

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

async def get_current_active_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependencia para obtener el usuario actual activo
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_current_user(credentials.credentials, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo"
        )
    
    return user

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

async def check_permission(permission_name: str, current_user: User = Depends(get_current_active_user)):
    """
    Dependencia para verificar si el usuario tiene un permiso específico
    """
    # Verificar si el usuario tiene el permiso en su rol
    has_permission = any(
        permission.name == permission_name 
        for permission in current_user.role.permissions
    )
    
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tienes el permiso: {permission_name}"
        )
    
    return current_user

# ✅ PERMISOS PREDEFINIDOS PARA USO COMÚN
async def can_manage_users(current_user: User = Depends(get_current_active_user)):
    """Verificar permiso para gestionar usuarios"""
    return await check_permission("users.manage", current_user)

async def can_view_reports(current_user: User = Depends(get_current_active_user)):
    """Verificar permiso para ver reportes"""
    return await check_permission("reports.view", current_user)

def can_manage_products(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Verificar si el usuario puede gestionar productos"""
    # Cargar el rol y permisos del usuario
    user_with_permissions = db.query(User).join(User.role).filter(User.id == current_user.id).first()
    
    if not user_with_permissions or not user_with_permissions.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para gestionar productos"
        )
    
    # Verificar si tiene el permiso products.manage
    user_permissions = [perm.name for perm in user_with_permissions.role.permissions]
    
    if "products.manage" not in user_permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes el permiso: products.manage"
        )
    
    return current_user

async def can_manage_orders(current_user: User = Depends(get_current_active_user)):
    """Verificar permiso para gestionar pedidos"""
    return await check_permission("orders.manage", current_user)