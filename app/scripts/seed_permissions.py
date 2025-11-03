from app.config.database import SessionLocal
from app.models.permission import Permission
from app.models.role import Role

def seed_permissions():
    db = SessionLocal()
    try:
        # Permisos base del sistema
        permissions_data = [
            # Módulo Usuarios
            {"name": "users.view", "description": "Ver usuarios", "module": "users", "action": "read"},
            {"name": "users.create", "description": "Crear usuarios", "module": "users", "action": "create"},
            {"name": "users.update", "description": "Actualizar usuarios", "module": "users", "action": "update"},
            {"name": "users.delete", "description": "Eliminar usuarios", "module": "users", "action": "delete"},
            {"name": "users.manage", "description": "Gestionar usuarios completo", "module": "users", "action": "manage"},
            
            # Módulo Productos
            {"name": "products.view", "description": "Ver productos", "module": "products", "action": "read"},
            {"name": "products.create", "description": "Crear productos", "module": "products", "action": "create"},
            {"name": "products.update", "description": "Actualizar productos", "module": "products", "action": "update"},
            {"name": "products.delete", "description": "Eliminar productos", "module": "products", "action": "delete"},
            {"name": "products.manage", "description": "Gestionar productos completo", "module": "products", "action": "manage"},
            
            # Módulo Pedidos
            {"name": "orders.view", "description": "Ver pedidos", "module": "orders", "action": "read"},
            {"name": "orders.create", "description": "Crear pedidos", "module": "orders", "action": "create"},
            {"name": "orders.update", "description": "Actualizar pedidos", "module": "orders", "action": "update"},
            {"name": "orders.delete", "description": "Eliminar pedidos", "module": "orders", "action": "delete"},
            {"name": "orders.manage", "description": "Gestionar pedidos completo", "module": "orders", "action": "manage"},
            
            # Módulo Reportes
            {"name": "reports.view", "description": "Ver reportes", "module": "reports", "action": "read"},
            {"name": "reports.generate", "description": "Generar reportes", "module": "reports", "action": "create"},
            
            # Módulo Sistema
            {"name": "system.settings", "description": "Configurar sistema", "module": "system", "action": "manage"},
        ]
        
        # Crear permisos si no existen
        for perm_data in permissions_data:
            existing_perm = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
            if not existing_perm:
                db_perm = Permission(**perm_data)
                db.add(db_perm)
        
        db.commit()
        print("✅ Permisos creados correctamente")
        
        # Asignar permisos a roles
        roles_permissions = {
            "gerente": ["users.manage", "reports.view", "reports.generate", "system.settings"],
            "administrador": ["products.manage", "orders.manage", "reports.view"],
            "vendedor": ["products.view", "orders.create", "orders.view", "orders.update"],
            "repartidor": ["orders.view", "orders.update"],
            "usuario_sistema": ["users.view"]  # Permisos básicos
        }
        
        for role_name, permission_names in roles_permissions.items():
            role = db.query(Role).filter(Role.name == role_name).first()
            if role:
                for perm_name in permission_names:
                    permission = db.query(Permission).filter(Permission.name == perm_name).first()
                    if permission and permission not in role.permissions:
                        role.permissions.append(permission)
                        print(f"✅ Permiso '{perm_name}' asignado a rol '{role_name}'")
        
        db.commit()
        print("🎉 Permisos sembrados y asignados correctamente")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error sembrando permisos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_permissions()