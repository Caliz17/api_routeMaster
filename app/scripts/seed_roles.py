# app/scripts/seed_roles.py
from app.config.database import SessionLocal
from app.models.role import Role

def seed_roles():
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
                print(f"✅ Rol {role_data['name']} creado")
            else:
                print(f"⚠️ Rol {role_data['name']} ya existe")
        
        db.commit()
        print("🎉 Roles sembrados correctamente")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error sembrando roles: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_roles()