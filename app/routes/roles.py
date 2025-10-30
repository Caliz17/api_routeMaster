from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.role import RoleResponse, RoleCreate
from app.auth.dependencies import get_admin_user
from app.crud import role as role_crud

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=List[RoleResponse])
def read_roles(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """
    Obtener lista de roles (solo admin)
    """
    return role_crud.get_roles(db, skip=skip, limit=limit)

@router.post("/", response_model=RoleResponse)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    """
    Crear nuevo rol (solo admin)
    """
    existing_role = role_crud.get_role_by_name(db, role.name)
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El rol ya existe"
        )
    
    return role_crud.create_role(db, role)