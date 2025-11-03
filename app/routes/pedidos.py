from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.schemas.pedidos import PedidoResponse, PedidoCreate, PedidoUpdate
from app.auth.dependencies import get_current_active_user, can_manage_orders
from app.crud import pedido as pedido_crud
from app.models.user import User

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.get("/", response_model=List[PedidoResponse])
def get_pedidos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener lista de pedidos
    """
    pedidos = pedido_crud.get_pedidos(db, skip=skip, limit=limit)
    return pedidos

@router.get("/{pedido_id}", response_model=PedidoResponse)
def get_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener un pedido por ID
    """
    pedido = pedido_crud.get_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )
    return pedido

@router.get("/cliente/{cliente_id}", response_model=List[PedidoResponse])
def get_pedidos_by_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener pedidos por cliente
    """
    pedidos = pedido_crud.get_pedidos_by_cliente(db, cliente_id)
    return pedidos

@router.post("/", response_model=PedidoResponse)
def create_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # Vendedores pueden crear pedidos
):
    """
    Crear un nuevo pedido
    """
    try:
        return pedido_crud.create_pedido(db, pedido)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{pedido_id}", response_model=PedidoResponse)
def update_pedido(
    pedido_id: int,
    pedido_update: PedidoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_orders)  # Solo administradores pueden cambiar estado
):
    """
    Actualizar estado de un pedido
    """
    pedido = pedido_crud.update_pedido_estado(db, pedido_id, pedido_update)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )
    return pedido

@router.delete("/{pedido_id}")
def delete_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_orders)  # Solo administradores
):
    """
    Eliminar un pedido
    """
    success = pedido_crud.delete_pedido(db, pedido_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado"
        )
    return {"message": "Pedido eliminado correctamente"}