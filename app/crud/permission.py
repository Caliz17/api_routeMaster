from sqlalchemy.orm import Session
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate

def get_permission(db: Session, permission_id: int):
    return db.query(Permission).filter(Permission.id == permission_id).first()

def get_permission_by_name(db: Session, name: str):
    return db.query(Permission).filter(Permission.name == name).first()

def get_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Permission).offset(skip).limit(limit).all()

def get_permissions_by_module(db: Session, module: str):
    return db.query(Permission).filter(Permission.module == module).all()

def create_permission(db: Session, permission: PermissionCreate):
    db_permission = Permission(**permission.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def assign_permission_to_role(db: Session, role_id: int, permission_id: int):
    from app.models.role import Role
    role = db.query(Role).filter(Role.id == role_id).first()
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    
    if role and permission:
        role.permissions.append(permission)
        db.commit()
        return True
    return False