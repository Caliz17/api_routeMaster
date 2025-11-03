from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.dashboard import (
    DashboardResponse, ResumenGeneral, MetricasVentas, 
    ProductoPopular, PedidoPendiente, RutaActiva, EstadisticasVentasMensuales
)
from app.auth.dependencies import get_current_active_user
from app.crud import dashboard as dashboard_crud
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener dashboard completo con todas las métricas
    """
    try:
        # Obtener todos los datos del dashboard
        resumen_general = dashboard_crud.get_resumen_general(db)
        metricas_ventas = dashboard_crud.get_metricas_ventas(db)
        productos_populares = dashboard_crud.get_productos_populares(db)
        pedidos_pendientes = dashboard_crud.get_pedidos_pendientes(db)
        rutas_activas = dashboard_crud.get_rutas_activas(db)
        ventas_mensuales = dashboard_crud.get_ventas_mensuales(db)
        
        return DashboardResponse(
            resumen_general=ResumenGeneral(**resumen_general),
            metricas_ventas=MetricasVentas(**metricas_ventas),
            productos_populares=productos_populares,
            pedidos_pendientes=pedidos_pendientes,
            rutas_activas=rutas_activas,
            ventas_mensuales=ventas_mensuales
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar dashboard: {str(e)}"
        )

@router.get("/resumen", response_model=ResumenGeneral)
def get_resumen(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener solo el resumen general
    """
    resumen = dashboard_crud.get_resumen_general(db)
    return ResumenGeneral(**resumen)

@router.get("/metricas-ventas", response_model=MetricasVentas)
def get_metricas_ventas(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener métricas de ventas
    """
    metricas = dashboard_crud.get_metricas_ventas(db)
    return MetricasVentas(**metricas)

@router.get("/productos-populares", response_model=List[ProductoPopular])
def get_productos_populares(
    limit: int = Query(5, description="Número de productos a mostrar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener productos más populares
    """
    return dashboard_crud.get_productos_populares(db, limit)

@router.get("/pedidos-pendientes", response_model=List[PedidoPendiente])
def get_pedidos_pendientes(
    limit: int = Query(5, description="Número de pedidos a mostrar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener pedidos pendientes de entrega
    """
    return dashboard_crud.get_pedidos_pendientes(db, limit)

@router.get("/rutas-activas", response_model=List[RutaActiva])
def get_rutas_activas(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener rutas activas
    """
    return dashboard_crud.get_rutas_activas(db)

@router.get("/ventas-mensuales", response_model=List[EstadisticasVentasMensuales])
def get_ventas_mensuales(
    meses: int = Query(6, description="Número de meses a mostrar"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener estadísticas de ventas mensuales
    """
    return dashboard_crud.get_ventas_mensuales(db, meses)