from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_, cast, Date
from datetime import datetime, timedelta, date
from decimal import Decimal
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.models.pedido import Pedido, EstadoPedido
from app.models.detalle_pedido import DetallePedido
from app.models.ruta import Ruta
from app.models.ruta_asignada import RutaAsignada
from app.models.user import User

def get_resumen_general(db: Session):
    """Obtener resumen general del sistema"""
    total_clientes = db.query(Cliente).filter(Cliente.estado == True).count()
    total_productos = db.query(Producto).filter(Producto.estado == True).count()
    total_pedidos = db.query(Pedido).count()
    
    # Total de ventas (suma de todos los pedidos)
    total_ventas_result = db.query(func.sum(Pedido.total)).scalar()
    total_ventas = total_ventas_result if total_ventas_result else Decimal('0.00')
    
    # Pedidos pendientes de entrega
    pedidos_pendientes = db.query(Pedido).filter(
        Pedido.estado == EstadoPedido.PENDIENTE_ENTREGA
    ).count()
    
    # Rutas activas
    rutas_activas = db.query(Ruta).filter(Ruta.estado == True).count()
    
    return {
        "total_clientes": total_clientes,
        "total_productos": total_productos,
        "total_pedidos": total_pedidos,
        "total_ventas": total_ventas,
        "pedidos_pendientes": pedidos_pendientes,
        "rutas_activas": rutas_activas
    }

def get_metricas_ventas(db: Session):
    """Obtener métricas de ventas por periodo"""
    hoy = datetime.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio_mes = hoy.replace(day=1)
    
    # Ventas de hoy - USAR CAST para SQL Server
    ventas_hoy_result = db.query(func.sum(Pedido.total)).filter(
        cast(Pedido.created_at, Date) == hoy  # ✅ CORREGIDO para SQL Server
    ).scalar()
    ventas_hoy = ventas_hoy_result if ventas_hoy_result else Decimal('0.00')
    
    # Ventas de esta semana
    ventas_semana_result = db.query(func.sum(Pedido.total)).filter(
        cast(Pedido.created_at, Date) >= inicio_semana  # ✅ CORREGIDO
    ).scalar()
    ventas_semana = ventas_semana_result if ventas_semana_result else Decimal('0.00')
    
    # Ventas de este mes
    ventas_mes_result = db.query(func.sum(Pedido.total)).filter(
        cast(Pedido.created_at, Date) >= inicio_mes  # ✅ CORREGIDO
    ).scalar()
    ventas_mes = ventas_mes_result if ventas_mes_result else Decimal('0.00')
    
    # Ventas del mes anterior para calcular crecimiento
    if inicio_mes.month == 1:
        mes_anterior_inicio = inicio_mes.replace(year=inicio_mes.year-1, month=12)
    else:
        mes_anterior_inicio = inicio_mes.replace(month=inicio_mes.month-1)
    
    mes_anterior_fin = inicio_mes - timedelta(days=1)
    
    ventas_mes_anterior_result = db.query(func.sum(Pedido.total)).filter(
        and_(
            cast(Pedido.created_at, Date) >= mes_anterior_inicio,  # ✅ CORREGIDO
            cast(Pedido.created_at, Date) <= mes_anterior_fin      # ✅ CORREGIDO
        )
    ).scalar()
    ventas_mes_anterior = ventas_mes_anterior_result if ventas_mes_anterior_result else Decimal('0.00')
    
    # Calcular crecimiento porcentual
    if ventas_mes_anterior > 0:
        crecimiento_mensual = ((ventas_mes - ventas_mes_anterior) / ventas_mes_anterior) * 100
    else:
        crecimiento_mensual = Decimal('100.00') if ventas_mes > 0 else Decimal('0.00')
    
    return {
        "ventas_hoy": ventas_hoy,
        "ventas_semana": ventas_semana,
        "ventas_mes": ventas_mes,
        "crecimiento_mensual": crecimiento_mensual
    }

def get_productos_populares(db: Session, limit: int = 5):
    """Obtener productos más vendidos"""
    productos_populares = db.query(
        Producto.id,
        Producto.nombre,
        Producto.sku,
        func.sum(DetallePedido.cantidad).label('cantidad_vendida'),
        func.sum(DetallePedido.subtotal).label('total_ventas')
    ).join(DetallePedido, Producto.id == DetallePedido.producto_id
    ).group_by(Producto.id, Producto.nombre, Producto.sku
    ).order_by(func.sum(DetallePedido.cantidad).desc()
    ).limit(limit).all()
    
    return [
        {
            "id": producto.id,
            "nombre": producto.nombre,
            "sku": producto.sku,
            "cantidad_vendida": producto.cantidad_vendida or 0,
            "total_ventas": producto.total_ventas or Decimal('0.00')
        }
        for producto in productos_populares
    ]

def get_pedidos_pendientes(db: Session, limit: int = 5):
    """Obtener pedidos pendientes de entrega"""
    pedidos_pendientes = db.query(Pedido).join(Cliente).filter(
        Pedido.estado == EstadoPedido.PENDIENTE_ENTREGA
    ).order_by(Pedido.created_at.asc()
    ).limit(limit).all()
    
    return [
        {
            "id": pedido.id,
            "cliente_nombre": pedido.cliente.nombre,
            "total": pedido.total,
            "fecha_pedido": pedido.created_at,
            "estado": pedido.estado.value
        }
        for pedido in pedidos_pendientes
    ]

def get_rutas_activas(db: Session):
    """Obtener rutas activas con información de repartidores"""
    rutas_activas = db.query(Ruta).filter(Ruta.estado == True).all()
    
    resultado = []
    for ruta in rutas_activas:
        # Contar clientes en la ruta
        total_clientes = len(ruta.rutas_clientes)
        
        # Obtener repartidor asignado (si existe)
        repartidor = None
        if ruta.rutas_asignadas:
            ultima_asignacion = ruta.rutas_asignadas[-1]  # La más reciente
            repartidor = f"{ultima_asignacion.usuario.username}"
        
        resultado.append({
            "id": ruta.id,
            "nombre": ruta.nombre,
            "tipo": ruta.tipo.value,
            "total_clientes": total_clientes,
            "repartidor": repartidor
        })
    
    return resultado

def get_ventas_mensuales(db: Session, meses: int = 6):
    """Obtener estadísticas de ventas de los últimos meses"""
    fecha_limite = datetime.now() - timedelta(days=30*meses)
    
    # Usar extract para SQL Server - CORREGIDO
    ventas_mensuales = db.query(
        extract('year', Pedido.created_at).label('ano'),
        extract('month', Pedido.created_at).label('mes'),
        func.sum(Pedido.total).label('total_ventas'),
        func.count(Pedido.id).label('cantidad_pedidos')
    ).filter(Pedido.created_at >= fecha_limite
    ).group_by(
        extract('year', Pedido.created_at),
        extract('month', Pedido.created_at)
    ).order_by('ano', 'mes').all()
    
    # Formatear resultado
    meses_espanol = {
        1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
    }
    
    return [
        {
            "mes": f"{meses_espanol[int(venta.mes)]} {int(venta.ano)}",
            "total_ventas": venta.total_ventas or Decimal('0.00'),
            "cantidad_pedidos": venta.cantidad_pedidos or 0
        }
        for venta in ventas_mensuales
    ]