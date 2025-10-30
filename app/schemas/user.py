from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schema de Token SIN user
class Token(BaseModel):
    access_token: str
    token_type: str
    # Eliminamos el campo 'user'

class TokenData(BaseModel):
    email: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    message: str = "Login exitoso"


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str
    message: str = "Token refrescado exitosamente"

# Agrega este schema para actualizar usuario
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None