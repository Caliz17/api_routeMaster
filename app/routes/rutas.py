from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.config.database import get_db
from app.schemas.ruta import RutaResponse, RutaCreate, RutaUpdate
from app.auth.dependencies import get_current_active_user, can_manage_products
from app.crud import ruta as ruta_crud
from app.models.user import User
from app.schemas.cliente import ClienteResponse


router = APIRouter(prefix="/rutas", tags=["Rutas"])

@router.get("/", response_model=List[RutaResponse])
def get_rutas(
    skip: int = 0,
    limit: int = 100,
    tipo: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener lista de rutas
    """
    if tipo:
        rutas = ruta_crud.get_rutas_by_tipo(db, tipo)
    else:
        rutas = ruta_crud.get_rutas(db, skip=skip, limit=limit)
    return rutas

@router.get("/activas", response_model=List[RutaResponse])
def get_rutas_activas(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener rutas activas
    """
    rutas = ruta_crud.get_rutas_activas(db)
    return rutas

@router.get("/{ruta_id}", response_model=RutaResponse)
def get_ruta(
    ruta_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener una ruta por ID
    """
    ruta = ruta_crud.get_ruta(db, ruta_id)
    if not ruta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruta no encontrada"
        )
    return ruta

@router.post("/", response_model=RutaResponse)
def create_ruta(
    ruta: RutaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Crear una nueva ruta
    """
    return ruta_crud.create_ruta(db, ruta)

@router.put("/{ruta_id}", response_model=RutaResponse)
def update_ruta(
    ruta_id: int,
    ruta_update: RutaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Actualizar una ruta
    """
    ruta = ruta_crud.update_ruta(db, ruta_id, ruta_update)
    if not ruta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruta no encontrada"
        )
    return ruta

@router.delete("/{ruta_id}")
def delete_ruta(
    ruta_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Eliminar una ruta (soft delete)
    """
    success = ruta_crud.delete_ruta(db, ruta_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ruta no encontrada"
        )
    return {"message": "Ruta eliminada correctamente"}

@router.post("/{ruta_id}/clientes/{cliente_id}")
def agregar_cliente_ruta(
    ruta_id: int,
    cliente_id: int,
    orden: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Agregar un cliente a una ruta
    """
    ruta_cliente = ruta_crud.add_cliente_a_ruta(db, ruta_id, cliente_id, orden)
    return {"message": "Cliente agregado a la ruta correctamente", "ruta_cliente_id": ruta_cliente.id}

@router.delete("/clientes/{ruta_cliente_id}")
def remover_cliente_ruta(
    ruta_cliente_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Remover un cliente de una ruta
    """
    success = ruta_crud.remove_cliente_de_ruta(db, ruta_cliente_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relación ruta-cliente no encontrada"
        )
    return {"message": "Cliente removido de la ruta correctamente"}

@router.post("/{ruta_id}/asignar/{usuario_id}")
def asignar_ruta_usuario(
    ruta_id: int,
    usuario_id: int,
    fecha: datetime = datetime.now(),
    db: Session = Depends(get_db),
    current_user: User = Depends(can_manage_products)  # Solo administradores
):
    """
    Asignar una ruta a un usuario (repartidor)
    """
    ruta_asignada = ruta_crud.asignar_ruta_usuario(db, ruta_id, usuario_id, fecha)
    return {"message": "Ruta asignada correctamente", "ruta_asignada_id": ruta_asignada.id}

@router.get("/{ruta_id}/optimizada")
def get_ruta_optimizada(
    ruta_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener ruta optimizada con coordenadas de clientes
    """
    ruta = ruta_crud.get_ruta(db, ruta_id)
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    
    # Obtener clientes con coordenadas
    clientes_con_coordenadas = []
    for ruta_cliente in ruta.rutas_clientes:
        cliente = ruta_cliente.cliente
        if cliente.latitud and cliente.longitud:
            clientes_con_coordenadas.append({
                "id": cliente.id,
                "nombre": cliente.nombre,
                "orden": ruta_cliente.orden,
                "latitud": float(cliente.latitud),
                "longitud": float(cliente.longitud),
                "direccion": cliente.direccion,
                "contacto": cliente.contacto
            })
    
    # Ordenar por orden de la ruta
    clientes_con_coordenadas.sort(key=lambda x: x["orden"])
    
    return {
        "ruta_id": ruta.id,
        "nombre": ruta.nombre,
        "tipo": ruta.tipo,
        "puntos": clientes_con_coordenadas
    }