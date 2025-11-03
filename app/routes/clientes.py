from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.schemas.cliente import ClienteResponse, ClienteCreate, ClienteUpdate
from app.auth.dependencies import get_current_active_user, can_manage_products
from app.crud import cliente as cliente_crud
from app.models.user import User

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=List[ClienteResponse])
def get_clientes(
    skip: int = 0,
    limit: int = 100,
    token: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener lista de clientes
    """
    clientes = cliente_crud.get_clientes(db, skip=skip, limit=limit)
    return clientes

@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(
    cliente_id: int,
    token: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener un cliente por ID
    """
    cliente = cliente_crud.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    return cliente

@router.post("/", response_model=ClienteResponse)
def create_cliente(
    cliente: ClienteCreate,
    token: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Crear un nuevo cliente
    """
    # Verificar si el NIT ya existe
    existing_cliente = cliente_crud.get_cliente_by_nit(db, cliente.nit)
    if existing_cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente con este NIT"
        )
    
    return cliente_crud.create_cliente(db, cliente)

@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    token: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Actualizar un cliente
    """
    cliente = cliente_crud.update_cliente(db, cliente_id, cliente_update)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    return cliente

@router.delete("/{cliente_id}")
def delete_cliente(
    cliente_id: int,
    token: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Eliminar un cliente (soft delete)
    """
    success = cliente_crud.delete_cliente(db, cliente_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )
    return {"message": "Cliente eliminado correctamente"}