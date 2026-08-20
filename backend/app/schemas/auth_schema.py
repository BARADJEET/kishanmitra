from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    email: str
    phone: Optional[str] = None
    password: str
    full_name: str
    role: Optional[str] = "farmer"
    language_pref: Optional[str] = "en"
    state: Optional[str] = "Gujarat"
    district: Optional[str] = "Ahmedabad"
    village: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserProfileResponse(BaseModel):
    full_name: str
    language_pref: str
    state: str
    district: str
    village: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    email: str
    phone: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    profile: Optional[UserProfileResponse] = None

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    language_pref: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None
    avatar_url: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
