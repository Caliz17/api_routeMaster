from sqlalchemy.orm import Session
from app.models.producto import Producto
from app.schemas.producto import ProductoCreate, ProductoUpdate

def get_producto(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()

def get_producto_by_sku(db: Session, sku: str):
    return db.query(Producto).filter(Producto.sku == sku).first()

def get_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Producto).order_by(Producto.id).offset(skip).limit(limit).all()

def create_producto(db: Session, producto: ProductoCreate):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto_update: ProductoUpdate):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        return None
    
    update_data = producto_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_producto, field, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto:
        db_producto.estado = False
        db.commit()
        return True
    return False