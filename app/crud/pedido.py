from sqlalchemy.orm import Session
from sqlalchemy import and_
from decimal import Decimal
from app.models.pedido import Pedido, EstadoPedido
from app.models.detalle_pedido import DetallePedido
from app.models.producto import Producto
from app.schemas.pedidos import PedidoCreate, PedidoUpdate

def get_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

def get_pedidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pedido).order_by(Pedido.id).offset(skip).limit(limit).all()

def get_pedidos_by_cliente(db: Session, cliente_id: int):
    return db.query(Pedido).filter(Pedido.cliente_id == cliente_id).all()

def get_pedidos_by_vendedor(db: Session, vendedor_id: int):
    return db.query(Pedido).filter(Pedido.vendedor_id == vendedor_id).all()

def create_pedido(db: Session, pedido: PedidoCreate):
    # Calcular total y verificar stock
    total = Decimal('0.00')
    
    # Verificar stock y calcular total
    for detalle in pedido.detalles:
        producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
        if not producto:
            raise ValueError(f"Producto con ID {detalle.producto_id} no encontrado")
        if producto.stock < detalle.cantidad:
            raise ValueError(f"Stock insuficiente para producto {producto.nombre}")
        
        subtotal = detalle.precio_unitario * detalle.cantidad
        total += subtotal
    
    # Crear pedido
    db_pedido = Pedido(
        cliente_id=pedido.cliente_id,
        vendedor_id=pedido.vendedor_id,
        fecha_pedido=pedido.fecha_pedido,
        total=total,
        estado=EstadoPedido.PENDIENTE_ENTREGA
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    
    # Crear detalles del pedido y actualizar stock
    for detalle in pedido.detalles:
        db_detalle = DetallePedido(
            pedido_id=db_pedido.id,
            producto_id=detalle.producto_id,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.precio_unitario,
            subtotal=detalle.precio_unitario * detalle.cantidad
        )
        db.add(db_detalle)
        
        # Actualizar stock del producto
        producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
        producto.stock -= detalle.cantidad
    
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def update_pedido_estado(db: Session, pedido_id: int, pedido_update: PedidoUpdate):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not db_pedido:
        return None
    
    if pedido_update.estado:
        db_pedido.estado = pedido_update.estado
    
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def delete_pedido(db: Session, pedido_id: int):
    db_pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if db_pedido:
        # Restaurar stock si el pedido se elimina
        if db_pedido.estado == EstadoPedido.PENDIENTE_ENTREGA:
            for detalle in db_pedido.detalle_pedidos:
                producto = db.query(Producto).filter(Producto.id == detalle.producto_id).first()
                if producto:
                    producto.stock += detalle.cantidad
        
        db.delete(db_pedido)
        db.commit()
        return True
    return False