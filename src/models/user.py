from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id_user: int
    password_hash: str
    id_listener: Optional[int] = None
    id_author: Optional[int] = None

class UserResponse(UserBase):
    id_user: int
    id_listener: Optional[int] = None
    id_author: Optional[int] = None