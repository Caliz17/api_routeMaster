# app/scripts/setup_database.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.config.database import SessionLocal, Base, engine
from app.models.role import Role

def setup_database():
    print("🚀 Configurando base de datos completa...")
    
    # 1. Crear todas las tablas
    print("📦 Creando tablas...")
    Base.metadata.create_all(bind=engine)
    
    # 2. Verificar tablas creadas
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("✅ Tablas creadas:")
    for table in tables:
        print(f"   - {table}")
    
    # 3. Sembrar roles
    print("🌱 Sembrando roles...")
    db = SessionLocal()
    try:
        roles_data = [
            {"name": "gerente", "description": "Administra usuarios y consulta reportes"},
            {"name": "administrador", "description": "Gestiona rutas y productos"},
            {"name": "vendedor", "description": "Consulta rutas de venta, registra clientes y pedidos"},
            {"name": "repartidor", "description": "Consulta rutas de entrega, confirma entregas y registra cobros"},
            {"name": "usuario_sistema", "description": "Rol general para autenticación"}
        ]
        
        for role_data in roles_data:
            existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
            if not existing_role:
                db_role = Role(**role_data)
                db.add(db_role)
                print(f"   ✅ {role_data['name']}")
        
        db.commit()
        print("🎉 Base de datos configurada exitosamente!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    setup_database()