from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.auth.dependencies import get_current_active_user
from app.crud.user import get_users, get_user, update_user, delete_user, get_user_by_email, get_user_by_username
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Obtener información del usuario actual
    """
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Actualizar información del usuario actual
    """
    # Verificar si el username ya existe (si se está actualizando)
    if user_update.username and user_update.username != current_user.username:
        if get_user_by_username(db, user_update.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya está en uso"
            )
    
    # Verificar si el email ya existe (si se está actualizando)
    if user_update.email and user_update.email != current_user.email:
        if get_user_by_email(db, user_update.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
    
    updated_user = update_user(db, current_user.id, user_update)
    return updated_user

@router.delete("/me")
def delete_user_me(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Eliminar el usuario actual (soft delete)
    """
    delete_user(db, current_user.id)
    return {"message": "Usuario eliminado correctamente"}

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obtener información de un usuario específico por ID
    """
    user = get_user(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user

@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de usuarios
    """
    users = get_users(db, skip=skip, limit=limit)
    return users