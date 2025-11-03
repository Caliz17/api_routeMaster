from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, date
from decimal import Decimal

class ResumenGeneral(BaseModel):
    total_clientes: int
    total_productos: int
    total_pedidos: int
    total_ventas: Decimal
    pedidos_pendientes: int
    rutas_activas: int

class MetricasVentas(BaseModel):
    ventas_hoy: Decimal
    ventas_semana: Decimal
    ventas_mes: Decimal
    crecimiento_mensual: Decimal

class ProductoPopular(BaseModel):
    id: int
    nombre: str
    sku: str
    cantidad_vendida: int
    total_ventas: Decimal

class PedidoPendiente(BaseModel):
    id: int
    cliente_nombre: str
    total: Decimal
    fecha_pedido: datetime
    estado: str

class RutaActiva(BaseModel):
    id: int
    nombre: str
    tipo: str
    total_clientes: int
    repartidor: Optional[str] = None

class EstadisticasVentasMensuales(BaseModel):
    mes: str
    total_ventas: Decimal
    cantidad_pedidos: int

class DashboardResponse(BaseModel):
    resumen_general: ResumenGeneral
    metricas_ventas: MetricasVentas
    productos_populares: List[ProductoPopular]
    pedidos_pendientes: List[PedidoPendiente]
    rutas_activas: List[RutaActiva]
    ventas_mensuales: List[EstadisticasVentasMensuales]