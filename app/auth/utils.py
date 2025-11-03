from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.user import User
from app.config.config import settings

# Configuración
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Usar bcrypt con configuración específica
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    # Limitar la contraseña a 72 caracteres para bcrypt
    if len(password) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(email: str):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def get_current_user(token: str, db = None):
    try:
        print(f"🔍 Verificando token: {token[:50]}...")  # ✅ LOG para debug
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        print(f"🔍 Email del token: {email}")  # ✅ LOG para debug
        
        if email is None:
            print("❌ Token no tiene email")
            return None
            
    except JWTError as e:
        print(f"❌ Error decodificando token: {e}")  # ✅ LOG para debug
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")  # ✅ LOG para debug
        return None
    
    if db:
        user = db.query(User).filter(User.email == email).first()
    else:
        from app.config.database import SessionLocal
        db_session = SessionLocal()
        try:
            user = db_session.query(User).filter(User.email == email).first()
        finally:
            db_session.close()
    
    print(f"🔍 Usuario encontrado: {user}")  # ✅ LOG para debug
    return user