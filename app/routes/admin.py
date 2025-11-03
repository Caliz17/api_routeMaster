from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.user import UserResponse, UserRoleUpdate
from app.auth.dependencies import can_manage_users
from app.crud import user as user_crud
from app.crud.role import get_roles, get_role
from app.schemas.role import RoleResponse
from typing import Optional, List


router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", response_model=List[UserResponse])
def admin_get_users(
    skip: int = 0, 
    limit: int = 100,
    token: Optional[str] = None,  # ✅ AGREGAR ESTO TEMPORALMENTE
    db: Session = Depends(get_db),
    current_user = Depends(can_manage_users)
):
    """
    Obtener todos los usuarios (solo con permiso users.manage)
    """
    # El parámetro token se ignora completamente
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users-with-permissions")
def admin_get_users_with_permissions(
    db: Session = Depends(get_db),
    current_user = Depends(can_manage_users) 
):
    """
    Obtener usuarios con información de permisos (solo con permiso users.manage)
    """
    users = user_crud.get_users(db)
    result = []
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role.name,
            "permissions": [perm.name for perm in user.role.permissions]
        }
        result.append(user_data)
    
    return result

@router.get("/roles", response_model=list[RoleResponse])
def admin_get_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(can_manage_users)  
):
    """
    Obtener lista de roles disponibles
    """
    roles = get_roles(db, skip=skip, limit=limit)
    return roles

@router.put("/users/{user_id}/role", response_model=UserResponse)
def admin_update_user_role(
    user_id: int,
    role_update: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(can_manage_users)
):
    """
    Actualizar el rol de un usuario
    """
    # Verificar que el usuario a modificar exista
    existing_user = user_crud.get_user(db, user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Verificar que el rol exista
    new_role = get_role(db, role_update.role_id)
    if not new_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol no encontrado"
        )
    
    # No permitir que un usuario se cambie su propio rol
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes cambiar tu propio rol"
        )
    
    # Actualizar el rol
    updated_user = user_crud.update_user_role(db, user_id, role_update.role_id)
    
    return updated_user

# Si necesitas la función get_current_active_user en main.py, agrega esto:
def get_current_active_user():
    """Función auxiliar para main.py"""
    from app.auth.dependencies import get_current_active_user as original
    return original