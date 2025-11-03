from pydantic import BaseModel
from typing import Optional, List

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    module: str
    action: str

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class RoleWithPermissions(BaseModel):
    id: int
    name: str
    description: Optional[str]
    permissions: List[PermissionResponse]
    
    class Config:
        from_attributes = True