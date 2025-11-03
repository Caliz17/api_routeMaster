from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.auth.utils import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).order_by(User.id).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    from app.models.role import Role
    default_role = db.query(Role).filter(Role.name == "usuario_sistema").first()
    
    if not default_role:
        default_role = db.query(Role).first()
        if not default_role:
            raise Exception("No hay roles disponibles en la base de datos")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role_id=default_role.id 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.is_active = False
        db.commit()
        return True
    return False

def update_user_role(db: Session, user_id: int, role_id: int):
    """
    Actualizar el rol de un usuario
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    
    user.role_id = role_id
    db.commit()
    db.refresh(user)
    return user