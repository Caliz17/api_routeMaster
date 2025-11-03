from sqlalchemy.orm import Session
from app.models.ruta import Ruta
from app.models.ruta_cliente import RutaCliente
from app.models.ruta_asignada import RutaAsignada
from app.schemas.ruta import RutaCreate, RutaUpdate

def get_ruta(db: Session, ruta_id: int):
    return db.query(Ruta).filter(Ruta.id == ruta_id).first()

def get_rutas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ruta).order_by(Ruta.id).offset(skip).limit(limit).all()

def get_rutas_activas(db: Session):
    return db.query(Ruta).filter(Ruta.estado == True).all()

def get_rutas_by_tipo(db: Session, tipo: str):
    return db.query(Ruta).filter(Ruta.tipo == tipo).all()

def create_ruta(db: Session, ruta: RutaCreate):
    db_ruta = Ruta(
        nombre=ruta.nombre,
        tipo=ruta.tipo,
        creada_por_id=ruta.creada_por_id,
        estado=True
    )
    db.add(db_ruta)
    db.commit()
    db.refresh(db_ruta)
    
    # Crear relaciones con clientes si se proporcionan
    if ruta.clientes:
        for cliente_data in ruta.clientes:
            db_ruta_cliente = RutaCliente(
                ruta_id=db_ruta.id,
                cliente_id=cliente_data.cliente_id,
                orden=cliente_data.orden
            )
            db.add(db_ruta_cliente)
    
    db.commit()
    db.refresh(db_ruta)
    return db_ruta

def update_ruta(db: Session, ruta_id: int, ruta_update: RutaUpdate):
    db_ruta = db.query(Ruta).filter(Ruta.id == ruta_id).first()
    if not db_ruta:
        return None
    
    update_data = ruta_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_ruta, field, value)
    
    db.commit()
    db.refresh(db_ruta)
    return db_ruta

def delete_ruta(db: Session, ruta_id: int):
    db_ruta = db.query(Ruta).filter(Ruta.id == ruta_id).first()
    if db_ruta:
        db_ruta.estado = False
        db.commit()
        return True
    return False

# CRUD para RutaCliente
def add_cliente_a_ruta(db: Session, ruta_id: int, cliente_id: int, orden: int):
    db_ruta_cliente = RutaCliente(
        ruta_id=ruta_id,
        cliente_id=cliente_id,
        orden=orden
    )
    db.add(db_ruta_cliente)
    db.commit()
    db.refresh(db_ruta_cliente)
    return db_ruta_cliente

def remove_cliente_de_ruta(db: Session, ruta_cliente_id: int):
    db_ruta_cliente = db.query(RutaCliente).filter(RutaCliente.id == ruta_cliente_id).first()
    if db_ruta_cliente:
        db.delete(db_ruta_cliente)
        db.commit()
        return True
    return False

# CRUD para RutaAsign orden = Coluada
def asignar_ruta_usuario(db: Session, ruta_id: int, usuario_id: int, fecha):
    db_ruta_asignada = RutaAsignada(
        ruta_id=ruta_id,
        usuario_id=usuario_id,
        fecha=fecha
    )
    db.add(db_ruta_asignada)
    db.commit()
    db.refresh(db_ruta_asignada)
    return db_ruta_asignada

def desasignar_ruta_usuario(db: Session, ruta_asignada_id: int):
    db_ruta_asignada = db.query(RutaAsignada).filter(RutaAsignada.id == ruta_asignada_id).first()
    if db_ruta_asignada:
        db.delete(db_ruta_asignada)
        db.commit()
        return True
    return False