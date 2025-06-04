from pydantic import BaseModel, EmailStr
from typing import Optional

class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    plan: Optional[str] = None
    createdAt: Optional[str] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True



class UpdatePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class UpdateUserRequest(BaseModel):
    full_name: Optional[str] = None  # 👈 yeni alan
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


