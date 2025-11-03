from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.config.database import get_db
from app.schemas.producto import ProductoResponse, ProductoCreate, ProductoUpdate
from app.auth.dependencies import get_current_active_user, can_manage_products
from app.crud import producto as producto_crud
from app.models.user import User

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("/", response_model=List[ProductoResponse])
def get_productos(
    skip: int = 0,
    limit: int = 100,
    token: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener lista de productos
    """
    productos = producto_crud.get_productos(db, skip=skip, limit=limit)
    return productos

@router.get("/{producto_id}", response_model=ProductoResponse)
def get_producto(
    producto_id: int,
    token: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener un producto por ID
    """
    producto = producto_crud.get_producto(db, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return producto

@router.post("/", response_model=ProductoResponse)
def create_producto(
    producto: ProductoCreate,
    token: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Crear un nuevo producto
    """
    # Verificar si el SKU ya existe
    existing_producto = producto_crud.get_producto_by_sku(db, producto.sku)
    if existing_producto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un producto con este SKU"
        )
    
    return producto_crud.create_producto(db, producto)

@router.put("/{producto_id}", response_model=ProductoResponse)
def update_producto(
    producto_id: int,
    producto_update: ProductoUpdate,
    token: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Actualizar un producto
    """
    producto = producto_crud.update_producto(db, producto_id, producto_update)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return producto

@router.delete("/{producto_id}")
def delete_producto(
    producto_id: int,
    token: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Eliminar un producto (soft delete)
    """
    success = producto_crud.delete_producto(db, producto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return {"message": "Producto eliminado correctamente"}